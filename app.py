from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/client')
def client():
    return render_template('client.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/client_information')
def client_information():
    return render_template('clientInformation.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/abuser')
def abuser():
    return render_template('abuser.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

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
        data1 = request.form.get("ReferCaseNum")
        data2 = request.form.get("firstName")
        print(data1 + data2)
        return  data1 
    dictInfo = get_abuser_info_from_db()
    return render_template('referringAgency.html', **dictInfo)

@app.route('/case_summary',methods =["GET", "POST"])
def case_summary():
    if request.method == "POST":
       
        return  data1 
    # deal with the data
    #
    v_name = "John Doe"
    v_notes = "In the early 19th century,<br> the Bennet family live at their Longbourn estate,<br> situated near the village of Meryton in Hertfordshire, <br>England. Mrs. Bennet's greatest desire is to marry off her five daughters in order to secure their futures. The arrival of Mr. Bingley, a rich bachelor who rents the neighbouring Netherfield estate, gives her hope that one of her daughters might contract an advantageous marriage, because It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife."
    v_goal = "Mr. Collins, the heir to the Longbourn estate, visits the Bennet family with the intention of finding a wife among the five girls under the advice of his patroness Lady Catherine de Bourgh, also revealed to be Mr. Darcy's aunt. He decides to pursue Elizabeth. The Bennet family meet the charming army officer George Wickham, <br>who tells Elizabeth in confidence Mr. Darcy's horrible past actions in his regards. Elizabeth, blinded by her prejudice toward Mr. Darcy, believes him."
    v_rcmd = "Elizabeth dances with Mr. Darcy at a ball, where Mrs. Bennet hints loudly that she expects Jane and Bingley to become engaged. Elizabeth rejects Mr. Collins' marriage proposal, to her mother's fury and her father's relief. Mr. Collins instead proposes to Charlotte Lucas, a friend of<br>Elizabeth. Having heard Mrs. Bennet's words at the ball and disapproving of the marriage, Mr. Darcy joins Mr. Bingley in a trip to London and, with the help of his sisters, convinces him not to return to Netherfield. A heartbroken Jane visits her Aunt and Uncle Gardiner in London to<br>raise her spirits, while Elizabeth's hatred for Mr. Darcy grows as she suspects he was responsible for Mr Bingley's departure."
    return render_template('caseSummary.html',name = v_name,notes = v_notes, goal = v_goal, rcmd = v_rcmd) 

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


@app.route('/notes')
def notes():
    variable = "check your name"
    return render_template('notes.html', value = variable)

@app.route('/attachments')
def attachments():
    variable = "check your name"
    return render_template('attachments.html', value = variable)