import torch
from torch.utils.data import DataLoader
from model import TranslationModel
from data_preprocessing import preprocess_text
from dataset import TranslationDataset, collate_fn


def train_model(model, dataloader, epochs, learning_rate):
    criterion = torch.nn.CrossEntropyLoss(ignore_index=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for source, target in dataloader:
            optimizer.zero_grad()
            source = source.long()
            target = target.long()

            output = model(source)
            output = output.view(-1, output.shape[-1])
            target = target.view(-1)

            if output.shape[0] > target.shape[0]:
                target = torch.cat(
                    [target, torch.ones(output.shape[0] - target.shape[0], dtype=torch.long)], dim=0
                )

            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(dataloader)}')


def build_vocab(source_file, target_file, preprocess):
    vocab = {"<UNK>": 0, "<PAD>": 1}
    files = [source_file, target_file]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                tokens = preprocess(line.strip())
                for token in tokens:
                    if token not in vocab:
                        vocab[token] = len(vocab)
    return vocab


if __name__ == '__main__':
    source_file = 'C:\\Users\\mniko\\PycharmProjects\\bases-ai\\translation_app\\txt\\nouns.txt'
    target_file = 'C:\\Users\\mniko\\PycharmProjects\\bases-ai\\translation_app\\txt\\imenice.txt'

    vocab = build_vocab(source_file, target_file, preprocess_text)

    dataset = TranslationDataset(source_file, target_file, preprocess_text, vocab)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

    input_size = len(vocab) + 1
    hidden_size = 256
    output_size = len(vocab) + 1

    model = TranslationModel(input_size, 256, hidden_size, output_size)
    train_model(model, dataloader, epochs=50, learning_rate=0.001)
    torch.save(model.state_dict(), "../models/translation_model.pth")
