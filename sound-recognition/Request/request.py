import pyaudio
import wave
import requests
import uuid
import os
import threading
from threading import Thread

os_lock = threading.Lock()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5
DEVICE_INDEX_1 = 1
DEVICE_INDEX_2 = 2
p = pyaudio.PyAudio()

URL = "http://127.0.0.1:5000/"

# code for showing micro index
# for ii in range(p.get_device_count()):
#     print(p.get_device_info_by_index(ii).get('name'))


def CreateWAW(FILENAME, frames):
    wf = wave.open(FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


def getStream(DEVICE_INDEX):
    return p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=DEVICE_INDEX,
    )


def getFileName():
    return "Samples/sample_%s.wav" % uuid.uuid4()


def getRecords():

    p1 = pyaudio.PyAudio()
    p2 = pyaudio.PyAudio()

    stream1 = getStream(DEVICE_INDEX_1)
    stream2 = getStream(DEVICE_INDEX_2)

    frames1 = []
    frames2 = []

    print("*recording...")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data1 = stream1.read(CHUNK)
        data2 = stream2.read(CHUNK)
        frames1.append(data1)
        frames2.append(data2)

    print("*end recording")

    stream1.stop_stream()
    stream2.stop_stream()

    stream1.close()
    stream2.close()

    p1.terminate()
    p2.terminate()

    FILENAME_Sample1 = getFileName()
    FILENAME_Sample2 = getFileName()

    CreateWAW(FILENAME_Sample1, frames1)
    CreateWAW(FILENAME_Sample2, frames2)

    return {"sample1": FILENAME_Sample1, "sample2": FILENAME_Sample2}


def sendFilesThread(FILENAME_Sample1, FILENAME_Sample2):
    print("send...")
    response = requests.post(
        URL,
        files={
            "sample1": open(FILENAME_Sample1, "rb"),
            "sample2": open(FILENAME_Sample2, "rb"),
        },
    )
    removeFiles(FILENAME_Sample1, FILENAME_Sample2)
    print(response.content)


def removeFiles(FILENAME_Sample1, FILENAME_Sample2):
    os_lock.acquire()
    os.remove(FILENAME_Sample1)
    os.remove(FILENAME_Sample2)
    os_lock.release()


def main():
    while True:
        files = getRecords()

        Thread(
            target=sendFilesThread,
            args=(files["sample1"], files["sample2"]),
            daemon=True,
        ).start()


if __name__ == "__main__":
    main()
