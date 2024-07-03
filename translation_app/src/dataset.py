import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence

class TranslationDataset(Dataset):
    def __init__(self, source_file, target_file, preprocess, vocab):
        self.source_data = []
        self.target_data = []

        with open(source_file, 'r', encoding='utf-8') as sf:
            self.source_data.extend(sf.readlines())
        with open(target_file, 'r', encoding='utf-8') as tf:
            self.target_data.extend(tf.readlines())

        self.preprocess = preprocess
        self.vocab = vocab

    def __len__(self):
        return len(self.source_data)

    def __getitem__(self, idx):
        source_line = self.source_data[idx].strip()
        target_line = self.target_data[idx].strip()

        source_tokens = self.preprocess(source_line)
        target_tokens = self.preprocess(target_line)

        source_indices = [self.vocab.get(f"{word}_{pos}", self.vocab["<UNK>"]) for word, pos in source_tokens]
        target_indices = [self.vocab.get(f"{word}_{pos}", self.vocab["<UNK>"]) for word, pos in target_tokens]

        return torch.tensor(source_indices), torch.tensor(target_indices)

def collate_fn(batch):
    sources, targets = zip(*batch)
    sources_padded = pad_sequence(sources, batch_first=True, padding_value=1)
    targets_padded = pad_sequence(targets, batch_first=True, padding_value=1)
    return sources_padded, targets_padded
