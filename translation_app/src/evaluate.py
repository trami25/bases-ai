import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from torch.utils.data import DataLoader
from model import TranslationModel
from data_preprocessing import preprocess_text, preprocess_text_sr
from dataset import TranslationDataset, collate_fn
from train import build_vocab

def evaluate_model(model, dataloader, device):
    model.eval()
    scores = []
    smoothie = SmoothingFunction().method1
    model.to(device)

    with torch.no_grad():
        for source, target in dataloader:
            source, target = source.long().to(device), target.long().to(device)
            output = model(source)
            predictions = output.argmax(dim=2)

            for pred, tgt in zip(predictions, target):
                pred = pred.cpu().tolist()
                tgt = tgt.cpu().tolist()
                scores.append(sentence_bleu([tgt], pred, smoothing_function=smoothie))

    return sum(scores) / len(scores)

# Evaluation script with CUDA support
if __name__ == "__main__":
    source_file = '../txt/nouns.txt'
    target_file = '../txt/imenice.txt'

    vocab = build_vocab(source_file, target_file, preprocess_text)
    dataset = TranslationDataset(source_file, target_file, preprocess_text, vocab)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TranslationModel(len(vocab) + 1, 256, 256, len(vocab) + 1)
    model.load_state_dict(torch.load("../models/translation_model.pth"))

    bleu_score = evaluate_model(model, dataloader, device)
    print(f'BLEU score for en_sr: {bleu_score:.4f}')

    sr_vocab = build_vocab(target_file, source_file, preprocess_text_sr)
    sr_dataset = TranslationDataset(target_file, source_file, preprocess_text_sr, sr_vocab)
    sr_dataloader = DataLoader(sr_dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

    sr_model = TranslationModel(len(sr_vocab) + 1, 256, 256, len(sr_vocab) + 1)
    sr_model.load_state_dict(torch.load("../models/sr_to_en_model.pth"))

    sr_bleu_score = evaluate_model(sr_model, sr_dataloader, device)
    print(f'BLEU score for sr_en: {sr_bleu_score:.4f}')
