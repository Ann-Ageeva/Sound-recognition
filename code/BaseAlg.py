import math as m

import numpy as np
from numpy.fft import rfft

import matplotlib.pyplot as plt
import librosa.display


import librosa


def test():

    maxRangeCor = 1000  # Диапозон маскимальной корреляции
    speed = 330  # Скорость звука
    frequency = 22000  # Частота дискретизации
    dist = 100  # Расстояние между микрофонами

    pathFirstMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\drone detect\\192 khz_ 64-bit\\test 1 - 01 (Left).wav'
    pathSecondMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\drone detect\\192 khz_ 64-bit\\test 1 - 02 (Right).wav'

    angles = baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro)

    return angles == 20

def baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro):
    angles = list()
    difDistValue=difDist(maxRangeCor, pathFirstMicro, pathSecondMicro)

    if difDistValue > 0:
        angles.append(m.degrees(m.cos(difDistValue)))
        angles.append(
            360 - m.degrees(m.cos(difDistValue))
        )

    angles.append(180 - m.degrees(m.cos(difDistValue)))
    angles.append(180 + m.degrees(m.cos(difDistValue)))

    return angles


def difDist(l, pathFirstMicro, pathSecondMicro):
    leftSignal, sr = librosa.load(pathFirstMicro, sr=None)
    rightSignal, sr = librosa.load(pathSecondMicro, sr=None)
    size = leftSignal.size
    best = 0
    dist = 0

    """plt.figure(figsize=(14, 5))
    librosa.display.waveplot(rightSignal, sr=sr)
    plt.show()
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(leftSignal, sr=sr)
    plt.show()"""

    for i in range(0, l):
        corrCoeff = np.corrcoef(leftSignal[i:size], rightSignal[0:size - i])[0][1]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(0, l):
        corrCoeff = np.corrcoef(leftSignal[0:size - i], rightSignal[i:size])[0][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


angles = test()
