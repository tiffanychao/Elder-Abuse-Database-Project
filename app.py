from flask import Flask, render_template, request
app = Flask(__name__)
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from Database.client_information import ClientInformation
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()  # take environment variables from .env.


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DatabaseUser")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DatabasePassword")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DatabaseDB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DatabaseHost")
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route('/client')
def client():
    return render_template('client.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/client_information', methods = ["POST", "GET"])
def client_information():
    print(request.form.get('func_status'))
    referral_id = 2
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    client_id = data[0]
    if request.method == "POST":
        cursor.execute("""UPDATE clients SET cl_phys_name = (%s),cl_phys_ph = (%s), cl_insurance = (%s) , 
        cl_medications = (%s), cl_Illnesses = (%s), cl_functional_status = (%s) WHERE client_id = """ + str(client_id),
         (request.form["physician_name"], request.form["physician_telephone"], 
         request.form["insurance"], request.form["medication"], request.form["illnesses_and_addictions"], request.form.get('func_status')))
        conn.commit()

    cursor.execute("SELECT * FROM clients INNER JOIN cases on clients.referral_id = cases.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    content = {}
    content['physican_name'] = data[17]
    content['phys_num'] = data[18]
    content['insurance'] = data[19]
    content['medication'] = data[20]
    content['illnesses'] = data[21]
    content['functional_status'] = data[22]
    content['cognitive_status'] = data[23]
    content['living_setting'] = data[24]
    content['lives_with'] = data[25]
    content['lives_with_desc'] = data[26]
    content['prev_abuse_no'] = data[27]
    content['prev_abuse_yes'] = data[28]
    content['prev_abuse_desc'] = data[29]
    content['multiple_suspects'] = data[30]

    if data == None:
        return "Sorry your data isn't here"
    if request.method == "POST":
        return render_template('clientInformation.html', **content)
    return render_template('clientInformation.html', **content)

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

@app.route('/search_cases',methods =["GET", "POST"])
def search_cases():
    if request.method == "POST":
       
        return  data1 
    # deal with the data
    #
    v_num = 2
    v_result = "In the early 19th century,<br> the Bennet family live at their Longbourn estate,<br> situated near the village of Meryton in Hertfordshire, <br>England. Mrs. Bennet's greatest desire is to marry off her five daughters in order to secure their futures. The arrival of Mr. Bingley, a rich bachelor who rents the neighbouring Netherfield estate, gives her hope that one of her daughters might contract an advantageous marriage, because It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. <br>Mr. Collins, the heir to the Longbourn estate, visits the Bennet family with the intention of finding a wife among the five girls under the advice of his patroness Lady Catherine de Bourgh, also revealed to be Mr. Darcy's aunt. He decides to pursue Elizabeth. The Bennet family meet the charming army officer George Wickham, <br>who tells Elizabeth in confidence Mr. Darcy's horrible past actions in his regards. Elizabeth, blinded by her prejudice toward Mr. Darcy, believes him.<br>Elizabeth dances with Mr. Darcy at a ball, where Mrs. Bennet hints loudly that she expects Jane and Bingley to become engaged. Elizabeth rejects Mr. Collins' marriage proposal, to her mother's fury and her father's relief. Mr. Collins instead proposes to Charlotte Lucas, a friend of<br>Elizabeth. Having heard Mrs. Bennet's words at the ball and disapproving of the marriage, Mr. Darcy joins Mr. Bingley in a trip to London and, with the help of his sisters, convinces him not to return to Netherfield. A heartbroken Jane visits her Aunt and Uncle Gardiner in London to<br>raise her spirits, while Elizabeth's hatred for Mr. Darcy grows as she suspects he was responsible for Mr Bingley's departure."
    return render_template('searchCases.html',number = v_num, result = v_result) 

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