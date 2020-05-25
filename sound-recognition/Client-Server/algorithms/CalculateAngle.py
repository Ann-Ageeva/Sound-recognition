import math as m

import librosa
import numpy as np

speed = 330  # Sound speed
frequency = 44100  # Sampling frequency
dist = 1  # Distance between micros
maxRangeCor = int(dist / speed * frequency + 100)  # Max correlation range


def difDist(pathFirstMicro, pathSecondMicro):
    leftSignal, sr = librosa.load(pathFirstMicro, sr=frequency)
    rightSignal, sr = librosa.load(pathSecondMicro, sr=frequency)
    sizeleft = leftSignal.size
    sizeright = rightSignal.size
    best = 0
    dist = 0

    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[i:sizeleft], rightSignal[0 : sizeright - i])[
            0
        ][1]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[0 : sizeleft - i], rightSignal[i:sizeright])[
            0
        ][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist


def baseAlg(pathFirstMicro, pathSecondMicro):
    angles = list()
    difDistValue = (difDist(pathFirstMicro, pathSecondMicro) * speed) / (
        frequency * dist
    )

    if difDistValue > 0:
        angles.append(m.degrees(m.acos(difDistValue)))
        angles.append(360 - m.degrees(m.acos(difDistValue)))

    angles.append(180 - m.degrees(m.acos(difDistValue)))
    angles.append(180 + m.degrees(m.acos(difDistValue)))

    return angles


def Calculate(pathFirstMicro, pathSecondMicro):
    angles = baseAlg(pathFirstMicro, pathSecondMicro)
    return angles
