import pandas as pd
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence

class TranslationDataset(Dataset):
    def __init__(self, source_file, target_file, preprocess, vocab):
        self.source_data = pd.read_csv(source_file, header=None)[0].tolist()
        self.target_data = pd.read_csv(target_file, header=None)[0].tolist()
        self.preprocess = preprocess
        self.vocab = vocab

    def __len__(self):
        return len(self.source_data)

    def __getitem__(self, idx):
        source_text = self.preprocess(self.source_data[idx])
        target_text = self.preprocess(self.target_data[idx])
        source_indices = [self.vocab.get(word, self.vocab["<UNK>"]) for word in source_text]
        target_indices = [self.vocab.get(word, self.vocab["<UNK>"]) for word in target_text]
        return torch.tensor(source_indices), torch.tensor(target_indices)

def collate_fn(batch):
    sources, targets = zip(*batch)
    sources_padded = pad_sequence(sources, batch_first=True, padding_value=1)
    targets_padded = pad_sequence(targets, batch_first=True, padding_value=1)
    return sources_padded, targets_padded
