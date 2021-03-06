import csv
import os
import pathlib
import pickle
import warnings

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings("ignore")
cmap = plt.get_cmap("inferno")


plt.figure(figsize=(10, 10))
classes = "Yes_Drone No_Drone".split()
for i in classes:
    pathlib.Path(f"img_data/{i}").mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(f"{i}"):
        songname = f"{i}/{filename}"
        y, sr = librosa.load(songname, mono=True, duration=5)
        plt.specgram(
            y,
            NFFT=2048,
            Fs=2,
            Fc=0,
            noverlap=128,
            cmap=cmap,
            sides="default",
            mode="default",
            scale="dB",
        )
        plt.axis("off")
        plt.savefig(f'img_data/{i}/{filename[:-3].replace(".", "")}.png')
        plt.clf()

header = "filename chroma_stft spectral_centroid spectral_bandwidth rolloff zero_crossing_rate"
header += " label"
header = header.split()

file = open("data.csv", "w", newline="")
with file:
    writer = csv.writer(file)
    writer.writerow(header)
classes = "Yes_Drone No_Drone".split()
for i in classes:
    for filename in os.listdir(f"{i}"):
        songname = f"{i}/{filename}"
        y, sr = librosa.load(songname, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        to_append = f"{filename} {np.mean(chroma_stft)} {np.mean(spec_cent)} \
            {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}"
        to_append += f" {i}"
        file = open("data.csv", "a", newline="")
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())
data = pd.read_csv("data.csv")
data.head()
# Dropping unneccesary columns
data = data.drop(["filename"], axis=1)

label_list = data.iloc[:, -1]
encoder = LabelEncoder()
y = encoder.fit_transform(label_list)

scaler = StandardScaler()
X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype=float))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = models.Sequential()
model.add(layers.Dense(256, activation="relu", input_shape=(X_train.shape[1],)))

model.add(layers.Dense(128, activation="relu"))

model.add(layers.Dense(64, activation="relu"))

model.add(layers.Dense(2, activation="softmax"))

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

history = model.fit(X_train, y_train, epochs=20, batch_size=128)

test_loss, test_acc = model.evaluate(X_test, y_test)

print("test_loss: ", test_loss)
print("test_acc: ", test_acc)

x_val = X_train[:200]
partial_x_train = X_train[200:]

y_val = y_train[:200]
partial_y_train = y_train[200:]

model = models.Sequential()
model.add(layers.Dense(512, activation="relu", input_shape=(X_train.shape[1],)))
model.add(layers.Dense(256, activation="relu"))
model.add(layers.Dense(128, activation="relu"))
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(2, activation="softmax"))

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

model.fit(
    partial_x_train,
    partial_y_train,
    epochs=30,
    batch_size=512,
    validation_data=(x_val, y_val),
)
results = model.evaluate(X_test, y_test)


with open("scaler.pickle", "wb") as f:
    pickle.dump(scaler, f)

model.save("CNN.h5")
