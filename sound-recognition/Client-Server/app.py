from flask import Flask, request, redirect, render_template
import os
import algorithms.UseModel as NeuralNetwork
import algorithms.CalculateAngle as CalculateAngle
from multiprocessing import Process, Value, Array

app = Flask(__name__)

BASE_PATH_TO_SAMPLES = os.path.join("algorithms", "samples")

ALLOWED_EXTENSIONS = {'wav'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validateFiles(sample1, sample2):
    # if user does not select file, browser also
    # submit an empty part without filename
    if sample1.filename == '' or sample2.filename == '':
        return False
            
    if not allowed_file(sample1.filename) or not allowed_file(sample2.filename): 
        return False

    return True

def createPath(sample):
    return  os.path.join(BASE_PATH_TO_SAMPLES, sample.filename)

def getAnswer(answer1, answer2, path_to_sample1, path_to_sample2):
    if (answer1.base_answer and answer2.base_answer):
        angle = CalculateAngle.Calculate(path_to_sample1, path_to_sample2)
        return 'Record contains drone sound! Angel:' + str(angle[0])
    elif (not answer1.base_answer and not answer2.base_answer):
        angle = CalculateAngle.Calculate(path_to_sample1, path_to_sample2)            
        return 'Record doesn`t contains drone sound! Angel:' + str(angle[0])
    else:
        if (answer1.percent > answer2.percent):
            if (answer1.base_answer):
                angle = CalculateAngle.Calculate(path_to_sample1, path_to_sample2)
                return 'Record contains drone sound! Angel:' + str(angle[0])
            else:
                return 'Record doesn`t contains drone sound!'
        else:
            if (answer2.base_answer):
                angle = CalculateAngle.Calculate(path_to_sample1, path_to_sample2)
                return 'Record contains drone sound Angel:' + str(angle[0])
            else:
                return 'Record doesn`t contains drone sound!'    

def removeFiles(path_to_file1, path_to_file2):
    os.remove(path_to_file1)
    os.remove(path_to_file2)    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        sample1 = request.files['sample1']
        sample2 = request.files['sample2']

        if not validateFiles(sample1, sample2):
            return redirect(request.url)

        #create pathes
        path_to_sample1 = createPath(sample1)
        path_to_sample2 = createPath(sample2)

        #saving
        sample1.save(path_to_sample1)
        sample2.save(path_to_sample2)

        #get answers from neural network
        answer1 = NeuralNetwork.GetAnswers(path_to_sample1)
        answer2 = NeuralNetwork.GetAnswers(path_to_sample2)

        #base selecting logic
        answer = getAnswer(answer1, answer2, path_to_sample1, path_to_sample2)

        #remove files
        removeFiles(path_to_sample1, path_to_sample2)

        return answer
                
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)