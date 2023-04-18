import os
import numpy as np
from music21 import converter, instrument, note, chord, stream
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation
from keras.utils import np_utils

# Define the directory where the MIDI files are located
midi_dir = 'C:/Mandil/data'


# Set the sequence length (number of notes/chords per input sequence)
sequence_length = 100

# Load the MIDI files and extract the notes and chords
notes = []
for file in os.listdir(midi_dir):
    if file.endswith('.mid'):
        midi = converter.parse(os.path.join(midi_dir, file))
        notes_to_parse = None
        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

# Create a dictionary to map notes and chords to integers
note_to_int = dict((note, i) for i, note in enumerate(sorted(set(notes))))

# Create input sequences and corresponding output labels
X = []
y = []
for i in range(0, len(notes) - sequence_length, 1):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]
    X.append([note_to_int[note] for note in sequence_in])
    y.append(note_to_int[sequence_out])

# Reshape the input sequences to fit the LSTM input shape
X = np.reshape(X, (len(X), sequence_length, 1))

# Normalize the input sequences
X = X / float(len(set(notes)))

# Convert the output labels to one-hot encoding
y = np_utils.to_categorical(y)

# Define the LSTM model architecture
model = Sequential()
model.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512))
model.add(Dropout(0.3))
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(len(set(notes))))
model.add(Activation('softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model
model.fit(X, y, epochs=50, batch_size=128)
