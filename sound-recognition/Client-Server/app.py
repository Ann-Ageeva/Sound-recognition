from flask import Flask, request, redirect, render_template
import os
import neural_network.UseModel as NeuralNetwork

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav'}
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
        path_to_file = os.path.join("neural_network", "samples")
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
            answer = 'Record contains drone sound!'
        elif (not answer1.base_answer and not answer2.base_answer):
            answer = 'Record doesn`t contains drone sound!'
        else:
            if (answer1.percent > answer2.percent):
                if (answer1.base_answer):
                    answer = 'Record contains drone sound!'
                else:
                    answer = 'Record doesn`t contains drone sound!'
            else:
                if (answer2.base_answer):
                    answer = 'Record contains drone sound!'
                else:
                    answer = 'Record doesn`t contains drone sound!'

        #remove files
        os.remove(path_to_file_sample1)
        os.remove(path_to_file_sample2)

        return answer
                
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)