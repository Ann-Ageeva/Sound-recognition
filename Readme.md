# Setup

```
conda env create -f environment.yml
conda activate sound-recog

# start server for receiving wav files
python app.py

# client part for recording wav files and sending it to server
python request.py
```
