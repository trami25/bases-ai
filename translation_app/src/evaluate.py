import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from torch.utils.data import DataLoader
from model import TranslationModel
from data_preprocessing import preprocess_text
from dataset import TranslationDataset, collate_fn
from train import build_vocab

def evaluate_model(model, dataloader):
    model.eval()
    scores = []
    smoothie = SmoothingFunction().method1

    with torch.no_grad():
        for source, target in dataloader:
            source = source.long()
            target = target.long()
            output = model(source)
            predictions = output.argmax(dim=2)

            for pred, tgt in zip(predictions, target):
                pred = pred.cpu().tolist()
                tgt = tgt.cpu().tolist()
                scores.append(sentence_bleu([tgt], pred, smoothing_function=smoothie))

    return sum(scores) / len(scores)

if __name__ == "__main__":
    source_file = '../txt/nouns.txt'
    target_file = '../txt/imenice.txt'

    vocab = build_vocab(source_file, target_file, preprocess_text)

    dataset = TranslationDataset(source_file, target_file, preprocess_text, vocab)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

    input_size = len(vocab) + 1
    hidden_size = 256
    output_size = len(vocab) + 1

    model = TranslationModel(input_size, 256, hidden_size, output_size)
    model.load_state_dict(torch.load("../models/translation_model.pth"))

    bleu_score = evaluate_model(model, dataloader)
    print(f'BLEU score: {bleu_score:.4f}')
