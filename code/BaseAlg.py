import math as m

import numpy as np
from numpy.fft import rfft

import librosa


def test():

    maxRangeCor = 10000  # Диапозон маскимальной корреляции
    speed = 330  # Скорость звука
    frequency = 22000  # Частота дискретизации
    dist = 100  # Расстояние между микрофонами

    pathFirstMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\detect\\right side about 20 degree\\mic 1 - 01 (Left).wav'
    pathSecondMicro = 'C:\\Users\\wwwvn\\Desktop\\тест\\detect\\right side about 20 degree\\mic 1 - 02 (Right).wav'

    angles = baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro)

    return angles == 20

def baseAlg(maxRangeCor, speed, frequency, dist, pathFirstMicro, pathSecondMicro):
    angles = list()

    if difDist(maxRangeCor, pathFirstMicro, pathSecondMicro) > 0:
        angles.append(m.degrees(m.cos(difDist(maxRangeCor, pathFirstMicro, pathSecondMicro) * speed / (frequency * dist))))
        angles.append(
            360 - m.degrees(m.cos(difDist(maxRangeCor, pathFirstMicro, pathSecondMicro) * speed / (frequency * dist)))
        )

    angles.append(180 - m.degrees(m.cos(difDist(maxRangeCor, pathFirstMicro, pathSecondMicro) * speed / (frequency * dist))))
    angles.append(180 + m.degrees(m.cos(difDist(maxRangeCor, pathFirstMicro, pathSecondMicro) * speed / (frequency * dist))))

    return angles


def difDist(l, pathFirstMicro, pathSecondMicro):
    leftSignalFurie, sr = librosa.load(pathFirstMicro, sr=10000)
    X = rfft(leftSignalFurie)
    rightSignalFurie, sr = librosa.load(pathSecondMicro, sr=10000)
    y = rfft(rightSignalFurie)
    corrCoeff = np.corrcoef(X, y)
    best = 0
    dist = 0

    for i in range(0, l):
        VAL = np.vstack((leftSignalFurie, rightSignalFurie))
        corrCoeff= np.corrcoef(leftSignalFurie, rightSignalFurie)
        corrCoeff = np.corrcoef(leftSignalFurie[i:l + i], rightSignalFurie[0:l])[0][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(0, l):
        corrCoeff = np.corrcoef(leftSignalFurie[0:l], rightSignalFurie[i: l + i])[0][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


angles = test()
