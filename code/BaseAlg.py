import math as m

import numpy as np
from numpy.fft import rfft

import matplotlib.pyplot as plt
import librosa.display


import librosa


def test():

    speed = 330  # Скорость звука
    frequency = 44100  # Частота дискретизации
    dist = 1  # Расстояние между микрофонами
    maxRangeCor = int(dist / speed * frequency + 100)  # Диапозон маскимальной корреляции

    pathFirstMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\detect\\right side about 20 degree\\mic 1 - 01 (Left).wav'
    pathSecondMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\detect\\right side about 20 degree\\mic 1 - 02 (Right).wav'

    angles = baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro)

    return angles == 20

def baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro):
    angles = list()
    difDistValue=(difDist(maxRangeCor, frequency, pathFirstMicro, pathSecondMicro) * speed) / (frequency * dist)


    if difDistValue > 0:
        angles.append(m.degrees(m.acos(difDistValue)))
        angles.append(
            360 - m.degrees(m.acos(difDistValue))
        )

    angles.append(180 - m.degrees(m.acos(difDistValue)))
    angles.append(180 + m.degrees(m.acos(difDistValue)))

    return angles


def difDist(maxRangeCor, frequency, pathFirstMicro, pathSecondMicro):
    leftSignal, sr = librosa.load(pathFirstMicro, sr=frequency)
    rightSignal, sr = librosa.load(pathSecondMicro, sr=frequency)
    size = rightSignal.size
    best = 0
    dist = 0


    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[i:size], rightSignal[0:size - i])[0][1]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[0:size - i], rightSignal[i:size])[0][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


angles = test()
