import tensorflow as tf
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Load real SMS Spam Collection dataset
data_path = '/Users/harish/Downloads/SMSSpamCollection'
data = []
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t', 1)
        if len(parts) == 2:
            label, text = parts
            data.append({'text': text, 'label': 1 if label == 'spam' else 0})

df = pd.DataFrame(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Text vectorization
max_tokens = 10000
max_len = 50
vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=max_tokens,
    output_mode='int',
    output_sequence_length=max_len
)
vectorizer.adapt(X_train)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(max_len,)),
    tf.keras.layers.Embedding(input_dim=max_tokens, output_dim=128),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
model.fit(vectorizer(X_train), np.array(y_train), epochs=10, batch_size=32, validation_split=0.2)

# Save model
model.save('model/scam_model.h5')

# Save vectorizer vocabulary
vocabulary = vectorizer.get_vocabulary()
with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump({'vocabulary': vocabulary}, f)

print("Model and vectorizer saved successfully!")