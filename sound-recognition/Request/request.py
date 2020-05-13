import pyaudio
import wave
import requests
import uuid
import os
import threading
from threading import Thread
import time
import aiohttp
import asyncio
import json

os_lock = threading.Lock()
wf_lock = threading.Lock()
stream_lock = threading.Lock()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5
DEVICE_INDEX_1 = 1
DEVICE_INDEX_2 = 2
p = pyaudio.PyAudio()

URL = 'http://127.0.0.1:5000/'

#code for showing micro index
#for ii in range(p.get_device_count()):
#     print(p.get_device_info_by_index(ii).get('name'))

def CreateWAW(FILENAME, frames):
    wf_lock.acquire()
    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    wf_lock.release()
   
def Recording(DEVICE_INDEX, FILENAME, threadName):
    print("p3.2", threadName)
    stream_lock.acquire()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)
    stream_lock.release()          
    print("p3.3", threadName)
    frames = []
    
    #print("* recording form %s device" % p.get_device_info_by_host_api_device_index(0, DEVICE_INDEX).get('name'))
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("p3.4", threadName)
    #print("* done recording form %s device" % p.get_device_info_by_host_api_device_index(0, DEVICE_INDEX).get('name'))

    stream_lock.acquire()
    stream.stop_stream()
    stream.close()
    p.terminate()
    stream_lock.release()  
    print("p3.5", threadName)

    CreateWAW(FILENAME, frames)

def getRecords():
    print("p1")
    FILENAME_Sample1 = 'Samples/sample_%s.wav' % uuid.uuid4()
    FILENAME_Sample2 = 'Samples/sample_%s.wav' % uuid.uuid4()
    thread1 = Thread(target=Recording, args=(DEVICE_INDEX_1, FILENAME_Sample1, "thread1"), daemon=True)
    thread2 = Thread(target=Recording, args=(DEVICE_INDEX_2, FILENAME_Sample2, "thread2"), daemon=True)
    print("p2")
    
    thread1.start()
    thread2.start()
    print("p3")
    thread2.join()
    thread1.join()
    print("p4")
    return {
        'sample1': FILENAME_Sample1, 
        'sample2': FILENAME_Sample2
    }

async def getResponse(session, FILENAME_Sample1, FILENAME_Sample2):
    async with session.post(URL, data={
        'sample1': open(FILENAME_Sample1, 'rb'), 
        'sample2': open(FILENAME_Sample2, 'rb')       
    }) as response:
        await response.text()
        print("ready!")
         
async def sendFiles(FILENAME_Sample1, FILENAME_Sample2):
    print('p5')
    async with aiohttp.ClientSession() as session:
        data = await getResponse(session, FILENAME_Sample1, FILENAME_Sample2)
        print (data)
    time.sleep(10) 
    print('p6')

def sendFilesThread(FILENAME_Sample1, FILENAME_Sample2):
    print("send...")
    response = requests.post(URL, files={
            'sample1': open(FILENAME_Sample1, 'rb'), 
            'sample2': open(FILENAME_Sample2, 'rb')
        })
    print("send end")
    Thread(target=removeFiles, args=(FILENAME_Sample1, FILENAME_Sample2), daemon=True).start()
    print("after new thread")
    print(response.content)

def removeFiles(FILENAME_Sample1, FILENAME_Sample2):
    print ("start removing")
    os_lock.acquire()
    print ("in lock")
    os.remove(FILENAME_Sample1)
    print ("in lock2")
    os.remove(FILENAME_Sample2)
    os_lock.release() 
    print ("end removing") 

def main():
    #while True:
    #for i in range(2):
    files = getRecords()

    #async with aiohttp.ClientSession() as session:
    #    await getResponse(session, files['sample1'], files['sample2'])

    Thread(target=sendFilesThread, args=(files['sample1'], files['sample2']), daemon=True).start()
    #await sendFiles(files['sample1'], files['sample2'])    
    #time.sleep(1000)

if __name__ == '__main__':
    main()