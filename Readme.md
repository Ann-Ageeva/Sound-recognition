# Setup

```
# You must be in Terminal (and you must select 1: cmd)
# If you don`t have enviroment area:
conda create -n sound-recog -f environment.yml
conda activate sound-recog
# go to folder which contains python file

# start server:
python app.py

# client part for recording wav files and sending it to server
python request.py

# if you need update sound-recog, enviroment area sound-recog must be activate
#conda install -c conda-forge NAME_PACK

# if you need check sound-recog
#conda list -n sound-recog

# if you need update yml file
#conda deactivate
#conda env update -f=environment.yml
```
