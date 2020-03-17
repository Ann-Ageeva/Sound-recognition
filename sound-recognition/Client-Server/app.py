from flask import Flask, redirect, render_template, request

ALLOWED_EXTENSIONS = {"wav"}

app = Flask(__name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        sample1 = request.files["sample1"]
        sample2 = request.files["sample2"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if sample1.filename == "" or sample2.filename == "":
            return redirect(request.url)

        if not allowed_file(sample1.filename) or not allowed_file(sample2.filename):
            return redirect(request.url)

        # Some code of neural network
        if True:
            return "Yes, it`s a quadcopter"

        return "No, it`s not a quadcopter"

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
