from scipy.stats.stats import pearsonr
from scipy.stats import linregress
import os
import numpy 
from numpy.fft import rfft, rfftfreq
import librosa
import matplotlib.pyplot as plt
import librosa.display

directory = 'C:/Users/BigDDY/Desktop/Test'
files = os.listdir(directory)

discr = list()
furie_list = list()

for file in range(0, len(files)):
    x, sr = librosa.load('C:/Users/BigDDY/Desktop/Test/' + str(files[file]))
    discr.append(x)
    
for file in range(0, len(discr)):
    furie = rfft(discr[file])
    furie_list.append(furie)

x, sr = librosa.load('C:/Users/BigDDY/Desktop/File/1.wav')
sample_furie = rfft(x)

def FindBestCor(sample, listOfFurie):
    best = numpy.corrcoef(sample, listOfFurie[0])[0,1]
    indexOfBest = 0
    
    for i in range(1, len(listOfFurie)):
        corrCoeff = numpy.corrcoef(sample, listOfFurie[i])[0,1]
        if corrCoeff > best:
            best = corrCoeff
            indexOfBest = i
    return best
    
bestCor = FindBestCor(sample_furie, furie_list)

print(bestCor)