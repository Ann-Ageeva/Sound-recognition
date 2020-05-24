import math as m
import numpy as np
import librosa

maxRangeCor = 1000  #Max correlation range
speed = 330  #Sound speed
frequency = 22000  #Sampling frequency
dist = 100  #Distance between micros

def baseAlg(pathFirstMicro, pathSecondMicro):
    angles = list()
    difDistValue=difDist(pathFirstMicro, pathSecondMicro)

    if difDistValue > 0:
        angles.append(m.degrees(m.cos(difDistValue)))
        angles.append(360 - m.degrees(m.cos(difDistValue)))

    angles.append(180 - m.degrees(m.cos(difDistValue)))
    angles.append(180 + m.degrees(m.cos(difDistValue)))

    return angles

def difDist(pathFirstMicro, pathSecondMicro):
    leftSignal, sr = librosa.load(pathFirstMicro, sr=48000)
    rightSignal, sr = librosa.load(pathSecondMicro, sr=48000)

    sizeleft = leftSignal.size
    sizeright = rightSignal.size
    best = 0
    dist = 0

    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[i:sizeleft], rightSignal[0:sizeright - i])[0][1]
        if corrCoeff > best:
            best = corrCoeff
            dist = i

    for i in range(0, maxRangeCor):
        corrCoeff = np.corrcoef(leftSignal[0:sizeleft - i], rightSignal[i:sizeright])[0][1]

        if corrCoeff > best:
            best = corrCoeff
            dist = -1 * i

    return dist

def Calculate(pathFirstMicro, pathSecondMicro):
    angles = baseAlg(pathFirstMicro, pathSecondMicro)
    return angles