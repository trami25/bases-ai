import torch.nn as nn

class TranslationModel(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, output_size):
        super(TranslationModel, self).__init__()
        self.embedding = nn.Embedding(input_size, embedding_size)
        self.rnn = nn.LSTM(embedding_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        output, _ = self.rnn(embedded)
        output = self.fc(output)
        return output
