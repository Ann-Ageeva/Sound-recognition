# feature extractoring and preprocessing data
import librosa
import numpy as np
import os
import pickle 
from keras import models

# Получаем предобработчик модели
with open('scaler.pickle', 'rb') as f:
    scaler = pickle.load(f)
# Загрузка модели
model = models.load_model('CNN.h5')

# Извлечение фич 
def GetFeatures(songname):
    y, sr = librosa.load(songname, mono=True, duration=30)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    to_append = f'{np.mean(chroma_stft)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'   
    
    SoundArr = np.array(to_append.split())
    return SoundArr

# Получаем предсказание
def GetAnswer(SoundFeatures):
    # Предобрабатываем данные
    SoundArr_transformed = scaler.transform(SoundFeatures.reshape(1, -1))
    # Получаем прогноз
    predict = model.predict(SoundArr_transformed)
    if np.argmax(predict[0]) == 1:
        print("дрон, с вероятностью:",predict[0][1]*100, "%")
    elif np.argmax(predict[0]) == 0:
        print("не дрон, с вероятностью:",predict[0][0]*100, "%")

# Получаем предсказание для каждой записи
def GetAnswers(directory):
    for filename in os.listdir(f'{directory}'):
        songname = f'{directory}/{filename}'
        Features = GetFeatures(songname)
        print(f'На записи {songname}', end = " ")
        GetAnswer(Features)

GetAnswers('Test')