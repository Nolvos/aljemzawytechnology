# -*- coding: utf-8 -*-
"""Task4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13NGFirwLsQNljOSv7eF-kNMfRWiMO4Li
"""

from google.colab import drive
drive.mount('/content/drive')

"""#Linguistic Analysis"""

pip install SpeechRecognition textblob nltk

!apt install ffmpeg -y

import os
import speech_recognition as sr
from textblob import TextBlob
import nltk
import subprocess

# Download NLTK Punkt tokenizer data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize the speech recognizer
recognizer = sr.Recognizer()


def transcribe_mp3(mp3_file):
    # Convert the MP3 file to WAV using ffmpeg
    wav_file = mp3_file.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-i", mp3_file, wav_file])

    # Transcribe the WAV recording
    with sr.AudioFile(wav_file) as source:
        audio_text = recognizer.listen(source)
        try:
            # Use Google Web Speech API for speech recognition
            transcription = recognizer.recognize_google(audio_text)
            return transcription
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        finally:
            # Clean up the temporary WAV file
            os.remove(wav_file)



# Function to segment text into sentences
def segment_text(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

# Function to perform basic linguistic analysis
def linguistic_analysis(text):
    blob = TextBlob(text)

    # Word count
    word_count = len(blob.words)

    # Sentence count
    sentence_count = len(blob.sentences)

    # Part-of-speech tagging
    pos_tags = blob.tags

    print("Word count:", word_count)
    print("Sentence count:", sentence_count)
    print("Part-of-speech tags:", pos_tags)

# Function to process all files in a directory
def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_file_path = os.path.join(directory, filename)
            print("Transcribing", mp3_file_path)
            # Transcribe the MP3 recording
            transcription = transcribe_mp3(mp3_file_path)
            if transcription is None:
                print("Transcription is None. Skipping linguistic analysis.")
                continue

            print("Transcription:", transcription)

            # Segment the text into sentences
            sentences = segment_text(transcription)
            print("Sentences:", sentences)

            # Perform linguistic analysis
            for sentence in sentences:
                print("Linguistic analysis for sentence:", sentence)
                linguistic_analysis(sentence)


# Example usage for testing directory
if __name__ == "__main__":
    testing_directory = "/content/drive/MyDrive/Animals_Dataset/testing"
    process_directory(testing_directory)

# Example usage for training directory
if __name__ == "__main__":
    training_directory = "/content/drive/MyDrive/Animals_Dataset/training"
    process_directory(training_directory)

"""#Bi-LSTM"""

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Function to tokenize and preprocess the text
def preprocess_text(texts, max_words, max_sequence_length):
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    data = pad_sequences(sequences, maxlen=max_sequence_length)

    return data, word_index

# Modify your existing code to include this function for text preprocessing

from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout

def build_bilstm_model(max_words, embedding_dim, max_sequence_length, num_classes):
    model = Sequential()
    model.add(Embedding(max_words, embedding_dim, input_length=max_sequence_length))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.summary()

    return model

# Function to train the Bi-LSTM model
def train_bilstm_model(X_train, y_train, max_words, embedding_dim, max_sequence_length, num_classes, epochs=10, batch_size=32):
    model = build_bilstm_model(max_words, embedding_dim, max_sequence_length, num_classes)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    return model

from keras.utils import to_categorical
import numpy as np

# Modify process_directory to include preprocessing and training
def process_directory(directory):
    texts = []
    labels = []

    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_file_path = os.path.join(directory, filename)
            print("Transcribing", mp3_file_path)
            transcription = transcribe_mp3(mp3_file_path)
            if transcription is None:
                print("Transcription is None. Skipping.")
                continue

            # Append the transcription and label (extracted from filename) to the lists
            texts.append(transcription)
            # Assume the label is the animal name (you may need to modify this based on your dataset structure)
            label = filename.split('.')[0]
            labels.append(label)

    # Preprocess text data
    max_words = 10000
    max_sequence_length = 100
    X, word_index = preprocess_text(texts, max_words, max_sequence_length)

    # Convert labels to one-hot encoding
    label_to_id = {label: idx for idx, label in enumerate(np.unique(labels))}
    y = np.array([label_to_id[label] for label in labels])
    y = to_categorical(y)

    # Train the Bi-LSTM model
    embedding_dim = 100
    num_classes = len(np.unique(labels))
    model = train_bilstm_model(X, y, max_words, embedding_dim, max_sequence_length, num_classes)

    return model, word_index, label_to_id

# Example usage for training directory
if __name__ == "__main__":
    training_directory = "/content/drive/MyDrive/Animals_Dataset/training"
    trained_model, word_index, label_to_id = process_directory(training_directory)

# You can save the model and label mappings for later use
# trained_model.save("bilstm_model.h5")
# np.save("word_index.npy", word_index)
# np.save("label_to_id.npy", label_to_id)

"""#CNN

Data Preprocessing for CNN
Tokenization and Padding:
"""

# Function to preprocess the text for CNN
def preprocess_text_cnn(texts, max_words, max_sequence_length):
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    data = pad_sequences(sequences, maxlen=max_sequence_length)

    return data, word_index

# Modify your existing code to include this function for text preprocessing

"""Define the CNN Model:"""

from keras.layers import Conv1D, GlobalMaxPooling1D

def build_cnn_model(max_words, embedding_dim, max_sequence_length, num_classes):
    model = Sequential()
    model.add(Embedding(max_words, embedding_dim, input_length=max_sequence_length))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.summary()

    return model

# Function to train the CNN model
def train_cnn_model(X_train, y_train, max_words, embedding_dim, max_sequence_length, num_classes, epochs=10, batch_size=32):
    model = build_cnn_model(max_words, embedding_dim, max_sequence_length, num_classes)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    return model

import os
import numpy as np
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical

# Modify your existing code to include this function for audio preprocessing
def preprocess_audio(data):
    # Rescale the MFCC data between 0 and 1
    min_val = np.min(data)
    max_val = np.max(data)
    data = (data - min_val) / (max_val - min_val)
    return data

def build_cnn_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.summary()

    return model

# Function to train the CNN model
def train_cnn_model(X_train, y_train, input_shape, num_classes, epochs=10, batch_size=32):
    model = build_cnn_model(input_shape, num_classes)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    return model

# Modify process_directory to include MFCC extraction and preprocessing
# Modify process_directory to handle varying-length MFCC features and preprocess the data
def process_directory(directory, max_pad_len=174):
    data = []  # This should be populated with actual data
    labels = []

    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_file_path = os.path.join(directory, filename)
            print("Loading and extracting MFCC features from", mp3_file_path)

            # Load the audio file and extract MFCC features
            y, sr = librosa.load(mp3_file_path, sr=None)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)

            # Pad or truncate the MFCC features to a fixed length
            if mfcc.shape[1] < max_pad_len:
                pad_width = max_pad_len - mfcc.shape[1]
                mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
            else:
                mfcc = mfcc[:, :max_pad_len]

            data.append(mfcc)

            # Assume the label is the animal name (you may need to modify this based on your dataset structure)
            label = filename.split('.')[0]
            labels.append(label)

    # Convert labels to one-hot encoding
    label_to_id = {label: idx for idx, label in enumerate(np.unique(labels))}
    y = np.array([label_to_id[label] for label in labels])
    y = to_categorical(y)

    # Preprocess audio data
    data = np.array(data)
    data = preprocess_audio(data)

    return data, y, label_to_id

    # Convert labels to one-hot encoding
    label_to_id = {label: idx for idx, label in enumerate(np.unique(labels))}
    y = np.array([label_to_id[label] for label in labels])
    y = to_categorical(y)

    # Train the CNN model
    input_shape = data.shape[1:]  # Shape of a single input sample
    num_classes = len(np.unique(labels))
    model = train_cnn_model(data, y, input_shape, num_classes)

    return model, label_to_id

# Example usage for training directory
if __name__ == "__main__":
    training_directory = "/content/drive/MyDrive/Animals_Dataset/training"
    X_train, y_train, label_to_id = process_directory(training_directory)
    print("Shapes of loaded data:")
    print("X_train shape:", X_train.shape)
    print("y_train shape:", y_train.shape)
    print("Label to ID mapping:", label_to_id)

# You can save the model and label mappings for later use
# trained_model.save("cnn_model.h5")
# np.save("label_to_id.npy", label_to_id)

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Create the CNN model
def build_cnn_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.summary()

    return model

# Train the CNN model
def train_cnn_model(X_train, y_train, input_shape, num_classes, epochs=10, batch_size=32):
    model = build_cnn_model(input_shape, num_classes)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    return model
# Reshape the data for CNN input
X_train_cnn = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)

# Input shape for CNN based on MFCC shape
input_shape_cnn = X_train_cnn.shape[1:]  # (num_mfcc_features, num_frames, 1)

# Number of classes
num_classes = len(label_to_id)

# Train the CNN model
cnn_model = train_cnn_model(X_train_cnn, y_train, input_shape_cnn, num_classes, epochs=10, batch_size=32)

"""#Bi-LSTM-CNN"""

pip install SpeechRecognition

import os
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_mp3(mp3_file_path):
    try:
        # Load the MP3 audio file
        audio = AudioSegment.from_mp3(mp3_file_path)

        # Convert to WAV format
        wav_file = mp3_file_path.replace('.mp3', '.wav')
        audio.export(wav_file, format="wav")

        # Recognize speech using Google Web Speech API
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)

        transcription = recognizer.recognize_google(audio)
        return transcription

    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
        return None

    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))
        return None

    except Exception as e:
        print("An error occurred while processing the audio:", str(e))
        return None

# List of MP3 files to transcribe
mp3_files = [
    "/content/drive/MyDrive/Animals_Dataset/testing/Record (online-voice-recorder (Joined by Happy Scribe).mp3",
    "/content/drive/MyDrive/Animals_Dataset/testing/Record (online-voice-recorder.com) (3).mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/16mLRrfH.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/1TEWgS4j.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/6XHCJ0d9.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/CKUbAGwN.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/NbMgkZr8.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/Vi8DU62C.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/WNigy84H.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/eorHWiFO.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/jh9Gwbsy.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/oEx6R8NF.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/q87MwIW0.mp3",
    "/content/drive/MyDrive/Animals_Dataset/training/y7dRBV0X.mp3"
]

# Transcribe each MP3 file and print the transcription
for mp3_file in mp3_files:
    print("Transcribing", mp3_file)
    try:
        transcription = transcribe_mp3(mp3_file)
        if transcription:
            print("Transcription:", transcription)
        else:
            print("Transcription is None. Skipping.")
    except Exception as e:
        print("An error occurred while processing the audio:", str(e))
        print("Skipping this file.")

from keras.layers import Conv1D, MaxPooling1D, GlobalMaxPooling1D

def build_bilstm_cnn_model(max_words, embedding_dim, max_sequence_length, num_classes):
    model = Sequential()
    model.add(Embedding(max_words, embedding_dim, input_length=max_sequence_length))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(MaxPooling1D(5))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    model.summary()

    return model

def train_bilstm_cnn_model(X_train, y_train, max_words, embedding_dim, max_sequence_length, num_classes, epochs=10, batch_size=32):
    model = build_bilstm_cnn_model(max_words, embedding_dim, max_sequence_length, num_classes)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    return model


if __name__ == "__main__":
    training_directory = "/content/drive/MyDrive/Animals_Dataset/training"
    trained_model, word_index, label_to_id = process_directory(training_directory)