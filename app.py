import pathlib
from flask import Flask, render_template, request,flash, send_from_directory, send_file
app = Flask(__name__)
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from getDataFromDB import *
import os #provides ways to access the Operating System and allows us to read the environment variables
from datetime import datetime
import pandas as pd
import pathlib
import worddocparser
import docToSql
load_dotenv()  # take environment variables from .env.


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DatabaseUser")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DatabasePassword")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DatabaseDB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DatabaseHost")
# app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
mysql.init_app(app)


conn = mysql.connect()
cursor = conn.cursor()



@app.errorhandler(404)
def not_found(e):
  return render_template('error_handling.html')


@app.route('/case_info/<int:referral_id>', methods = ["POST", "GET"])
def case_info(referral_id): 
    status_urgent = True
    status_routine = True
    case_closed = True
    if request.form.get("status_urgent") == None:
        status_urgent = False
    if request.form.get("status_routine") == None:
        status_routine = False
    if request.form.get("case_closed") == None:
        case_closed = False    
    dateForm = request.form.get("case_date")
    if request.method == "POST":
        cursor.execute("""UPDATE cases SET status_urgent = (%s), status_routine = (%s), case_closed = (%s) WHERE referral_id = """ + str(referral_id),
         (status_urgent, status_routine,case_closed))
        conn.commit()

        if dateForm != None and dateForm != '':
            cursor.execute("""UPDATE cases SET case_date = (%s) WHERE referral_id = """ + str(referral_id),
         (dateForm))
            conn.commit()

        cursor.execute("""UPDATE case_number SET case_number = (%s) WHERE referral_id = """ + str(referral_id),
         (request.form.get("case_number")))
        conn.commit()

    cursor.execute("SELECT * FROM cases INNER JOIN case_number ON cases.referral_id = case_number.referral_id WHERE cases.referral_id = " + str(referral_id) + ';')
    data = cursor.fetchone()
    if data == None:
        return render_template('error_handling.html')
    
    content = {}
    content["status_urgent"] = data[1]
    content["status_routine"] = data[2]
    content["case_date"] = data[3]
    content["case_closed"] = data[4]
    content["case_number"] = data[5]
    print(data)
    content['searchCase'] = True
    content['bar_urgentstatus'] = content['status_urgent']
    content['bar_routinestatus'] = content['status_routine']
    content['bar_caseclosed'] = content['case_closed']
    content['bar_date'] = content['case_date']
    content['bar_case_number'] = content['case_number']
    return render_template('case_info.html', referral_id = referral_id, **content)
    

@app.route('/client/<int:referral_id>', methods = ["POST", "GET"])
def client(referral_id):  
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    print(data)
    ageField = request.form.get('cl_age')
    dateField = request.form.get("cl_DOB")
    if data == None:
        return render_template('error_handling.html')
    client_id = data[0]
    if request.method == "POST":
        cursor.execute("""UPDATE clients SET cl_name_first = (%s),cl_name_last = (%s) , 
        cl_language = (%s), cl_TransComm = (%s), cl_education = (%s), cl_ethnicity = (%s), 
        cl_gender = (%s), cl_marital = (%s), cl_address = (%s), cl_city = (%s), 
        cl_zip = (%s), cl_phone = (%s) WHERE client_id = """ + str(client_id),
         (request.form["cl_name_first"], request.form["cl_name_last"], 
            request.form["cl_language"], request.form["cl_TransComm"],
         request.form.get('cl_education'), request.form.get("cl_ethnicity"), request.form.get("cl_gender"), 
         request.form.get("cl_marital"), request.form.get("cl_address"), request.form.get("cl_city"), 
         request.form.get("cl_zip"),request.form.get("cl_phone")))
        conn.commit()

        if(ageField != ""):
            cursor.execute("""UPDATE clients SET cl_age = (%s) WHERE client_id = """ + str(client_id),
         (ageField))
            conn.commit()
        if(dateField != ""):
            cursor.execute("""UPDATE clients SET cl_DOB = (%s) WHERE client_id = """ + str(client_id),
         (dateField))
            conn.commit()

    cursor.execute("SELECT * FROM clients INNER JOIN cases on clients.referral_id = cases.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()

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
    content['searchCase'] = True

    if request.method == "POST":
        return render_template('client.html',referral_id =referral_id, **content)

    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    return render_template('client.html',referral_id = referral_id, **content)  


@app.route('/client_information/<int:referral_id>', methods = ["POST", "GET"])
def client_information(referral_id):
    prev_abuse_no = True
    prev_abuse_yes = True
    multiple_alleged_suspects = True
    if request.form.get("previous_abuse_no") == None:
        prev_abuse_no = False
    if request.form.get("previous_abuse_yes") == None:
        prev_abuse_yes = False

    if request.form.get("multiple_alleged_suspects") == None:
        multiple_alleged_suspects = False


    # if referral_id == None:
    # referral_id = 1
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data == None:
        return render_template('error_handling.html')
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
    content['searchCase'] = True
    
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']

    if request.method == "POST":
        return render_template('clientInformation.html',referral_id = referral_id, **content)
    return render_template('clientInformation.html',referral_id = referral_id, **content)

@app.route('/abuser/<int:referral_id>', methods = ["POST", "GET"])
def abuser(referral_id):
    su_PrimCrGvYES = True
    su_PrimCrGvNO = True
    su_LivesWthYES = True
    su_LivesWthNO = True
    su_AdAlchlYES = True
    su_AdAlchlNO = True
    su_AdAlchlUNK = True
    su_AdDrugsYES = True
    su_AdDrugsNO = True
    su_AdDrugsUNK = True
    su_AdPrepYES = True
    su_AdPrepNO = True
    su_AdPrepUNK = True
    if(request.form.get('su_PrimCrGvYES') == None):
        su_PrimCrGvYES = False
    if(request.form.get('su_PrimCrGvNO')== None):
        su_PrimCrGvNO = False
    if(request.form.get('su_LivesWthYES') == None):
        su_LivesWthYES = False
    if(request.form.get('su_LivesWthNO') == None):
        su_LivesWthNO = False
    if(request.form.get('su_AdAlchlYES') == None):
       su_AdAlchlYES = False
    if(request.form.get('su_AdAlchlNO') == None):
        su_AdAlchlNO = False
    if(request.form.get('su_AdAlchlUNK') == None):
        su_AdAlchlUNK = False
    if(request.form.get('su_AdDrugsYES') == None):
        su_AdDrugsYES = False
    if(request.form.get('su_AdDrugsNO') == None):
        su_AdDrugsNO = False
    if(request.form.get('su_AdDrugsUNK') == None):
        su_AdDrugsUNK = False
    if(request.form.get('su_AdPrepYES') == None):
        su_AdPrepYES = False
    if(request.form.get('su_AdPrepNO') == None):
        su_AdPrepNO = False
    if(request.form.get('su_AdPrepUNK') == None):
        su_AdPrepUNK = False
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM suspects INNER JOIN cases ON cases.referral_id = suspects.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    
    if data == None:
        return render_template('error_handling.html')
 
    su_id = data[0]
    if request.method == "POST":
        cursor.execute("""UPDATE suspects SET su_name_first = (%s),su_name_last = (%s), su_organization = (%s), 
        su_age = (%s), su_DOB = (%s), su_ethnicity = (%s), su_gender = (%s), su_language = (%s), 
        su_TransComm = (%s), su_PrimCrGvYES = (%s), su_PrimCrGvNO = (%s), su_LivesWthYES = (%s), 
        su_relationship = (%s), su_LivesWthNO = (%s), su_mental_ill = (%s), su_mental_ill_desc = (%s),
        su_AdAlchlYES = (%s), su_AdAlchlNO = (%s), su_AdAlchlUNK = (%s), su_AdDrugsYES = (%s),
        su_AdDrugsNO = (%s), su_AdDrugsUNK = (%s), su_AdPrepYES = (%s), su_AdPrepNO = (%s),
        su_AdPrepUNK = (%s), su_AdOther = (%s), su_address = (%s), su_city = (%s), su_zip = (%s),
        su_phone = (%s) WHERE su_id = """ + str(su_id),
         (request.form["su_name_first"], request.form["su_name_last"], 
         request.form["su_organization"], request.form["su_age"], request.form["su_DOB"], request.form.get("su_ethnicity"),
         request.form.get('su_gender'), request.form.get("su_language"), request.form.get("su_TransComm"), 
         su_PrimCrGvYES, su_PrimCrGvNO, su_LivesWthYES, request.form.get("su_relationship"), 
         su_LivesWthNO,request.form.get("su_mental_ill"), request.form.get("su_mental_ill_desc"),  
         su_AdAlchlYES, su_AdAlchlNO, su_AdAlchlUNK, 
         su_AdDrugsYES,su_AdDrugsNO, su_AdDrugsUNK, 
         su_AdPrepYES, su_AdPrepNO, su_AdPrepUNK, 
         request.form.get("su_AdOther"),request.form.get("su_address"), request.form.get("su_city"),
         request.form.get("su_zip"),request.form.get("su_phone")))
        conn.commit()
    
    cursor.execute("SELECT * FROM suspects INNER JOIN cases on cases.referral_id = suspects.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    print(data)   
    content = {}
    content['su_name_first'] = data[2]
    content['su_name_last'] = data[3]
    content['su_organization'] = data[4]
    content['su_age'] = data[6]
    content['su_DOB'] = data[7]
    content['su_ethnicity'] = data[8]
    content['su_gender'] = data[9]
    content['su_language'] = data[10]
    content['su_TransComm'] = data[11]
    content['su_PrimCrGvYES'] = data[12]
    content['su_PrimCrGvNO'] = data[13]
    content['su_LivesWthYES'] = data[14]
    content['su_relationship'] = data[15]
    content['su_LivesWthNO'] = data[16]
    content['su_mental_ill'] = data[17]
    content['su_mental_ill_desc'] = data[18]
    content['su_AdAlchlYES'] = data[19]
    content['su_AdAlchlNO'] = data[20]
    content['su_AdAlchlUNK'] = data[21]
    content['su_AdDrugsYES'] = data[22]
    content['su_AdDrugsNO'] = data[23]
    content['su_AdDrugsUNK'] = data[24]
    content['su_AdPrepYES'] = data[25]
    content['su_AdPrepNO'] = data[26]
    content['su_AdPrepUNK'] = data[27]
    content['su_AdOther'] = data[28]
    content['su_address'] = data[29]
    content['su_city'] = data[30]
    content['su_zip'] = data[31]
    content['su_phone'] = data[32]
    content['searchCase'] = True

    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    return render_template('abuser.html',referral_id = referral_id, **content)


@app.route('/abuse_info/<int:referral_id>', methods = ["POST", "GET"])
def abuse_info(referral_id):
    ad_Abandon = True
    ad_Abduction = True
    ad_Emotional = True
    ad_FinanRlEst = True
    ad_FinanOth = True
    ad_Isolation = True
    ad_Sexual = True
    ad_SelfNeglec = True
    ad_NeglectOth = True
    ad_PhyAssault = True
    ad_PhyChemRst = True
    ad_PhyCnstDpr = True
    ad_PhyMedicat = True
    ad_UndueInflu = True
    ad_Other = True
    if(request.form.get('ad_Abandon') == None):
        ad_Abandon = False
    if(request.form.get('ad_Abduction')== None):
        ad_Abduction = False
    if(request.form.get('ad_Emotional') == None):
        ad_Emotional = False
    if(request.form.get('ad_FinanRlEst') == None):
        ad_FinanRlEst = False
    if(request.form.get('ad_FinanOth') == None):
        ad_FinanOth = False
    if(request.form.get('ad_Isolation') == None):
        ad_Isolation = False
    if(request.form.get('ad_Sexual') == None):
        ad_Sexual = False
    if(request.form.get('ad_SelfNeglec') == None):
        ad_SelfNeglec = False
    if(request.form.get('ad_NeglectOth') == None):
        ad_NeglectOth = False
    if(request.form.get('ad_PhyAssault') == None):
        ad_PhyAssault = False
    if(request.form.get('ad_PhyChemRst') == None):
        ad_PhyChemRst = False
    if(request.form.get('ad_PhyCnstDpr') == None):
        ad_PhyCnstDpr = False
    if(request.form.get('ad_PhyMedicat') == None):
        ad_PhyMedicat = False
    if(request.form.get('ad_UndueInflu') == None):
        ad_UndueInflu = False
    if(request.form.get('ad_Other') == None):
        ad_Other = False
     # figure out the associated abuse_id of the referral_id
    cursor.execute("SELECT * FROM abuse_information INNER JOIN cases ON cases.referral_id = abuse_information.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data == None:
        return render_template('error_handling.html')
    abuse_id = data[0]
    if request.method == "POST":
        cursor.execute("""UPDATE abuse_information SET ad_InvAgencies = (%s), ad_RptingParty = (%s), ad_Others = (%s), ad_Abandon = (%s),
         ad_Abduction = (%s), ad_Emotional = (%s), ad_FinanRlEst = (%s), ad_FinanOth = (%s), ad_FinanLoss = (%s), ad_Isolation= (%s), ad_Sexual = (%s), ad_SelfNeglec = (%s), 
         ad_NeglectOth = (%s), ad_PhyAssault = (%s), ad_PhyChemRst =(%s), ad_PhyCnstDpr = (%s), ad_PhyMedicat = (%s), ad_UndueInflu = (%s), ad_Other = (%s), ad_Narrative = (%s) WHERE abuser_id = """ + str(abuse_id),
            (request.form.get('ad_InvAgencies'), request.form.get('ad_RptingParty'), request.form.get('ad_Others'),ad_Abandon,ad_Abduction,
            ad_Emotional,ad_FinanRlEst,ad_FinanOth,request.form.get('ad_FinanLoss'), ad_Isolation, ad_Sexual, ad_SelfNeglec, ad_NeglectOth,ad_PhyAssault, ad_PhyChemRst, 
            ad_PhyCnstDpr, ad_PhyMedicat, ad_UndueInflu, ad_Other, request.form.get('ad_Narrative') ))
        conn.commit()

    cursor.execute("SELECT * FROM abuse_information INNER JOIN cases ON cases.referral_id = abuse_information.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    content = {}
    content['ad_InvAgencies'] = data[2] 
    content['ad_RptingParty'] = data[3]
    content['ad_Others'] = data[4]
    content['ad_Abandon'] = data[5]
    content['ad_Abduction'] = data[6]   
    content['ad_Emotional'] = data[7] 
    content['ad_FinanRlEst'] = data[8] 
    content['ad_FinanOth'] = data[9] 
    content['ad_FinanLoss'] = data[10] 
    content['ad_Isolation'] = data[11] 
    content['ad_Sexual'] = data[12]  
    content['ad_SelfNeglec'] = data[13] 
    content['ad_NeglectOth'] = data[14] 
    content['ad_PhyAssault'] = data[15] 
    content['ad_PhyChemRst'] = data[16] 
    content['ad_PhyCnstDpr'] = data[17] 
    content['ad_PhyMedicat'] = data[18] 
    content['ad_UndueInflu'] = data[19] 
    content['ad_Other'] = data[20] 
    content['ad_Narrative'] = data[21] 
    
    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    print('--------')
    print(content)
    return render_template('abuse_info.html',referral_id = referral_id, **content)



@app.route('/center_outcomes/<int:referral_id>', methods = ["POST", "GET"])
def center_outcomes(referral_id):
    content = {}
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
        return render_template('error_handling.html')

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

    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    return render_template("centerOutcomes.html",referral_id = referral_id, **content)



@app.route('/referring_agency/<referral_id>',methods =["GET", "POST"])
def referring_agency(referral_id):
    # referral_id = 1
    
    if request.method == "POST":
 
        cursor.execute("""UPDATE referring_agency SET ra_fname = (%s),ra_lname = (%s),ra_fc_team = (%s),ra_fc_other = (%s), ra_email = (%s), ra_ph_office = (%s),ra_fx_office = (%s),ra_ph_mobile = (%s), ra_supervisor_name = (%s)   WHERE referral_id = """ + str(referral_id),
         (request.form["FirstName"], request.form["LastName"], 
         request.form["FCTeamMember"], request.form["FCTeamOther"], request.form["Email"], 
         request.form.get('OfficePhone'), request.form.get("OfficeTax"), request.form.get("MobilePhone"), 
         request.form.get("SupervisorName")  ))
        conn.commit()

    dictInfo = get_referral_info_from_db(referral_id,cursor,conn)
    if not dictInfo :
        return render_template('error_handling.html')
    dictInfo['referral_id'] = referral_id
    dictInfo['searchCase'] = True

    barinfo = getBarInfo(referral_id,cursor,conn)
    dictInfo['bar_urgentstatus'] = barinfo['status_urgent']
    dictInfo['bar_routinestatus'] = barinfo['status_routine']
    dictInfo['bar_caseclosed'] = barinfo['case_closed']
    dictInfo['bar_date'] = barinfo['case_date']
    dictInfo['bar_case_number'] = barinfo['case_number']

    return render_template('referringAgency.html', **dictInfo)



    
@app.route('/case_summary/<referral_id>',methods =["GET", "POST"])
def case_summary(referral_id):

    
    dic = get_case_summary_from_db(referral_id,cursor,conn)
    dic['referral_id'] = referral_id
  
    barinfo = getBarInfo(referral_id,cursor,conn)
    dic['bar_urgentstatus'] = barinfo['status_urgent']
    dic['bar_routinestatus'] = barinfo['status_routine']
    dic['bar_caseclosed'] = barinfo['case_closed']
    dic['bar_date'] = barinfo['case_date']
    dic['bar_case_number'] = barinfo['case_number']
    return render_template('caseSummary.html',**dic) 



@app.route('/search_cases',methods =["GET", "POST"])
def search_cases():
    delete_referal_id = -1
    search_type = 'client'
    first_name = ''
    last_name = ''
    full_name = ''
    case_closed = 0
    query = 0
    if request.method == "POST":
        if (request.form.get("deleteButton")):
            delete_referal_id = request.form.get("deleteButton")
            delete_case(delete_referal_id,cursor,conn)
        
            
        search_type = request.form.get("searchType")
        # print(search_type)
        first_name = request.form.get("FirstName")
        last_name =  request.form.get("LastName")
        full_name =  request.form.get("FullName")
    
        if (request.form.get("closedCased")):
            case_closed = 1

        # print(case_closed)
    
    dic = dict()
    

   
    infolist = search_cases_from_database(search_type,first_name,last_name,full_name,case_closed,cursor,conn)
    v_num = len(infolist)
    dic = dict()
    dic['searchType'] = search_type
    if search_type == 'presenter':
        first_name = ''
        last_name = ''
    if search_type != 'presenter' :
        full_name = ''
    dic['firstName'] = first_name
    dic['fullName'] = full_name
    dic['lastName'] = last_name
    
        
    dic['closedCase'] = case_closed
    dic['number'] = v_num
    dic['result'] = infolist
    
    return render_template('searchCases.html',**dic) 





@app.route('/')
def homepage():
    return render_template('homepage.html',referral_id = -1, searchCase = False)




@app.route('/example')
def example():
    variable = "check your name"
    return render_template('example.html', value = variable, searchCase = False)

@app.route('/narrative/<int:referral_id>',methods =["GET", "POST"])
def narrative(referral_id):
    cursor.execute("SELECT * FROM outcome INNER JOIN cases ON cases.referral_id = outcome.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data == None:
        return render_template('error_handling.html')
    
    if request.method == "POST":
        oc_narrative = request.form.get("oc_narrative")
        cursor.execute("""UPDATE outcome SET  oc_narrative = (%s) WHERE referral_id = """ + str(referral_id),
         (oc_narrative))

        conn.commit()
        
    cursor.execute("SELECT * FROM outcome INNER JOIN cases ON cases.referral_id = outcome.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    content = {}
    content["oc_narrative"] = data[14]
    
    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    if data == None:
        return render_template('error_handling.html')
    if request.method == "POST":
        return render_template('narrative.html',referral_id = referral_id, **content)
    return render_template('narrative.html',referral_id = referral_id, **content)


@app.route('/consultation/<int:referral_id>', methods =["GET", "POST"])
def consulation(referral_id):

    cursor.execute("SELECT * FROM consultation_information INNER JOIN cases ON cases.referral_id = consultation_information.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    #consultation_id = data[0]
    if data == None:
        return render_template('error_handling.html')

    
    #
    Services = True
    GENESIS = True
    DA = True
    Regional_center = True
    Corner = True
    Law_enforcement = True
    Attorney = True
    Psychologist = True
    Medical_Practitioner = True
    Ombudsman = True
    Public_Guardian = True
    Description_other = True

    if(request.form.get("Services") == None):
        Services = False
    if(request.form.get("GENESIS") == None):
        GENESIS = False
    if(request.form.get("DA") == None):
        DA = False
    if(request.form.get("Regional_center") == None):
        Regional_center = False
    if(request.form.get("Corner") == None):
        Corner = False
    if(request.form.get("Law_enforcement") == None):
        Law_enforcement = False
    if(request.form.get("Attorney") == None):
        Attorney = False
    if(request.form.get("Psychologist") == None):
        Psychologist = False
    if(request.form.get("Medical_Practitioner") == None):
        Medical_Practitioner = False
    if(request.form.get("Ombudsman") == None):
        Ombudsman = False
    if(request.form.get("Public_Guardian") == None):
        Public_Guardian = False
    if(request.form.get("Description_other") == None):
        Description_other = False
    if request.method == "POST":
        Services = bool(request.form.get("Services"))
        GENESIS = bool(request.form.get("GENESIS"))
        DA = bool(request.form.get("DA"))
        Regional_center = bool(request.form.get("Regional_center"))
        Corner = bool(request.form.get("Corner"))
        Law_enforcement = bool(request.form.get("Law_enforcement"))
        Attorney = bool(request.form.get("Attorney"))
        Psychologist = bool(request.form.get("Psychologist"))
        Medical_Practitioner = bool(request.form.get("Medical_Practitioner")) #physician
        Ombudsman = bool(request.form.get("Ombudsman"))
        Public_Guardian = bool(request.form.get("Public_Guardian"))
        Other = bool(request.form.get("Other"))
        Description_other = request.form.get("Description_other")
        Reason = request.form.get("Reason")
        
        
        
        cursor.execute("""UPDATE consultation_information SET consult_aps = (%s), consult_genesis = (%s),
        consult_district_att = (%s), consult_regional = (%s), consult_coroner = (%s), consult_law_enf = (%s),
        consult_att_oth = (%s), consult_psychologist  = (%s), consult_physician = (%s), consult_ombudsman = (%s), consult_pub_guard = (%s), consult_other = (%s),
        consult_other_desc = (%s), consult_reason = (%s)  WHERE referral_id = """ + str(referral_id),
         (Services, GENESIS, DA, Regional_center, Corner, Law_enforcement, Attorney, Psychologist, 
         Medical_Practitioner, Ombudsman, Public_Guardian, Other, Description_other,Reason))
        conn.commit()
    
    cursor.execute("SELECT * FROM consultation_information INNER JOIN cases on consultation_information.referral_id = cases.referral_id WHERE consultation_information.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    
    content = {}
    content["Services"] = data[2]
    content["GENESIS"] = data[3]
    content["DA"] = data[4]
    content["Regional_center"] = data[5]
    content["Corner"] = data[6]
    content["Law_enforcement"] = data[7]
    content["Attorney"] = data[8]
    content["Psychologist"] = data[9]
    content["Medical_Practitioner"] = data[10]
    content["Ombudsman"] = data[11]
    content["Public_Guardian"] = data[12]
    content["Other"] = data[13]
    content["Description_other"] = data[14]
    content["Reason"] = data[15]
    
    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']
    if data == None:
        return render_template('error_handling.html')
    if request.method == "POST":
        return render_template('consultation.html',referral_id = referral_id, **content)

    return render_template('consultation.html',referral_id = referral_id, **content)


@app.route('/notes/<int:referral_id>',methods =["GET", "POST"])
def notes(referral_id):
    
    # meeting_notes
    cursor.execute("SELECT * FROM meeting_notes INNER JOIN cases ON cases.referral_id =meeting_notes.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchall()
    note_num_db = len(data)
    #meeting_id = data[0]
    # goals
    cursor.execute("SELECT * FROM goals INNER JOIN cases ON cases.referral_id =goals.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data1 = cursor.fetchall()
    goal_num_db = len(data1)
    
    #referral_id = data1[1]
    # recommendations
    cursor.execute("SELECT * FROM recommendations INNER JOIN cases ON cases.referral_id =recommendations.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data2 = cursor.fetchall()
    #client_rec_id  = data2[0]
    action_num_db = len(data2)
    
  
    #print(action_num_db)
    
    if request.method == "POST":
        meeting_recs = ""
        fake_goals = ""
        
        # for loop get data - update note table
        for num in range(note_num_db):
        #     # meeting notes
            meeting_id = request.form.get("note_num_"+str(num+1))
            
            presenter = request.form.get("presenter_"+str(num+1))
            try:
                meeting_date = datetime.strptime(request.form.get("meeting_date_"+str(num+1)),'%Y-%m-%d')
            except:
                meeting_date = None
            meeting_notes = request.form.get("meeting_notes_"+str(num+1))
            # update
            cursor.execute("""UPDATE meeting_notes SET meeting_date = (%s),meeting_recs = (%s), meeting_goals = (%s) , 
            meeting_presenters = (%s), meeting_narrative = (%s) WHERE meeting_id = """ + str(meeting_id),(meeting_date, meeting_recs,fake_goals,presenter,meeting_notes))
            conn.commit()
        if request.form.get("note_num"):
            note_num = int(request.form.get("note_num"))
            for num in range(note_num_db+1,note_num+1):
                if request.form.get("new_presenter"+str(num)):
                    new_presenter = request.form.get("new_presenter"+str(num))
                    try:
                        new_date = datetime.strptime(request.form.get("new_meetingdate"+str(num)),'%Y-%m-%d')
                    except:
                        new_date = None
                    new_meeting_notes = request.form.get("new_meeting_note"+str(num))
                    # insert
                    sql = "INSERT INTO meeting_notes (referral_id,meeting_date,meeting_presenters,meeting_narrative) VALUES (%s, %s,%s, %s)"
                    val = (referral_id,new_date,new_presenter,new_meeting_notes)
                    cursor.execute(sql,val)
                    conn.commit()
        # update for goal

        for num in range(goal_num_db): #012
            goal = request.form.get("goals_"+str(num+1))
            goal_id = request.form.get("goal_num_"+str(num+1))
            cursor.execute("""UPDATE goals SET goal = (%s) WHERE client_goals_id = """ + str(goal_id),(goal))
            conn.commit()   
        if request.form.get("goal_num"):
            goal_num = int(request.form.get("goal_num"))
            for num in range(goal_num_db+1,goal_num+1):
                new_goal = request.form.get("new_goal"+str(num))
                if new_goal:
                    sql = "INSERT INTO goals(referral_id,goal) VALUES(%s,%s)"
                    val = (referral_id,new_goal)
                    cursor.execute(sql,val)
                    conn.commit()
        for num in range(action_num_db): 
            # update table
            action_step = request.form.get("action_step_"+str(num+1))
            person_response = request.form.get("person_response_"+str(num+1)) 
            
            if request.form.get("follow_up_"+str(num+1)):
                try:
                    follow_up = datetime.strptime(request.form.get("follow_up_"+str(num+1)),'%Y-%m-%d')
                except:
                    follow_up = None
                
            action_status = request.form.get("status_"+str(num+1))
            client_rec_id = request.form.get("action_num_"+str(num+1))
            cursor.execute("""UPDATE recommendations SET action_step = (%s), person_responsible = (%s), followup_date = (%s), action_status = (%s) WHERE client_rec_id = """ + str(client_rec_id),(action_step,person_response,follow_up,action_status))
            conn.commit()

        # insert for recommendations
        if request.form.get("rec_num"):
            action_num = int(request.form.get("rec_num"))
            # Insert
            for num in range(action_num_db+1,action_num+1):
                if request.form.get("new_step"+str(num)):
                    # only update if the row count exists
                    new_step = request.form.get("new_step"+str(num))
                    new_response = request.form.get("new_response"+str(num))
                    try:
                        new_follow =  datetime.strptime(request.form.get("new_follow"+str(num)),'%Y-%m-%d')
                    except:
                        # modified, default: today
                        new_follow = datetime.strptime("0001-01-01",'%Y-%m-%d')
                    new_status = request.form.get("new_status"+str(num))
                    sql = "INSERT INTO recommendations(referral_id,action_step,person_responsible,followup_date,action_status) VALUES(%s,%s,%s,%s,%s)"
                    val = (referral_id,new_step,new_response,new_follow,new_status)
                    cursor.execute(sql,val)
                    conn.commit()

    # goal
    cursor.execute("SELECT * FROM goals INNER JOIN cases ON cases.referral_id = goals.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    #data3 = cursor.fetchone()
    columns = [col[0] for col in cursor.description]
    goals= [dict(zip(columns, row)) for row in cursor.fetchall()]
    data3 = cursor.fetchall()

    content = {}
    goalarr = []
    notearr = []
     

    for row in data3:
        goalarr.append(row[2])
   
    #content["goals"] = goalarr
    #content["goals"] = data3[2]# goals.goal

    # meeting_notes
    cursor.execute("SELECT * FROM meeting_notes INNER JOIN cases ON cases.referral_id = meeting_notes.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    columns = [col[0] for col in cursor.description]
    meeting_notes = [dict(zip(columns, row)) for row in cursor.fetchall()]
   
    

    # recommendations
    cursor.execute("SELECT * FROM recommendations INNER JOIN cases ON cases.referral_id = recommendations.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    columns = [col[0] for col in cursor.description]

    recommendations = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']

    if len(data) == 0:
        #print("no data")
        return render_template('error_handling.html')
    if request.method == "POST":
        return render_template('notes.html', referral_id = referral_id, **content,goals = goals, meeting_notes = meeting_notes,recommendations = recommendations)
    
    return render_template('notes.html',referral_id = referral_id, **content,goals = goals,meeting_notes = meeting_notes, recommendations= recommendations)



@app.route('/attachments/<int:referral_id>',methods =["GET", "POST"])
def attachments(referral_id):
    content = dict()
    content['searchCase'] = True
    barinfo = getBarInfo(referral_id,cursor,conn)
    content['bar_urgentstatus'] = barinfo['status_urgent']
    content['bar_routinestatus'] = barinfo['status_routine']
    content['bar_caseclosed'] = barinfo['case_closed']
    content['bar_date'] = barinfo['case_date']
    content['bar_case_number'] = barinfo['case_number']

    UPLOAD_FOLDER = 'uploads/' + str(referral_id) + '/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # print(UPLOAD_FOLDER)
    if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    sql_attachments = """
    SELECT
	    file_path
    FROM
	    attachments
    WHERE
	referral_id = 
        """ + str(referral_id)
    cursor.execute(sql_attachments)
    data = cursor.fetchall()
    print("data: " + str(data))

    attachments = []
    for itemori in data:
            item = convertNonetoNull(itemori)
            dic = dict()
            dic["name"] = str(item[0]).split('/')[2]
            attachments.append(dic)
            print ("Result: " + str(attachments))
    
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            message = "No selected file"
            return render_template('attachments.html', referral_id = referral_id, **content, message = message, attachments = attachments)
        if not(file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            message = "file format is not allowed, please upload .txt, .pdf, .png, .jpg, .jpeg or .gif file."
            return render_template('attachments.html', referral_id = referral_id, **content, message = message, attachments = attachments)
        else:
            # case_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(referral_id))
            # if not os.path.isdir(UPLOAD_FOLDER):
            #     os.mkdir(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            file_path = UPLOAD_FOLDER + file.filename
            print(file_path)
            sql = """INSERT INTO attachments(referral_id, file_path) VALUES (%s, %s)"""
            val = (referral_id, file_path)
            cursor.execute(sql, val)
            conn.commit()
            message = "file uploaded successfully : " + file.filename
            return render_template('attachments.html', referral_id = referral_id, **content, message = message, attachments = attachments)
    
    return render_template('attachments.html', referral_id = referral_id, **content, attachments = attachments)

@app.route('/uploads/<int:referral_id>')
def download_file(name):
    print(name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/download')
def download():
    path = 'samplefile.pdf'
    return send_file(path, as_attachment=True)

@app.route('/import_case',methods =["GET", "POST"])
def import_case():
     if request.method == 'POST':
         f = request.files['file']
         file = 'files/' + f.filename
         file_extension = pathlib.Path(file).suffix

         if not(file_extension.endswith(".docx" or ".doc")):
             content = "Please choose the standardized Microsoft Form to create a new case."
             return render_template('import_case.html', content = content)
         else:
             f.save((file))
             print("file uploaded successfully")
             content = "file uploaded successfully : " + file
             doc = worddocparser.docx2python(file).text
             r_id = -1
             try:
                r_id = docToSql.mapToObj(doc, cursor, conn)
                return render_template('import_case.html', content = content,referral_id = r_id)
             except:
                content = "Please choose the standardized Microsoft Form to create a new case."
                return render_template('import_case.html', content = content)

     return render_template('import_case.html')

@app.route('/import_excel',methods =["GET", "POST"])
def import_excel():
    show_results= 0
    if request.method == 'POST':
        f = request.files['file']
        file = 'files/' + f.filename
        file_extension = pathlib.Path(file).suffix

        if not(file_extension.endswith(".xlsx") or file_extension.endswith(".xls")):
            content = "NOT VALID FILE PROVIDED! CHECK YOUR EXCEL FILE!"
            show_results=1
            #flash(u'Invalid file provided', 'error')
            return render_template('import_excel.html', content = content, show_results = show_results)
        else:
             
            show_results=2
            f.save((file))
            content = pd.read_excel(file)

            #return render_template('import_excel.html', content = content)
            # cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0;")
            # conn.commit()

            excel_file = pd.ExcelFile(file)
            try:
                # check excel format
                # client_sheet
                client_col = list(content.columns.values)
                client_col_true = ['referral_id', 'status_urgent', 'status_routine', 'case_date', 'case_number', 'consult_aps', 'consult_genesis', 'consult_district_att', 'consult_regional', 'consult_coroner', 'consult_law_enf', 'consult_att_oth', 'consult_psychologist', 'consult_physician', 'consult_ombudsman', 'consult_pub_guard', 'consult_other', 'consult_other_desc', 'consult_reason', 'case_closed', 'ra_case_no', 'ra_fname', 'ra_lname', 'ra_name_list', 'ra_fc_team', 'ra_fc_other', 'ra_email', 'ra_ph_office', 'ra_fx_office', 'ra_ph_mobile', 'ra_supervisor_name', 'cl_name_first', 'cl_name_last', 'cl_name_list', 'cl_age', 'cl_DOB', 'cl_language', 'cl_TransComm', 'cl_education', 'cl_ethnicity', 'cl_gender', 'cl_marital', 'cl_address', 'cl_city', 'cl_zip', 'cl_phone', 'cl_phys_name', 'cl_phys_ph', 'cl_insurance', 'cl_medications', 'cl_Illnesses', 'cl_functional_status', 'cl_cognitive_status', 'cl_living_setting', 'cl_lives_with', 'cl_lives_with_desc', 'cl_prev_abuse_no', 'cl_prev_abuse_yes', 'cl_prev_abuse_desc', 'cl_multiple_suspects', 'ad_InvAgencies', 'ad_RptingParty', 'ad_Others', 'ad_Abandon', 'ad_Abduction', 'ad_Emotional', 'ad_FinanRlEst', 'ad_FinanOth', 'ad_FinanLoss', 'ad_Isolation', 'ad_Sexual', 'ad_SelfNeglec', 'ad_NeglectOth', 'ad_PhyAssault', 'ad_PhyChemRst', 'ad_PhyCnstDpr', 'ad_PhyMedicat', 'ad_UndueInflu', 'ad_Other', 'ad_Narrative', 'oc_cp_arrest', 'oc_cp_hospital', 'oc_ev_geri', 'oc_ev_neuro', 'oc_ev_mental', 'oc_ev_law', 'oc_ss_support', 'oc_ss_compAPS', 'oc_ss_civil', 'oc_ap_freeze', 'oc_ap_other', 'oc_ap_restitution', 'oc_pr_charges', 'oc_pr_legal', 'oc_narrative', 'oc_self_suff', 'attachments', 'oc_csv_probate', 'oc_csv_lps', 'oc_csv_temp', 'oc_csv_pubg', 'oc_csv_priv', 'oc_csv_ext', 'oc_csv_name', 'oc_sa', 'oc_ro', 'oc_ro_name']
                # meeting_sheet
                excel_meeting = excel_file.parse(sheet_name="Meeting_Notes")
                meeting_col = list(excel_meeting.columns.values)
                meeting_col_true = ['referral_id', 'meeting_id', 'meeting_date', 'meeting_narrative', 'meeting_recs', 'meeting_goals', 'meeting_presenters']
                # recommendation sheet
                excel_recommendation = excel_file.parse(sheet_name = "Recommendations")
                recommendation_col = list(excel_recommendation.columns.values)
                recommendation_col_true = ['client_rec_id', 'referral_id', 'action_step', 'person_responsible', 'followup_date', 'action_status']
                # suspect sheet
                excel_suspect = excel_file.parse(sheet_name = "Suspect")
                suspect_col = list(excel_suspect.columns.values)
                
                suspect_col_true = ['referral_id', 'su_id', 'su_name_first', 'su_name_last', 'su_organization', 'su_name_list', 'su_age', 'su_DOB', 'su_ethnicity', 'su_gender', 'su_language', 'su_TransComm', 'su_PrimCrGvYES', 'su_PrimCrGvNO', 'su_LivesWthYES', 'su_relationship', 'su_LivesWthNO', 'su_mental_ill', 'su_mental_ill_desc', 'su_AdAlchlYES', 'su_AdAlchlNO', 'su_AdAlchlUNK', 'su_AdDrugsYES', 'su_AdDrugsNO', 'su_AdDrugsUNK', 'su_AdPrepYES', 'su_AdPrepNO', 'su_AdPrepUNK', 'su_AdOther', 'su_address', 'su_city', 'su_zip', 'su_phone']
                # goals sheet
                excel_goals = excel_file.parse(sheet_name = "Goals")
                goal_col = list(excel_goals.columns.values)
                goal_col_true = ['client_goals_id', 'referral_id', 'goal']

                if (client_col!=client_col_true or meeting_col!=meeting_col_true or recommendation_col!=recommendation_col_true or suspect_col!=suspect_col_true or goal_col!=goal_col_true):
                    show_results = 3
                    content = "Please check your format of excel file"
                    return render_template('import_excel.html',show_results = show_results, content = content)
            except:
                show_results = 3
                content = "Please check your format of excel file"
                return render_template('import_excel.html',show_results = show_results, content = content)
            '''
            meeting_notes 
            '''
           
            meeting_df = excel_meeting[['meeting_id','referral_id','meeting_date','meeting_narrative','meeting_recs','meeting_goals','meeting_presenters']]
            # Truncate table first
            cursor.execute("Truncate table meeting_notes;")
            conn.commit()
            
            meeting_df = meeting_df.where(pd.notnull(meeting_df), None)

            for index,row in meeting_df.iterrows():
                meeting_id = row['meeting_id']
                referral_id = row['referral_id']
                meeting_date  = row['meeting_date']
                meeting_narrative = row['meeting_narrative']
                meeting_recs = row['meeting_recs']
                meeting_goals = row['meeting_goals']
                meeting_presenters = row['meeting_presenters']
                sql = """INSERT INTO meeting_notes(meeting_id,referral_id,meeting_date,meeting_narrative,meeting_recs,meeting_goals,meeting_presenters)VALUES
                (%s,%s,%s,%s,%s,%s,%s)"""
                val = (meeting_id,referral_id,meeting_date,meeting_narrative,meeting_recs,meeting_goals,meeting_presenters)
                cursor.execute(sql,val)
                conn.commit()

            '''
            recommendation
            '''
            cursor.execute("Truncate table recommendations;")
            conn.commit()
            recommendation_df = excel_recommendation[['client_rec_id','referral_id','action_step',	'person_responsible',	'followup_date',	'action_status']]
            recommendation_df = recommendation_df.where(pd.notnull(recommendation_df), None)
            recommendation_df['followup_date'] = recommendation_df['followup_date'].astype('str')
            recommendation_df.replace({'NaT': None}, inplace=True)
            for index,row in recommendation_df.iterrows():
                client_rec_id = row['client_rec_id']
                referral_id = row['referral_id']
                action_step  = row['action_step']
                person_responsible = row['person_responsible']
                followup_date = row['followup_date']
                action_status = row['action_status']
                sql = """INSERT INTO recommendations(client_rec_id,referral_id,action_step,person_responsible,followup_date,action_status)VALUES
                (%s,%s,%s,%s,%s,%s)"""
                val = (client_rec_id,referral_id,action_step,person_responsible,followup_date,action_status)
                cursor.execute(sql,val)
                conn.commit()
            
            
            '''
            Goal
            '''         
            goals_df = excel_goals[['client_goals_id','referral_id','goal']]
            cursor.execute("Truncate table goals;")
            conn.commit()
            
            goals_df = goals_df.where(pd.notnull(goals_df), None)

            for index,row in goals_df.iterrows():
                client_goals_id = row['client_goals_id']
                referral_id = row['referral_id']
                goal = row['goal']
                sql = """INSERT INTO goals(client_goals_id,referral_id,goal)VALUES(%s,%s,%s)"""
                val = (client_goals_id,referral_id,goal)
                cursor.execute(sql,val)
                conn.commit()
            
            '''
            Suspect
            ''' 
            suspect_df = excel_suspect[[
                'su_id',
                'referral_id',
                'su_name_first',
                'su_name_last' ,
                'su_organization',
                'su_name_list',
                'su_age',
                'su_DOB',
                'su_ethnicity' ,
                'su_gender' ,
                'su_language' ,
                'su_TransComm' ,
                'su_PrimCrGvYES' ,
                'su_PrimCrGvNO' ,
                'su_LivesWthYES' ,
                'su_relationship' ,
                'su_LivesWthNO' ,
                'su_mental_ill' ,
                'su_mental_ill_desc' ,
                'su_AdAlchlYES' ,
                'su_AdAlchlNO' ,
                'su_AdAlchlUNK' ,
                'su_AdDrugsYES' ,
                'su_AdDrugsNO' ,
                'su_AdDrugsUNK' ,
                'su_AdPrepYES' ,
                'su_AdPrepNO' ,
                'su_AdPrepUNK' ,
                'su_AdOther' ,
                'su_address' ,
                'su_city' ,
                'su_zip' ,
                'su_phone' 
            ]]
            suspect_df = suspect_df.where(pd.notnull(suspect_df), None)
            # truncate table first
            cursor.execute( """TRUNCATE TABLE suspects;""")
            conn.commit()
            # insert by row
            for index,row in suspect_df.iterrows():
                referral_id = row['referral_id']
                su_name_first = row['su_name_first']
                su_name_last = row['su_name_last']
                su_organization = row['su_organization']
                su_name_list = row['su_name_list']
                su_age = row['su_age']
                su_DOB = row['su_DOB']
                su_ethnicity = row['su_ethnicity']
                su_gender = row['su_gender']
                su_language = row['su_language']
                su_TransComm = row['su_TransComm']
                su_PrimCrGvYES = row['su_PrimCrGvYES']
                su_PrimCrGvNo = row['su_PrimCrGvNO']
                su_LivesWthYES = row['su_LivesWthYES']
                su_relationship = row['su_relationship']
                su_LivesWthNO = row['su_LivesWthNO']
                su_mental_ill = row['su_mental_ill']
                su_mental_ill_desc = row['su_mental_ill_desc']
                su_AdAlchlYES = row['su_AdAlchlYES']
                su_AdAlchlNO = row['su_AdAlchlNO']
                su_AdAlchlUNK = row['su_AdAlchlUNK']
                su_AdDrugsYES = row['su_AdDrugsYES']
                su_AdDrugsNO = row['su_AdDrugsNO']
                su_AdDrugsUNK = row['su_AdDrugsUNK']
                su_AdPrepYES = row['su_AdPrepYES']
                su_AdPrepNO = row['su_AdPrepNO']
                su_AdPrepUNK = row['su_AdPrepUNK']
                su_AdOther = row['su_AdOther']
                su_address = row['su_address']
                su_city = row['su_city']
                su_zip = row['su_zip']
                su_phone = row['su_phone']
                sql = """INSERT INTO suspects (referral_id, su_name_first, su_name_last, su_organization, su_name_list, su_age, su_DOB, 
                su_ethnicity, su_gender, su_language, su_TransComm, su_PrimCrGvYES, su_PrimCrGvNo, su_LivesWthYES, su_relationship, su_LivesWthNO, su_mental_ill, 
                su_mental_ill_desc, su_AdAlchlYES, su_AdAlchlNO, su_AdAlchlUNK, su_AdDrugsYES, su_AdDrugsNO, su_AdDrugsUNK, su_AdPrepYES, su_AdPrepNO, su_AdPrepUNK,
                su_AdOther, su_address, su_city, su_zip, su_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (referral_id, su_name_first, su_name_last, su_organization, su_name_list, (su_age), (su_DOB), 
                su_ethnicity, su_gender, su_language, su_TransComm, su_PrimCrGvYES, su_PrimCrGvNo, su_LivesWthYES, su_relationship, su_LivesWthNO, su_mental_ill, 
                su_mental_ill_desc, su_AdAlchlYES, su_AdAlchlNO, su_AdAlchlUNK, su_AdDrugsYES, su_AdDrugsNO, su_AdDrugsUNK, su_AdPrepYES, su_AdPrepNO, su_AdPrepUNK,
                su_AdOther, su_address, su_city, su_zip, su_phone)
                cursor.execute(sql, val)
                conn.commit()


            '''
            Client
            '''

            excel_client  = excel_file.parse(sheet_name="Client")
            client_df = excel_client [[
                'referral_id' ,
                'cl_name_first' ,
                'cl_name_last' ,
                'cl_name_list' ,
                'cl_age',
                'cl_DOB',
                'cl_language' ,
                'cl_TransComm' ,
                'cl_education' ,
                'cl_ethnicity' ,
                'cl_gender' ,
                'cl_marital' ,
                'cl_address' ,
                'cl_city' ,
                'cl_zip' ,
                'cl_phone' ,
                'cl_phys_name' ,
                'cl_phys_ph' ,
                'cl_insurance' ,
                'cl_medications' ,
                'cl_Illnesses' ,
                'cl_functional_status' ,
                'cl_cognitive_status' ,
                'cl_living_setting' ,
                'cl_lives_with' ,
                'cl_lives_with_desc' ,
                'cl_prev_abuse_no' ,
                'cl_prev_abuse_yes' ,
                'cl_prev_abuse_desc' ,
                'cl_multiple_suspects' 


            ]]
            
            
            client_df = client_df.where(pd.notnull(client_df), None)
            
           
            client_df['cl_DOB'] = client_df['cl_DOB'].astype('str')
            client_df.replace({'NaT': None}, inplace=True)
            # truncate first
            cursor.execute("""TRUNCATE TABLE clients;""")
            conn.commit()
            for index,row in client_df.iterrows():
                referral_id = row['referral_id']
                cl_name_first = row['cl_name_first']
                cl_name_last = row['cl_name_last']
                cl_name_list = row['cl_name_list']
                cl_age = row['cl_age']
                cl_DOB = row['cl_DOB']
                cl_language = row['cl_language']
                cl_TransComm = row['cl_TransComm']
                cl_education = row['cl_education']
                cl_ethnicity = row['cl_ethnicity']
                cl_gender = row['cl_gender']
                cl_marital = row['cl_marital']
                cl_address = row['cl_address']
                cl_city = row['cl_city']
                cl_zip = row['cl_zip']
                cl_phone = row['cl_phone']
                cl_phys_name = row['cl_phys_name']
                cl_phys_ph = row['cl_phys_ph']
                cl_insurance = row['cl_insurance']
                cl_medications = row['cl_medications']
                cl_Illnesses = row['cl_Illnesses']
                cl_functional_status = row['cl_functional_status']
                cl_cognitive_status = row['cl_cognitive_status']
                cl_living_setting = row['cl_living_setting']
                cl_lives_with = row['cl_lives_with']
                cl_lives_with_desc = row['cl_lives_with_desc']
                cl_prev_abuse_no = row['cl_prev_abuse_no']
                cl_prev_abuse_yes = row['cl_prev_abuse_no']
                cl_prev_abuse_desc = row['cl_prev_abuse_desc']
                cl_multiple_suspects = row['cl_multiple_suspects']

                # insert
                sql = """INSERT INTO clients(                    
                referral_id ,
                cl_name_first,
                cl_name_last ,
                cl_name_list,
                cl_age,
                cl_DOB,
                cl_language,
                cl_TransComm,
                cl_education,
                cl_ethnicity,
                cl_gender,
                cl_marital,
                cl_address,
                cl_city,
                cl_zip,
                cl_phone,
                cl_phys_name,
                cl_phys_ph,
                cl_insurance,
                cl_medications,
                cl_Illnesses,
                cl_functional_status,
                cl_cognitive_status,
                cl_living_setting,
                cl_lives_with,
                cl_lives_with_desc,
                cl_prev_abuse_no,
                cl_prev_abuse_yes,
                cl_prev_abuse_desc,
                cl_multiple_suspects) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                val = (
                        referral_id ,
                        cl_name_first,
                        cl_name_last ,
                        cl_name_list,
                        cl_age,
                        cl_DOB,
                        cl_language,
                        cl_TransComm,
                        cl_education,
                        cl_ethnicity,
                        cl_gender,
                        cl_marital,
                        cl_address,
                        cl_city,
                        cl_zip,
                        cl_phone,
                        cl_phys_name,
                        cl_phys_ph,
                        cl_insurance,
                        cl_medications,
                        cl_Illnesses,
                        cl_functional_status,
                        cl_cognitive_status,
                        cl_living_setting,
                        cl_lives_with,
                        cl_lives_with_desc,
                        cl_prev_abuse_no,
                        cl_prev_abuse_yes,
                        cl_prev_abuse_desc,
                        cl_multiple_suspects
                     )
                cursor.execute(sql,val)
                conn.commit()

            '''
            case_number
            '''
            cursor.execute("Truncate table case_number;")
            conn.commit()
            case_number_df = excel_client[['case_number','referral_id']]
            #case_number_df.to_sql(name='case_number',con = engine ,if_exists = 'replace', index = False)
            for index,row in case_number_df.iterrows():
                referral_id = row['referral_id']
                case_number = row['case_number']
                sql = """INSERT INTO case_number(case_number,referral_id) VALUES(%s,%s)"""
                val = (case_number,referral_id)
                cursor.execute(sql,val)
                conn.commit()
                # else:
                #     cursor.execute("""SET FOREIGN_KEY_CHECKS=0;""")
                #     conn.commit()
                #     cursor.execute("""UPDATE case_number SET case_number = (%s), referral_id = (%s) WHERE referral_id = """+str(referral_id),(case_number,referral_id))
                #     conn.commit()
            
            '''
            cases 
            '''

            cases_df = excel_client[[
                
                'referral_id' ,
                'status_urgent' ,
                'status_routine',
                'case_date' ,
                'case_closed' 

            ]]
            cases_df = cases_df.where(pd.notnull(cases_df), None)
            for index,row in cases_df.iterrows():
                referral_id = row['referral_id']
                status_urgent = bool(row['status_urgent'])
                status_routine = bool(row['status_routine'])
                case_date = row['case_date']
                case_closed = bool(row['case_closed'])
                cursor.execute ("""SELECT referral_id from cases""")
                
               
                ref_id = [i[0] for i in cursor.fetchall()]
                
                
                if referral_id in ref_id:
                    cursor.execute("""UPDATE cases SET status_urgent = (%s),status_routine=(%s),case_date=(%s),case_closed=(%s) WHERE referral_id = """+str(referral_id),(status_urgent,status_routine,case_date,case_closed))
                    #print("update "+str(referral_id))
                    conn.commit()
                else:
                    
                    sql = """INSERT INTO cases VALUES(%s,%s,%s,%s,%s)"""
                    val = (referral_id,status_urgent,status_routine,case_date,case_closed)
                    #print("insert "+referral_id)
                    cursor.execute(sql,val)
                    conn.commit()

            '''
            abuse-information
            '''
            abuse_df = excel_client[[
                'referral_id' ,
                'ad_InvAgencies' ,
                'ad_RptingParty' ,
                'ad_Others' ,
                'ad_Abandon' ,
                'ad_Abduction' ,
                'ad_Emotional' ,
                'ad_FinanRlEst' ,
                'ad_FinanOth' ,
                'ad_FinanLoss' , 
                'ad_Isolation' ,
                'ad_Sexual' ,
                'ad_SelfNeglec' ,
                'ad_NeglectOth' ,
                'ad_PhyAssault' ,
                'ad_PhyChemRst' ,
                'ad_PhyCnstDpr' ,
                'ad_PhyMedicat' ,
                'ad_UndueInflu' ,
                'ad_Other' ,
                'ad_Narrative' 
            ]]
            abuse_df = abuse_df.where(pd.notnull(abuse_df), None)
            
            cursor.execute("Truncate table abuse_information;")
            conn.commit()      
            
            for index,row in abuse_df.iterrows():
                referral_id = row['referral_id']
                ad_InvAgencies = row['ad_InvAgencies']
                ad_RptingParty = row['ad_RptingParty']
                ad_Others = row['ad_Others']
                ad_Abandon = row['ad_Abandon']
                ad_Abduction = row['ad_Abduction']
                ad_Emotional = row['ad_Emotional']
                ad_FinanRlEst = row['ad_FinanRlEst']
                ad_FinanOth = row['ad_FinanOth']
                ad_FinanLoss = row['ad_FinanLoss'] 
                ad_Isolation = row['ad_Isolation']
                ad_Sexual = row['ad_Sexual']
                ad_SelfNeglec = row['ad_SelfNeglec']
                ad_NeglectOth = row['ad_NeglectOth']
                ad_PhyAssault = row['ad_PhyAssault']
                ad_PhyChemRst = row['ad_PhyChemRst']
                ad_PhyCnstDpr = row['ad_PhyCnstDpr']
                ad_PhyMedicat = row['ad_PhyMedicat']
                ad_UndueInflu = row['ad_UndueInflu']
                ad_Other = row['ad_Other']
                ad_Narrative = row['ad_Narrative']                
                   
                sql = """INSERT INTO abuse_information (referral_id, ad_InvAgencies, ad_RptingParty, ad_Others, ad_Abandon, ad_Abduction, 
                ad_Emotional, ad_FinanRlEst, ad_FinanOth, ad_FinanLoss,ad_Isolation, ad_Sexual, ad_SelfNeglec, ad_NeglectOth, ad_PhyAssault, 
                ad_PhyChemRst, ad_PhyCnstDpr, ad_PhyMedicat, ad_UndueInflu, ad_Other, ad_Narrative) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s)"""
                val = (referral_id, ad_InvAgencies, ad_RptingParty, ad_Others, ad_Abandon, ad_Abduction, 
                ad_Emotional, ad_FinanRlEst, ad_FinanOth, ad_FinanLoss,ad_Isolation, ad_Sexual, ad_SelfNeglec, ad_NeglectOth, ad_PhyAssault, 
                ad_PhyChemRst, ad_PhyCnstDpr, ad_PhyMedicat, ad_UndueInflu, ad_Other, ad_Narrative)
                cursor.execute(sql, val)
                conn.commit()

            '''
            outcome
            '''
            outcome_df = excel_client[[
                'referral_id' ,
                'oc_cp_arrest' ,
                'oc_cp_hospital' ,
                'oc_ev_neuro' ,
                'oc_ev_mental' ,
                'oc_ev_law' ,
                'oc_ss_support' ,
                'oc_ss_compAPS' ,
                'oc_ss_civil' ,
                'oc_ap_freeze' ,
                'oc_ap_other' ,
                'oc_ap_restitution' ,
                'oc_pr_charges' ,
                'oc_pr_legal' ,
                'oc_narrative' ,
                'oc_csv_probate' ,
                'oc_csv_lps' , 
                'oc_csv_temp' ,
                'oc_csv_pubg' ,
                'oc_csv_priv' ,
                'oc_csv_ext' ,
                'oc_csv_name' ,
                'oc_sa' ,
                'oc_ro' ,
                'oc_ro_name' ,
                'oc_ev_geri' ,
                'oc_self_suff' 

            ]]
            outcome_df = outcome_df.where(pd.notnull(outcome_df), None)
            # TRUNCATE
            cursor.execute("Truncate table outcome;")
            conn.commit()
            # sql to insert or update
            for index, row in outcome_df.iterrows():
                referral_id  = row['referral_id']
                oc_cp_arrest = row['oc_cp_arrest']
                oc_cp_hospital = row['oc_cp_hospital']
                oc_ev_neuro = row['oc_ev_neuro']
                oc_ev_mental = row['oc_ev_mental']
                oc_ev_law = row['oc_ev_law']
                oc_ss_support = row['oc_ss_support']
                oc_ss_compAPS = row['oc_ss_compAPS']
                oc_ss_civil = row['oc_ss_civil']
                oc_ap_freeze = row['oc_ap_freeze']
                oc_ap_other = row['oc_ap_other']
                oc_ap_restitution = row['oc_ap_restitution']
                oc_pr_charges = row['oc_pr_charges']
                oc_pr_legal = row['oc_pr_legal']
                oc_narrative = row['oc_narrative']
                oc_csv_probate = row['oc_csv_probate']
                oc_csv_lps = row['oc_csv_lps']
                oc_csv_temp = row['oc_csv_temp']
                oc_csv_pubg = row['oc_csv_pubg']
                oc_csv_priv = row['oc_csv_priv']
                oc_csv_ext = row['oc_csv_ext']
                oc_csv_name = row['oc_csv_name']
                oc_sa = row['oc_sa']
                oc_ro = row['oc_ro']
                oc_ro_name = row['oc_ro_name']
                oc_ev_geri = row['oc_ev_geri']
                oc_self_suff = row['oc_self_suff']

                # INSERT
                sql="""INSERT INTO outcome(referral_id,                
                        oc_cp_arrest,
                        oc_cp_hospital,
                        oc_ev_neuro,
                        oc_ev_mental,
                        oc_ev_law,
                        oc_ss_support,
                        oc_ss_compAPS,
                        oc_ss_civil,
                        oc_ap_freeze,
                        oc_ap_other,
                        oc_ap_restitution,
                        oc_pr_charges,
                        oc_pr_legal,
                        oc_narrative,
                        oc_csv_probate,
                        oc_csv_lps,
                        oc_csv_temp,
                        oc_csv_pubg,
                        oc_csv_priv,
                        oc_csv_ext,
                        oc_csv_name,
                        oc_sa,
                        oc_ro,
                        oc_ro_name,
                        oc_ev_geri,
                        oc_self_suff)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
                val = (
                        referral_id,                
                        oc_cp_arrest,
                        oc_cp_hospital,
                        oc_ev_neuro,
                        oc_ev_mental,
                        oc_ev_law,
                        oc_ss_support,
                        oc_ss_compAPS,
                        oc_ss_civil,
                        oc_ap_freeze,
                        oc_ap_other,
                        oc_ap_restitution,
                        oc_pr_charges,
                        oc_pr_legal,
                        oc_narrative,
                        oc_csv_probate,
                        oc_csv_lps,
                        oc_csv_temp,
                        oc_csv_pubg,
                        oc_csv_priv,
                        oc_csv_ext,
                        oc_csv_name,
                        oc_sa,
                        oc_ro,
                        oc_ro_name,
                        oc_ev_geri,
                        oc_self_suff 
                       )

            '''
            referring_agency
            '''
            referring_df = excel_client[[
                'referral_id' ,
                'ra_fname' ,
                'ra_lname' ,
                'ra_name_list' ,
                'ra_fc_team' ,
                'ra_fc_other' ,
                'ra_email' ,
                'ra_ph_office' ,
                'ra_fx_office' ,
                'ra_ph_mobile' ,
                'ra_supervisor_name'

            ]]
            referring_df = referring_df.where(pd.notnull(referring_df), None)
            cursor.execute("Truncate table referring_agency;")
            conn.commit()
            for index, row in referring_df.iterrows():
                referral_id  = row['referral_id']
                ra_fname  = row['ra_fname']
                ra_lname = row['ra_lname']
                ra_name_list = row['ra_name_list']
                ra_fc_team = row['ra_fc_team']
                ra_fc_other = row['ra_fc_other']
                ra_email = row['ra_email']
                ra_ph_office = row['ra_ph_office']
                ra_fx_office = row['ra_fx_office']
                ra_ph_mobile = row['ra_ph_mobile']
                ra_supervisor_name = row['ra_supervisor_name']   
  
                sql = """INSERT INTO referring_agency(referral_id,
                        ra_fname ,
                        ra_lname ,
                        ra_name_list ,
                        ra_fc_team ,
                        ra_fc_other ,
                        ra_email ,
                        ra_ph_office ,
                        ra_fx_office ,
                        ra_ph_mobile ,
                        ra_supervisor_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                val = (referral_id,
                        ra_fname ,
                        ra_lname ,
                        ra_name_list ,
                        ra_fc_team ,
                        ra_fc_other ,
                        ra_email ,
                        ra_ph_office ,
                        ra_fx_office ,
                        ra_ph_mobile ,
                        ra_supervisor_name)
                cursor.execute(sql, val)
                conn.commit()
    
            '''
            consultation
            '''
            consultation_df = excel_client[[
                'referral_id' ,
                'consult_aps' ,
                'consult_genesis' ,
                'consult_district_att' ,
                'consult_regional' ,
                'consult_coroner' ,
                'consult_law_enf' ,
                'consult_att_oth' ,
                'consult_psychologist' ,
                'consult_physician' ,
                'consult_ombudsman' ,
                'consult_pub_guard' ,
                'consult_other' ,
                'consult_other_desc' ,
                'consult_reason' 

            ]]
            
            consultation_df = consultation_df.where(pd.notnull(consultation_df), None)
            cursor.execute("Truncate table consultation_information;")
            conn.commit()
            for index,row in consultation_df.iterrows():
                referral_id = row['referral_id']
                consult_aps = row['consult_aps']
                consult_genesis = row['consult_genesis']
                consult_district_att = row['consult_district_att']
                consult_regional = row['consult_regional']
                consult_coroner= row['consult_coroner']
                consult_law_enf = row['consult_law_enf']
                consult_att_oth = row['consult_att_oth']
                consult_psychologist = row['consult_psychologist']
                consult_physician = row['consult_physician']
                consult_ombudsman = row['consult_ombudsman']
                consult_pub_guard = row['consult_pub_guard']
                consult_other = row['consult_other']
                consult_other_desc = row['consult_other_desc']
                consult_reason = row['consult_reason']

                
                sql = """INSERT INTO consultation_information(referral_id, consult_aps, consult_genesis, consult_district_att, consult_regional, consult_coroner,
                consult_law_enf, consult_att_oth, consult_psychologist, consult_physician, consult_ombudsman, consult_pub_guard, consult_other, consult_other_desc,consult_reason) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                val = (referral_id, consult_aps, consult_genesis, consult_district_att, consult_regional, consult_coroner,
                consult_law_enf, consult_att_oth, consult_psychologist, consult_physician, consult_ombudsman, consult_pub_guard, consult_other, consult_other_desc,consult_reason)
                cursor.execute(sql, val)
                conn.commit()

            forward_message = "Insert successfully!"

            clients_res = client_df
            goals_res = goals_df
            rec_res = recommendation_df
            suspect_res = suspect_df
            meeting_res = meeting_df
            outcome_res = outcome_df
            abuse_res = abuse_df
            referring_res = referring_df
            consultation_res = consultation_df
        
            return render_template('import_excel.html', forward_message=forward_message, goals_res = goals_res,rec_res = rec_res ,
            suspect_res = suspect_res, meeting_res = meeting_res, clients_res = clients_res,consultation_res = consultation_res,
            outcome_res= outcome_res, abuse_res = abuse_res, referring_res = referring_res, content = content, show_results = show_results
            
            )

    return render_template('import_excel.html',show_results = show_results)


