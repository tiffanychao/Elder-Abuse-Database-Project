from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/client_information')
def client_information():
    return render_template('clientInformation.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/center_outcomes')
def center_outcomes():
    return render_template("centerOutcomes.html")

@app.route('/test', methods =["GET", "POST"])
def get_abuser_info_from_db():
    # size 10
    Dic = dict()
    Dic["referCaseNum"] = "12345"
    Dic["firstName"] = "Jorge"
    Dic["lastName"] = "Sole"
    Dic["FCTeamMember"] = "APS"
    Dic["fcTeamOther"] = ""
    Dic["email"] = "jsole@hs.uci.edu"
    Dic["officePhone"] = "(714)456-8586"
    Dic["officeTax"] = "(714)456-7933"
    Dic["mobilePhone"] = ""
    Dic["supervisorName"] = "Jacklyn Schult"
 
    return Dic

@app.route('/referring_agency',methods =["GET", "POST"])
def referring_agency():
    if request.method == "POST":
        data = request.form.get("ReferCaseNum")
        print(data)
    dictInfo = get_abuser_info_from_db()
    return render_template('referringAgency.html', **dictInfo)

@app.route('/')
def homepage():
    return render_template('homepage.html')




@app.route('/example')
def example():
    variable = "check your name"
    return render_template('example.html', value = variable)

@app.route('/narrative')
def narrative():
    variable = "check your name"
    return render_template('narrative.html', value = variable)



@app.route('/consulation')
def consulation():
    variable = "check your name"
    return render_template('consulation.html', value = variable)

