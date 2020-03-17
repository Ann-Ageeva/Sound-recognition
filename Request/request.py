import pyaudio
import wave
import requests

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5

RECORDS_COUNT = 1
while RECORDS_COUNT < 3:    
    WAVE_SAMPLE_FILENAME = 'Samples/sample_%s.wav' % RECORDS_COUNT

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_SAMPLE_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #this code block for test api
    if (RECORDS_COUNT % 2 == 0):
    #end
        files = {
            'sample1': open('Samples/sample_%s.wav' % (RECORDS_COUNT - 1), 'rb'), 
            'sample2': open('Samples/sample_%s.wav' % RECORDS_COUNT, 'rb')}
        response = requests.post('http://127.0.0.1:5000/', files = files)
        print(response.content)

    RECORDS_COUNT += 1