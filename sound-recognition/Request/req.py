import requests
files = {
    'sample1': open('Samples/sample_02133277-0dc6-4b34-8a14-17a980c3307c.wav', 'rb'), 
    'sample2': open('Samples/sample_63398534-adb8-4640-9645-e5e78290870e.wav', 'rb')}
response = requests.post('http://127.0.0.1:5000/', files = files)