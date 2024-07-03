import torch
from torch.utils.data import DataLoader
from model import TranslationModel
from data_preprocessing import preprocess_text, preprocess_text_sr
from dataset import TranslationDataset, collate_fn

def train_model(model, dataloader, epochs, learning_rate):
    criterion = torch.nn.CrossEntropyLoss(ignore_index=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for source, target in dataloader:
            optimizer.zero_grad()
            source, target = source.long(), target.long()

            output = model(source)

            if output.shape[1] < target.shape[1]:
                target = target[:, :output.shape[1]]
            elif output.shape[1] > target.shape[1]:
                padding = torch.ones((target.shape[0], output.shape[1] - target.shape[1]), dtype=torch.long)
                target = torch.cat((target, padding), dim=1)


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

def train_model_sr_to_en(model, dataloader, epochs=100, learning_rate=0.001):
    criterion = torch.nn.CrossEntropyLoss(ignore_index=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for source, target in dataloader:
            optimizer.zero_grad()
            source, target = source.long(), target.long()

            output = model(source)

            if output.shape[1] < target.shape[1]:
                target = target[:, :output.shape[1]]
            elif output.shape[1] > target.shape[1]:
                padding = torch.ones((target.shape[0], output.shape[1] - target.shape[1]), dtype=torch.long)
                target = torch.cat((target, padding), dim=1)

            output = output.view(-1, output.shape[-1])
            target = target.view(-1)

            if output.shape[0] > source.shape[0]:
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
                for word, pos in tokens:
                    token = f"{word}_{pos}"
                    if token not in vocab:
                        vocab[token] = len(vocab)
    return vocab

if __name__ == '__main__':
    source_file = '../txt/nouns.txt'
    target_file = '../txt/imenice.txt'

    vocab = build_vocab(source_file, target_file, preprocess_text)

    dataset = TranslationDataset(source_file, target_file, preprocess_text, vocab)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

    model = TranslationModel(len(vocab) + 1, 256, 256, len(vocab) + 1)
    train_model(model, dataloader, epochs=50, learning_rate=0.001)
    torch.save(model.state_dict(), "../models/translation_model.pth")

    # sr_to_en_vocab = build_vocab(target_file, source_file, preprocess_text_sr)
    # sr_to_en_dataset = TranslationDataset(target_file, source_file, preprocess_text_sr, sr_to_en_vocab)
    # sr_to_en_dataloader = DataLoader(sr_to_en_dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)
    # sr_to_en_model = TranslationModel(len(sr_to_en_vocab) + 1, 256, 256, len(sr_to_en_vocab) + 1)
    # train_model_sr_to_en(sr_to_en_model, sr_to_en_dataloader, epochs=100, learning_rate=0.001)
    # torch.save(sr_to_en_model.state_dict(), "../models/sr_to_en_model.pth")
