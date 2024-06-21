'''from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding


def create_model(vocab_size, embedding_dim, input_length):
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=input_length),
        LSTM(units=128),
        Dense(units=vocab_size, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
'''