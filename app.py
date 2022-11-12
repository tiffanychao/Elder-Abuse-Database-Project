import pathlib
from flask import Flask, render_template, request,flash
app = Flask(__name__)
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from getDataFromDB import *
import os #provides ways to access the Operating System and allows us to read the environment variables
# from mysql.connector import Error
# import mysql.connector
from datetime import datetime
# import pandas as pd
# import pathlib
# import worddocparser
# load_dotenv()  # take environment variables from .env.


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DatabaseUser")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DatabasePassword")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DatabaseDB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DatabaseHost")
# app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
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


@app.route('/client/<int:referral_id>', methods = ["POST", "GET"])
def client(referral_id):  
    # figure out the associated client ID of the referral_id
    cursor.execute("SELECT * FROM clients INNER JOIN cases ON cases.referral_id = clients.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    print(data)
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
         request.form.get("cl_marital"), request.form.get("cl_address"), request.form.get("cl_city"), 
         request.form.get("cl_zip"),request.form.get("cl_phone")))
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

    if request.method == "POST":
        return render_template('client.html',referral_id =referral_id, **content)
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
        return "There is no data sorry"
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
        return "There is no data sorry"
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
    dictInfo = get_referral_info_from_db(referral_id)
    dictInfo['referral_id'] = referral_id
    dictInfo['searchCase'] = True
    return render_template('referringAgency.html', **dictInfo)



    
@app.route('/case_summary/<referral_id>',methods =["GET", "POST"])
def case_summary(referral_id):
    if request.method == "POST":
       
        return  data1 
    # deal with the data
    #
    v_name = "John Doe"
    
    dic = get_case_summary_from_db(referral_id)
    dic['referral_id'] = referral_id
    # print(dic['notes'])
    print ("123")
    return render_template('caseSummary.html',**dic) 



@app.route('/search_cases',methods =["GET", "POST"])
def search_cases():
    delete_referal_id = -1
    search_type = ''
    first_name = ''
    last_name = ''
    case_closed = 0
    query = 0
    if request.method == "POST":
        if (request.form.get("deleteButton")):
            delete_referal_id = request.form.get("deleteButton")
            delete_case(delete_referal_id)
        
            
        search_type = request.form.get("searchType")
        print(search_type)
        first_name = request.form.get("FirstName")
        last_name =  request.form.get("LastName")
        if (request.form.get("closedCased")):
            case_closed = 1

        # print(case_closed)
    
    dic = dict()
    dic['firstName'] = first_name

   
    infolist = search_cases_from_database(search_type,first_name,last_name,case_closed)
    v_num = len(infolist)
    dic = dict()
    dic['searchType'] = search_type
    dic['firstName'] = first_name
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
    return render_template('example.html', value = variable)

@app.route('/narrative/<int:referral_id>',methods =["GET", "POST"])
def narrative(referral_id):
    cursor.execute("SELECT * FROM outcome INNER JOIN cases ON cases.referral_id = outcome.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    
    if request.method == "POST":
        oc_narrative = request.form.get("oc_narrative")
        cursor.execute("""UPDATE outcome SET  oc_narrative = (%s) WHERE referral_id = """ + str(referral_id),
         (oc_narrative))

        conn.commit()
        
    cursor.execute("SELECT * FROM outcome INNER JOIN cases ON cases.referral_id = outcome.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    content = {}
    content["oc_narrative"] = data[14]

    if data == None:
        return "Sorry your data isn't here"
    if request.method == "POST":
        return render_template('narrative.html',referral_id = referral_id, **content)
    return render_template('narrative.html',referral_id = referral_id, **content)


@app.route('/consultation/<int:referral_id>', methods =["GET", "POST"])
def consulation(referral_id):

    cursor.execute("SELECT * FROM consultation_information INNER JOIN cases ON cases.referral_id = consultation_information.referral_id WHERE cases.referral_id = " + str(referral_id) + ";")
    data = cursor.fetchone()
    consultation_id = data[0]
    
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
    content["Coroner"] = data[6]
    content["Law_enforcement"] = data[7]
    content["Attorney"] = data[8]
    content["Psychologist"] = data[9]
    content["Medical_Practitioner"] = data[10]
    content["Ombudsman"] = data[11]
    content["Public_Guardian"] = data[12]
    content["Other"] = data[13]
    content["Description_other"] = data[14]
    content["Reason"] = data[15]
    
    if data == None:
        return "Sorry your data isn't here"
    if request.method == "POST":
        return render_template('consultation.html',referral_id = referral_id, **content)

    return render_template('consultation.html',referral_id = referral_id, **content)


@app.route('/notes/<int:referral_id>',methods =["GET", "POST"])
def notes(referral_id):
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

        # for Goals - goals table
        cur = conn.cursor()
        cursor.execute("""UPDATE goals SET goal = (%s) WHERE client_goals_id = """ + str(client_goals_id),(goal))
        conn.commit()     
        # for recommendations
        cur = conn.cursor()
        cursor.execute("""UPDATE recommendations SET  action_step = (%s), person_responsible = (%s), followup_date = (%s), action_status = (%s) WHERE client_rec_id = """ + str(client_rec_id),(action_step,person_response,follow_up,action_status))
        conn.commit()


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
        return render_template('notes.html',referral_id = referral_id,  **content)

    return render_template('notes.html',referral_id = referral_id, **content)

@app.route('/attachments')
def attachments():
    variable = "check your name"
    return render_template('attachments.html', value = variable)

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
             print(worddocparser.docx2python(file).text)
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
            content = "NOT EXCEL!!!"
            show_results=1
            return render_template('import_excel.html', content = content, show_results = show_results)
        else:
            show_results=2
            f.save((file))
            content = pd.read_excel(file)
            #return render_template('import_excel.html', content = content)
            engine = create_engine(os.getenv("DatabaseEngine"))

            excel_file = pd.ExcelFile(file)
            '''
            test  - meeting_notes (use test table)
            '''
            excel_meeting = excel_file.parse(sheet_name="Meeting_Notes")
            meeting_df = excel_meeting[['referral_id','meeting_date','meeting_narrative','meeting_recs','meeting_goals','meeting_presenters']]
            meeting_df.to_sql(name = 'meeting_notes', con=engine, if_exists = 'append', index = False)

            '''
            test - recommendationsv
            '''
            excel_recommendation = excel_file.parse(sheet_name = "Recommendations")
            recommendation_df = excel_recommendation[['referral_id','action_step',	'person_responsible',	'followup_date',	'action_status']]
            recommendation_df.to_sql(name = 'recommendations', con=engine, if_exists = 'append', index = False)
            '''
            test - Goalsv
            '''

            excel_goals = excel_file.parse(sheet_name = "Goals")
            goals_df = excel_goals[['referral_id','goal']]
            goals_df.to_sql(name = 'goals', con=engine, if_exists = 'append', index = False)




            '''
            test - Suspectv
            '''


            excel_suspect = excel_file.parse(sheet_name = "Suspect")
            suspect_df = excel_suspect[[
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
            suspect_df.to_sql(name = 'suspects', con=engine, if_exists = 'append', index = False)



            '''
            test - Client
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
            client_df.to_sql(name='clients',con = engine ,if_exists = 'append', index = False)

            # replace or append?
            forward_message = "Insert successfully!"

            clients_res = client_df
            goals_res = goals_df
            rec_res = recommendation_df
            suspect_res = suspect_df
            meeting_res = meeting_df
        
            return render_template('import_excel.html', forward_message=forward_message, goals_res = goals_res,rec_res = rec_res ,
            suspect_res = suspect_res, meeting_res = meeting_res, clients_res = clients_res, content = content, show_results = show_results
            )

    return render_template('import_excel.html',show_results = show_results)


