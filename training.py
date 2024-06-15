import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json

# Load the training data
with open('data.json', 'r') as file:
    data = json.load(file)

# Preprocess the data
questions = [q['question'] for q in data]
answers = [q['answer'] for q in data]

# Tokenize the questions and answers
tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers)
question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

# Pad the sequences to a fixed length
max_length = max(len(seq) for seq in question_sequences)
question_padded = pad_sequences(question_sequences, maxlen=max_length, padding='post')
answer_padded = pad_sequences(answer_sequences, maxlen=max_length, padding='post')

# Define the model architecture
model = Sequential()
model.add(Embedding(len(tokenizer.word_index) + 1, 128, input_length=max_length))
model.add(LSTM(128))
model.add(Dense(len(tokenizer.word_index) + 1, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(question_padded, tf.keras.utils.to_categorical(answer_padded), epochs=100, batch_size=32)

# Save the model and tokenizer
model.save('chatbot_model.h5')
with open('tokenizer.json', 'w') as file:
    json.dump(tokenizer.to_json(), file)