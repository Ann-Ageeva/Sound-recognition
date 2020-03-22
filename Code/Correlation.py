import os
import numpy 
import librosa
import matplotlib.pyplot as plt
import librosa.display
from numpy.fft import rfft, rfftfreq

def FindBestCor(sample, listOfFurie):
    best = abs(numpy.corrcoef(sample, listOfFurie[0])[0,1])
    
    for i in range(1, len(listOfFurie)):
        corrCoeff = abs(numpy.corrcoef(sample, listOfFurie[i])[0,1])
        if corrCoeff > best:
            best = corrCoeff
    return best

def MakeEqual(files):
    min = len(files[0])
    
    for file in range(1, len(files)):
        if len(files[file]) < min:
            min = len(files[file])
            
    for file in range(0, len(files)):
        if len(files[file]) > min:
            files[file] = files[file][len(files[file]) - min : ]

directory  = 'C:/Users/BigDDY/Desktop/Repos/Sound-recognition/Code/Test'
files      = os.listdir(directory)

discr      = list()
furie_list = list()

for file in range(0, len(files)):
    x, sr = librosa.load('C:/Users/BigDDY/Desktop/Repos/Sound-recognition/Code/Test/' + str(files[file]))
    discr.append(x)

MakeEqual(discr)
for file in range(0, len(discr)):
    furie = rfft(discr[file])
    furie_list.append(furie)

x, sr        = librosa.load('C:/Users/BigDDY/Desktop/Repos/Sound-recognition/Code/File/1.wav')
sample_furie = rfft(x)
sample_furie = sample_furie[len(sample_furie) - len(furie_list[0]) : len(sample_furie)]

Best = FindBestCor(sample_furie, furie_list)

print(Best)