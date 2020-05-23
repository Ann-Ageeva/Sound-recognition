import librosa
import numpy as np
import os
import pickle 
from keras import models, backend
import tensorflow as tf


# Get model handler
with open('neural_network\\scaler.pickle', 'rb') as f:
    scaler = pickle.load(f)

# Model download
session = tf.Session(graph=tf.Graph())
with session.graph.as_default():
    backend.set_session(session)
    model = models.load_model('neural_network\\CNN.h5')

# Feature extraction 
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

# Get prediction
def GetAnswer(SoundFeatures):
    # Preparing data
    SoundArr_transformed = scaler.transform(SoundFeatures.reshape(1, -1))
    # Get prediction
    with session.graph.as_default():
        backend.set_session(session)
        predict = model.predict(SoundArr_transformed)

    if np.argmax(predict[0]) == 1:
        return answer(True, predict[0][1]*100)
    elif np.argmax(predict[0]) == 0:
        return answer(False, predict[0][1]*100)  

# Get prediction for each sample
def GetAnswers(songname):
    Features = GetFeatures(songname)
    return GetAnswer(Features)

class answer(object):
    def __init__(self, base_answer, percent):
        self.base_answer = base_answer
        self.percent = percent