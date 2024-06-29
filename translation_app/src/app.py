import torch
from flask import Flask, request, jsonify
from translation_app.src.data_preprocessing import preprocess_text
from translation_app.src.model import TranslationModel
from translation_app.src.train import build_vocab

app = Flask(__name__)

# Load vocabulary
source_file = 'C:\\Users\\mniko\\PycharmProjects\\bases-ai\\translation_app\\txt\\nouns.txt'
target_file = 'C:\\Users\\mniko\\PycharmProjects\\bases-ai\\translation_app\\txt\\imenice.txt'
vocab = build_vocab(source_file, target_file, preprocess_text)


def translate_text_backend(source_text):
    tokens = preprocess_text(source_text)
    token_indices = [vocab.get(token, vocab["<UNK>"]) for token in tokens]
    input_tensor = torch.tensor([token_indices], dtype=torch.long)

    input_size = len(vocab) + 1
    hidden_size = 256
    output_size = len(vocab) + 1
    model = TranslationModel(input_size,256, hidden_size, output_size)
    model.load_state_dict(torch.load("../models/translation_model.pth"))
    model.eval()

    with torch.no_grad():
        output = model(input_tensor)
        predicted_indices = output.argmax(dim=2).squeeze().tolist()

    idx_to_word = {index: word for word, index in vocab.items()}
    if isinstance(predicted_indices, int):
        predicted_indices = [predicted_indices]
    translated_text = ' '.join([idx_to_word[idx] for idx in predicted_indices if idx in idx_to_word])

    return translated_text
