from flask import Flask, render_template, request
app = Flask(__name__)
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables
from mysql.connector import Error
import mysql.connector
from datetime import datetime
import random
load_dotenv()  # take environment variables from .env.


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DatabaseUser")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DatabasePassword")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DatabaseDB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DatabaseHost")
mysql.init_app(app)


# conn = mysql.connect()
# cursor = conn.cursor()

# check whether DB is connected
try:
    conn = mysql.connect()
    if conn:
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)

@app.route('/client', methods = ["POST", "GET"])
def client():
    referral_id = 3
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data == None:
        return "There is no data sorry"
    client_id = data[0]
    if request.method == "POST":
        cursor.execute("""UPDATE clients SET cl_name_first = (%s),cl_name_last = (%s), cl_age = (%s) , 
        cl_DOB = (%s), cl_language = (%s), cl_TransComm = (%s), cl_education = (%s), cl_ethnicity = (%s), 
        cl_gender = (%s), cl_marital = (%s), cl_address = (%s), cl_city = (%s), 
        cl_zip = (%s), cl_phone = (%s) WHERE client_id = """ + str(client_id),
         (request.form["cl_name_first"], request.form["cl_name_last"], 
         request.form["cl_age"], request.form["cl_DOB"], request.form["cl_language"], request.form["cl_TransComm"],
         request.form.get('cl_education'), request.form.get("cl_ethnicity"), request.form.get("cl_gender"), 
         request.form.get("cl_marital"), request.form("cl_address"), request.form("cl_city"), request.form("cl_zip"),
         request.form("cl_phone")))
        conn.commit()

    cursor.execute("SELECT * FROM clients INNER JOIN cases on clients.referral_id = cases.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    print(data)
    content = {}
    content['cl_name_first'] = data[2]
    content['cl_name_last'] = data[3]
    content['cl_age'] = data[5]
    content['cl_DOB'] = data[6]
    content['cl_language'] = data[7]
    content['cl_TransComm'] = data[8]
    content['cl_education'] = data[9]
    content['cl_ethnicity'] = data[10]
    content['cl_gender'] = data[11]
    content['cl_marital'] = data[12]
    content['cl_address'] = data[13]
    content['cl_city'] = data[14]
    content['cl_zip'] = data[15]
    content['cl_phone'] = data[16]

    if request.method == "POST":
        return render_template('client.html', **content)
    return render_template('client.html', **content)  

@app.route('/client_information', methods = ["POST", "GET"])
def client_information():
    prev_abuse_no = True
    prev_abuse_yes = True
    multiple_alleged_suspects = True
    if request.form.get("previous_abuse_no") == None:
        prev_abuse_no = False
    if request.form.get("previous_abuse_yes") == None:
        prev_abuse_yes = False

    if request.form.get("multiple_alleged_suspects") == None:
        multiple_alleged_suspects = False


    
    referral_id = 1
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data == None:
        return "There is no data sorry"
    client_id = data[0]
    if request.method == "POST":
        request.form.getlist("previous_abuse_no")
        cursor.execute("""UPDATE clients SET cl_phys_name = (%s),cl_phys_ph = (%s), cl_insurance = (%s) , 
        cl_medications = (%s), cl_Illnesses = (%s), cl_functional_status = (%s), cl_cognitive_status = (%s), cl_living_setting = (%s), 
        cl_lives_with = (%s), cl_lives_with_desc = (%s), cl_prev_abuse_no = (%s), cl_prev_abuse_yes = (%s), 
        cl_prev_abuse_desc = (%s), cl_multiple_suspects = (%s) WHERE client_id = """ + str(client_id),
         (request.form["physician_name"], request.form["physician_telephone"], 
         request.form["insurance"], request.form["medication"], request.form["illnesses_and_addictions"], 
         request.form.get('func_status'), request.form.get("cognitive_status"), request.form.get("living_setting"), 
         request.form.get("lives_with"), request.form.get("other_describe"), prev_abuse_no, prev_abuse_yes, request.form.get("previous_abuse_explain"), multiple_alleged_suspects  ))
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

    if request.method == "POST":
        return render_template('clientInformation.html', **content)
    return render_template('clientInformation.html', **content)

@app.route('/abuser')
def abuser():
    return render_template('abuser.html', sampleInfo = "sampleInfo", exampleCheckbox = "1")

@app.route('/center_outcomes', methods = ["POST", "GET"])
def center_outcomes():
    content = {}
    referral_id = 1
    oc_csv_probate = True
    oc_csv_pubg = True
    oc_csv_lps = True
    oc_csv_temp = True
    oc_sa = True
    oc_ev_geri = True
    oc_ev_neuro = True
    oc_ev_mental = True
    oc_ev_law = True
    oc_ss_support = True
    oc_ss_compAPS = True
    oc_ss_civil = True
    oc_ap_freeze = True
    oc_ap_other = True
    oc_ap_restitution = True
    oc_pr_charges = True
    oc_pr_legal = True
    oc_self_suff = True
    oc_cp_arrest = True
    oc_cp_hospital = True
    if(request.form.get("oc_csv_probate") == None):
        oc_csv_probate = False
    if(request.form.get("oc_csv_pubg") == None):
        oc_csv_pubg = False
    if(request.form.get("oc_csv_lps") == None):
        oc_csv_lps = False
    if(request.form.get("oc_csv_temp") == None):
        oc_csv_temp = False
    if(request.form.get("oc_sa") == None):
        oc_sa = False
    if(request.form.get("oc_ev_geri") == None):
        oc_ev_geri = False
    if(request.form.get("oc_ev_neuro") == None):
        oc_ev_neuro = False
    if(request.form.get("oc_ev_mental") == None):
        oc_ev_mental = False
    if(request.form.get("oc_ev_law") == None):
        oc_ev_law = False
    if(request.form.get("oc_ss_support") == None):
        oc_ss_support = False
    if(request.form.get("oc_ss_compAPS") == None):
        oc_ss_compAPS = False
    if(request.form.get("oc_ss_civil") == None):
        oc_ss_civil = False
    if(request.form.get("oc_ap_freeze") == None):
        oc_ap_freeze = False
    if(request.form.get("oc_ap_other") == None):
        oc_ap_other = False
    if(request.form.get("oc_ap_restitution") == None):
        oc_ap_restitution = False
    if(request.form.get("oc_pr_charges") == None):
        oc_pr_charges = False
    if(request.form.get("oc_pr_legal") == None):
        oc_pr_legal = False
    if(request.form.get("oc_self_suff") == None):
        oc_self_suff = False
    if(request.form.get("oc_cp_arrest") == None):
        oc_cp_arrest = False
    if(request.form.get("oc_cp_hospital") == None):
        oc_cp_hospital = False
    
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM outcome INNER JOIN cases ON cases.referral_id = outcome.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()

    if data == None:
        return "There is no data sorry"

    if request.method == "POST":
        request.form.getlist("previous_abuse_no")
        cursor.execute("""UPDATE outcome SET oc_csv_probate = (%s), oc_csv_pubg = (%s),
        oc_csv_ext = (%s), oc_csv_lps = (%s), oc_csv_priv = (%s), oc_csv_name = (%s),
        oc_csv_temp = (%s), oc_sa  = (%s), oc_ev_geri = (%s), oc_ev_neuro = (%s), oc_ev_mental = (%s), oc_ev_law = (%s),
        oc_ss_support = (%s), oc_ss_compAPS = (%s), oc_ss_civil = (%s), oc_ap_freeze = (%s), oc_ap_other = (%s), oc_ap_restitution = (%s),
        oc_pr_charges = (%s), oc_pr_legal = (%s), oc_self_suff = (%s), oc_cp_arrest = (%s), oc_cp_hospital = (%s), oc_ro = (%s), oc_ro_name = (%s)  WHERE referral_id = """ + str(referral_id),
         (oc_csv_probate,oc_csv_pubg,request.form.get("oc_csv_ext"), oc_csv_lps, request.form.get("oc_csv_priv"), 
         request.form.get("oc_csv_name"),oc_csv_temp, oc_sa,oc_ev_geri, oc_ev_neuro, oc_ev_mental, oc_ev_law, 
         oc_ss_support,oc_ss_compAPS,oc_ss_civil,oc_ap_freeze, oc_ap_other,
         oc_ap_restitution,oc_pr_charges,oc_pr_legal,oc_self_suff, oc_cp_arrest, oc_cp_hospital, request.form.get("oc_ro"), request.form.get("oc_ro_name")))
        conn.commit()

    cursor.execute("SELECT * FROM outcome INNER JOIN cases on outcome.referral_id = cases.referral_id WHERE outcome.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()

    
    content["oc_cp_arrest"] = data[1]
    content["oc_cp_hospital"] = data[2]
    content["oc_ev_neuro"] = data[3]
    content["oc_ev_mental"] = data[4]
    content["oc_ev_law"] = data[5]
    content["oc_ss_support"] = data[6]
    content["oc_ss_compAPS"] = data[7]
    content["oc_ss_civil"] = data[8]
    content["oc_ap_freeze"] = data[9]
    content["oc_ap_other"] = data[10]
    content["oc_ap_restitution"] = data[11]
    content["oc_pr_charges"] = data[12]
    content["oc_pr_legal"] = data[13]
    content["oc_narrative"] = data[14]
    content["oc_csv_probate"] = data[15]
    content["oc_csv_lps"] = data[16]
    content["oc_csv_temp"] = data[17]
    content["oc_csv_pubg"] = data[18]
    content["oc_csv_priv"] = data[19]
    content["oc_csv_ext"] = data[20]
    content["oc_csv_name"] = data[21]
    content["oc_sa"] = data[22]
    content["oc_ro"] = data[23]
    content["oc_ro_name"] = data[24]
    content["oc_ev_geri"] = data[25]
    content["oc_self_suff"] = data[26]
    return render_template("centerOutcomes.html", **content)

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
    
    table_list = SQL_for_search_cases()
    v_num = len(table_list)
    return render_template('searchCases.html',number = v_num, result = table_list) 

def SQL_for_search_cases():
    result =  [dict(link="https://www.google.com/",id="1234", name="John Doe4"),
                dict(link="https://www.google.com/",id="1235", name="John Doe5"),
                dict(link="https://www.google.com/",id="1236", name="John Doe6"),
                dict(link="https://www.google.com/",id="1237", name="John Doe7"),
                ]
    return result

@app.route('/')
def homepage():
    return render_template('homepage.html')




@app.route('/example')
def example():
    variable = "check your name"
    return render_template('example.html', value = variable)

@app.route('/narrative',methods =["GET", "POST"])
def narrative():
    referral_id = 2
    cursor.execute("SELECT * FROM meeting_notes INNER JOIN cases ON cases.referral_id = meeting_notes.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    print(data)
    if request.method == "POST":
        meeting_narrative = request.form.get("meeting_narrative")
        cur = conn.cursor()
        sql = "insert into meeting_notes(meeting_narrative) values (%s)"
        val = meeting_narrative
        cur.execute(sql, val)
        conn.commit()
        print(cur.rowcount, "record inserted.")
    content = {}
    content["meeting_narrative"] = data[6]
    print(content)
    if data == None:
        return "Sorry your data isn't here"
    if request.method == "POST":
        return render_template('narrative.html', **content)
    return render_template('narrative.html', **content)


@app.route('/consulation')
def consulation():
    variable = "check your name"
    return render_template('consulation.html', value = variable)


@app.route('/notes',methods =["GET", "POST"])
def notes():
    referral_id = 2
    # meeting_notes
    cursor.execute("SELECT * FROM meeting_notes INNER JOIN cases ON cases.referral_id =meeting_notes.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    meeting_id = data[0]
    # goals
    cursor.execute("SELECT * FROM goals INNER JOIN cases ON cases.referral_id =goals.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data1 = cursor.fetchone()
    client_goals_id = data1[0]
    # recommendations
    cursor.execute("SELECT * FROM recommendations INNER JOIN cases ON cases.referral_id =recommendations.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data2 = cursor.fetchone()
    client_rec_id  = data2[0]
    

    if request.method == "POST":
        # meeting notes
        presenter = request.form.get("presenter")
        meeting_date = datetime.strptime(request.form.get("meeting_date"),'%Y-%m-%d')
        meeting_notes = request.form.get("meeting_notes")
        meeting_recs = ""
        fake_goals = ""
        # goals
        goal = request.form.get("goals")
        # recommendations
        action_step = request.form.get("action_step")
        person_response = request.form.get("person_response")
        follow_up = datetime.strptime(request.form.get("follow_up"),'%Y-%m-%d')
        action_status = request.form.get("status")
        
        # meeting notes insertion
        cur = conn.cursor()
        cursor.execute("""UPDATE meeting_notes SET meeting_date = (%s),meeting_recs = (%s), meeting_goals = (%s) , 
        Meeting_presenters = (%s), meeting_narrative = (%s) WHERE meeting_id = """ + str(meeting_id),(meeting_date, meeting_recs,fake_goals,presenter,meeting_notes))

        conn.commit()
        print(cur.rowcount, "record inserted.")
        # for Goals - goals table
        cur = conn.cursor()
        cursor.execute("""UPDATE goals SET goal = (%s) WHERE client_goals_id = """ + str(client_goals_id),(goal))
        conn.commit()
        print(cur.rowcount, "record inserted.")       
        # for recommendations
        cur = conn.cursor()
        cursor.execute("""UPDATE recommendations SET  action_step = (%s), person_responsible = (%s), followup_date = (%s), action_status = (%s) WHERE client_rec_id = """ + str(client_rec_id),(action_step,person_response,follow_up,action_status))
        conn.commit()
        print(cur.rowcount, "record inserted.")

    # meeeting_notes
    cursor.execute("SELECT * FROM meeting_notes INNER JOIN cases ON cases.referral_id = meeting_notes.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    
    # recommendations
    cursor.execute("SELECT * FROM recommendations INNER JOIN cases ON cases.referral_id = recommendations.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data2 = cursor.fetchone()
    
    # goal
    cursor.execute("SELECT * FROM goals INNER JOIN cases ON cases.referral_id = goals.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data3 = cursor.fetchone()
    
    content = {}
    content["presenter"] = data[5]
    content["meeting_date"] = data[2]
    content["meeting_notes"] = data[6] # meeting_narrative
    content["goals"] = data3[2]# goals.goal
    content["action_step"] = data2[2] 
    content["person_response"] = data2[3]
    content["follow_up"] = data2[4]
    content["status"] = data2[5]

    if data == None:
        return "Sorry your data isn't here"
    if request.method == "POST":
        return render_template('notes.html',  **content)

    return render_template('notes.html', **content)

@app.route('/attachments')
def attachments():
    variable = "check your name"
    return render_template('attachments.html', value = variable)


