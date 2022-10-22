from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('clientInformation.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/test')
def test():
    return render_template('framework.html')

