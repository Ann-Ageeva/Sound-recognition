import math as m

import librosa
import numpy
from numpy.fft import rfft

pathFirstMicro = ""
pathSecondMicro = ""


def baseAlg():
    maxRangeCor = 5500  # Диапозон маскимальной корреляции
    u = 330  # Скорость звука
    frequency = 22000  # Частота дискретизации
    dist = 100  # Расстояние между микрофонами

    angles = list()

    if difDist(maxRangeCor) > 0:
        angles.append(m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))
        angles.append(
            360 - m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist))
        )

    angles.append(180 - m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))
    angles.append(180 + m.degrees.cos(difDist(maxRangeCor) * u / (frequency * dist)))

    return angles


def difDist(maxRange):
    x, sr = librosa.load(pathFirstMicro)
    leftSignalFurie = rfft(x)
    x, sr = librosa.load(pathSecondMicro)
    rightSignalFurie = rfft(x)
    best = 0
    dist = 0

    for i in range(1, maxRange):
        corrCoeff = numpy.corrcoef(
            leftSignalFurie(i, maxRange + i), rightSignalFurie(0, maxRange)
        )[0, 1]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(1, maxRange):
        corrCoeff = numpy.corrcoef(
            leftSignalFurie(0, maxRange), rightSignalFurie(i, maxRange + i)
        )[0, 1]
        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


angles = baseAlg()
