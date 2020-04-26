import numpy
import librosa
import math as m
from numpy.fft import rfft

pathNorthMicro = ""
pathSouthMicro = ""
pathWestMicro = ""
pathEastMicro = ""


def myAlg():
    horizontAngles = baseAlg(pathWestMicro, pathEastMicro)

    verticalAngles = baseAlg(pathNorthMicro, pathSouthMicro) - 90

    for i in range(0, 1):
        if verticalAngles[i] < 0:
            verticalAngles[i] += 360

    best = 360
    hInd = 0
    vInd = 0

    for i in range(0, 1):
        for j in range(0, 1):
            if horizontAngles[i] - verticalAngles[j] < best:
                best = horizontAngles[i] - verticalAngles[j]
                hInd = i
                vInd = j

    return (horizontAngles[hInd] + verticalAngles[vInd]) / 2


def baseAlg(fistPath, secondPath):
    maxRangeCor = 5500  # Диапозон маскимальной корреляции
    speed = 330  # Скорость звука
    freq = 22000  # Частота дискретизации
    dist = 100  # Расстояние между микрофонами

    difDist = offsetReference(maxRangeCor, fistPath, secondPath) * speed / (2 * freq)
    angles = []

    if difDist > 0:
        angles.append(m.degrees.cos(difDist / dist))
        angles.append(360 - m.degrees.cos(difDist / dist))

    angles.append(180 - m.degrees.cos(difDist / dist))
    angles.append(180 + m.degrees.cos(difDist / dist))

    return angles


def offsetReference(maxRange, fistPath, secondPath):
    x, sr = librosa.load(fistPath)
    firstSignalFurie = rfft(x)
    x, sr = librosa.load(secondPath)
    secondSignalFurie = rfft(x)
    best = 0
    offset = 0

    for i in range(0, maxRange):
        corrCoeff = numpy.corrcoef(secondSignalFurie(i, maxRange + i), firstSignalFurie(0, maxRange))[0, 1]
        if corrCoeff > best:
            best = corrCoeff
            offset = i

    for i in range(0, maxRange):
        corrCoeff = numpy.corrcoef(firstSignalFurie(0, maxRange), secondSignalFurie(i, maxRange + i))[0, 1]
        if corrCoeff > best:
            best = corrCoeff
            offset = -1 * i

    return offset
