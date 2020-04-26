from flask import Flask, request, redirect, render_template
import os
from werkzeug.utils import secure_filename
import Neural_Network.UseModel as NeuralNetwork

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
            
        sample1 = request.files['sample1']
        sample2 = request.files['sample2']
        # if user does not select file, browser also
        # submit an empty part without filename
        if sample1.filename == '' or sample2.filename == '':
            return redirect(request.url)
            
        if not allowed_file(sample1.filename) or not allowed_file(sample2.filename):
            return redirect(request.url)
    
        #create pathes
        path_to_file = os.path.join("neural-network", "samples")
        path_to_file_sample1 = os.path.join(path_to_file, sample1.filename)
        path_to_file_sample2 = os.path.join(path_to_file, sample2.filename)
        
        #saving
        sample1.save(path_to_file_sample1)
        sample2.save(path_to_file_sample2)

        #get answers from neural network
        answer1 = NeuralNetwork.GetAnswers(path_to_file_sample1)
        answer2 = NeuralNetwork.GetAnswers(path_to_file_sample2)     

        #base selecting logic
        if (answer1.base_answer and answer2.base_answer):
            answer = "Record contains drone sound! Percentage:" + str((answer1.percent + answer2.percent) / 2)
        elif (not answer1.base_answer and not answer2.base_answer):
            answer = "Record doesn`t contains drone sound! Percentage:" + str((answer1.percent + answer2.percent) / 2)
        else:
            if (answer1.percent > answer2.percent):
                if (answer1.base_answer):
                    answer = "Record contains drone sound! Percentage:" + str(answer1.percent)
                else:
                    answer = "Record doesn`t contains drone sound! Percentage:" + str(answer1.percent)
            else:
                if (answer2.base_answer):
                    answer = "Record contains drone sound! Percentage:" + str(answer2.percent)
                else:
                    answer = "Record doesn`t contains drone sound! Percentage:" + str(answer2.percent)

        #remove files
        os.remove(path_to_file_sample1)
        os.remove(path_to_file_sample2)

        return answer
                
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)