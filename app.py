from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/client_information')
def client_information():
    return render_template('clientInformation.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/example')
def example():
    variable = "check your name"
    return render_template('example.html', value = variable)

