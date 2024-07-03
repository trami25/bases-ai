import torch
from flask import Flask, request, jsonify
from translation_app.src.data_preprocessing import preprocess_text, preprocess_text_sr
from translation_app.src.model import TranslationModel
from translation_app.src.train import build_vocab

app = Flask(__name__)

# Load vocabulary
source_file = '../txt/nouns.txt'
target_file = '../txt/imenice.txt'
vocab = build_vocab(source_file, target_file, preprocess_text)
sr_to_en_vocab = build_vocab(target_file, source_file, preprocess_text_sr)

model = TranslationModel(len(vocab) + 1, 256, 256, len(vocab) + 1)
model.load_state_dict(torch.load("../models/translation_model.pth"))
model.eval()

sr_to_en_model = TranslationModel(len(sr_to_en_vocab) + 1, 256, 256, len(sr_to_en_vocab) + 1)
sr_to_en_model.load_state_dict(torch.load("../models/sr_to_en_model.pth"))
sr_to_en_model.eval()


def translate_text_backend(source_text):
    tokens = preprocess_text(source_text)
    token_indices = [vocab.get(f"{word}_{pos}", vocab["<UNK>"]) for word, pos in tokens]
    input_tensor = torch.tensor([token_indices], dtype=torch.long)

    with torch.no_grad():
        output = model(input_tensor)
        predicted_indices = output.argmax(dim=2).squeeze().tolist()

    if isinstance(predicted_indices, int):
        predicted_indices = [predicted_indices]

    idx_to_word = {index: word.split('_')[0] for word, index in vocab.items()}

    translated_tokens = []
    for token, idx in zip(tokens, predicted_indices):
        word, pos = token
        if pos == 'PUNCTUATION':
            translated_tokens.append(word)
        else:
            translated_tokens.append(idx_to_word.get(idx, "<UNK>"))

    translated_text = ' '.join(translated_tokens)

    # Ensure proper formatting
    for punct in ['.', ',', '!', '?', ':', ';', '-', '(', ')', '"', "'"]:
        translated_text = translated_text.replace(f" {punct}", punct)

    return translated_text


def translate_text_sr_to_en(source_text):
    tokens = preprocess_text_sr(source_text)
    token_indices = [sr_to_en_vocab.get(f"{word}_{pos}", sr_to_en_vocab["<UNK>"]) for word, pos in tokens]
    input_tensor = torch.tensor([token_indices], dtype=torch.long)

    with torch.no_grad():
        output = sr_to_en_model(input_tensor)
        predicted_indices = output.argmax(dim=2).squeeze().tolist()

    if isinstance(predicted_indices, int):
        predicted_indices = [predicted_indices]

    idx_to_word = {index: word.split('_')[0] for word, index in sr_to_en_vocab.items()}

    translated_tokens = []
    for token, idx in zip(tokens, predicted_indices):
        word, pos = token
        if pos == 'PUNCTUATION':
            translated_tokens.append(word)
        else:
            translated_tokens.append(idx_to_word.get(idx, "<UNK>"))

    translated_text = ' '.join(translated_tokens)
    for punct in ['.', ',', '!', '?', ':', ';', '-', '(', ')', '"', "'"]:
        translated_text = translated_text.replace(f" {punct}", punct)

    return translated_text


