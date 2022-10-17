from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    variable = "check your name"
    return render_template('example.html', value = variable)
