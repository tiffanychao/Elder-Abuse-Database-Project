import re
from datetime import datetime
from sqlalchemy import DefaultClause

def mapToObj(input, cursor, conn): 
    print("Start From Here-------")
    list = []
    for line in input.splitlines():
        list.append(line)
    urgent = list[0].find("☐ Urgent") == -1
    routine = list[0].find("☐ Routine") == -1
    try:
        date = datetime.strptime(list[2].split()[1].strip(), '%m/%d/%Y').date()
    except:
        date = None
    caseNumber = list[4].split(':')[1].strip()
    # print("Urgent " + str(urgent) + " Routine " + str(routine) + " Date " + str(date) + " Case Number " + caseNumber)
    
    ## Insert Data into cases table, and get the Referal ID
    sql = """INSERT INTO cases (status_urgent, status_routine, case_date, case_closed) VALUES (%s, %s, %s, %s)"""
    val = (urgent, routine, date, False)
    cursor.execute(sql, val)
    conn.commit()
    referral_id = (cursor.lastrowid)
    print("Referral ID: " + str(referral_id))
    ## Insert Data into case number table
    sql = """INSERT INTO case_number (case_number, referral_id) VALUES (%s, %s)"""
    val = (caseNumber, referral_id)
    cursor.execute(sql, val)
    conn.commit()
    consult_aps = list[10].find("☐ Adult Protective Services") == -1
    consult_genesis = list[12].find("☐ Dept. Mental Health") == -1
    consult_district_att = list[14].find("☐ D.A.") == -1
    consult_regional = list[16].find("☐ Regional Center") == -1
    consult_coroner = list[18].find("☐ Coroner/ME") == -1
    consult_law_enf = list[20].find("☐ Law Enforcement") == -1
    consult_att_oth = list[22].find("☐ Attorney Other") == -1
    consult_psychologist = list[24].find("☐ Psychologist") == -1
    consult_physician = list[26].find("☐ Medical Practitioner") == -1
    consult_ombudsman = list[28].find("☐ Ombudsman") == -1
    consult_pub_guard = list[30].find("☐ Public Guardian") == -1
    consult_other = list[32].find("☐ Other") == -1
    consult_other_desc = list[32].split(':')[1]
    # print("Adult Protective Services: " + str(consult_aps) + " Dept. Mental Health " + str(consult_genesis) + " D.A. " + str(consult_district_att) +
    # " Regional Center " + str(consult_regional) + " Coroner/ME " + str(consult_coroner) + " Law Enforcement " + str(consult_law_enf) + " Attorney Other " + 
    # str(consult_att_oth) + " Psychologist " + str(consult_psychologist) + " Medical Practitioner  " + str(consult_physician) + " Ombudsman " +
    # str(consult_ombudsman) + " Public Guardian " + str(consult_pub_guard) + " Other " + str(consult_other) + " Other Describe " + str(consult_other_desc))

    ## Insert Data into consultation table
    sql = """INSERT INTO consultation_information(referral_id, consult_aps, consult_genesis, consult_district_att, consult_regional, consult_coroner,
    consult_law_enf, consult_att_oth, consult_psychologist, consult_physician, consult_ombudsman, consult_pub_guard, consult_other, consult_other_desc) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (referral_id, consult_aps, consult_genesis, consult_district_att, consult_regional, consult_coroner,
    consult_law_enf, consult_att_oth, consult_psychologist, consult_physician, consult_ombudsman, consult_pub_guard, consult_other, consult_other_desc)
    cursor.execute(sql, val)
    conn.commit()


    ra_fname = list[44].strip()
    ra_lname = list[46].strip()
    ra_name_list = ra_fname + " " + ra_lname
    ra_fc_team = re.split('(other)', list[48])[0].strip()
    ra_fc_other = list[48].split(':')[1].strip()
    ra_email = list[50].strip()
    ra_ph_office = list[60].strip()
    ra_fx_office = list[62].strip()
    ra_ph_mobile = list[64].strip()
    ra_supervisor_name = list[66].strip()
    # print("First Name: " + str(ra_fname) + " Last Nmae: " + str(ra_lname) + " FC Team Member: " + str(ra_fc_team) + " Other: " + str(ra_fc_other) + " Email: " + str(ra_email) + 
    # " Office Phone: " + str(ra_ph_office) + " Office Fax: " + str(ra_fx_office) + " Mobile Phone: " + str(ra_ph_mobile) + " Supervisor Name: " + str(ra_supervisor_name))

    ## Insert Data into referring agency table
    sql = """INSERT INTO referring_agency(referral_id, ra_fname, ra_lname, ra_name_list, ra_fc_team, ra_fc_other, ra_email, ra_ph_office, 
    ra_fx_office, ra_ph_mobile, ra_supervisor_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (referral_id, ra_fname, ra_lname, ra_name_list, ra_fc_team, ra_fc_other, ra_email, ra_ph_office, ra_fx_office, ra_ph_mobile, ra_supervisor_name)
    cursor.execute(sql, val)
    conn.commit()

    cl_name_first = list[82].strip()
    cl_name_last = list[84].strip()
    cl_name_list = cl_name_first + " " + cl_name_last
    cl_age = list[86].strip()
    try:
        cl_DOB = datetime.strptime(list[88].strip(), '%m/%d/%Y').date()
    except:
        cl_DOB = None
    cl_language = list[90].strip()
    cl_TransComm = list[92].strip()
    cl_education = list[102].strip()
    cl_ethnicity = list[104].strip()
    cl_gender = list[106].strip()
    cl_marital = list[108].strip()
    cl_address = list[118].strip()
    cl_city = list[120].strip()
    cl_zip = list[122].strip()
    cl_phone = list[124].strip()
    cl_phys_name = list[134].strip()
    cl_phys_ph = list[136].strip()
    cl_insurance = list[138].strip()
    cl_medications = list[142].strip()
    cl_Illnesses = list[148].strip()
    cl_functional_status = list[158].strip()
    cl_cognitive_status = list[160].strip()
    cl_living_setting = list[170].strip()
    cl_lives_with = list[172].split(')')[0]# check to edit
    if cl_lives_with == "Non-family (describe":
        cl_lives_with = "Non-family (describe)"
        cl_lives_with_desc = list[172].split(')')[1].strip()
    else:
        cl_lives_with_desc = ""
    cl_prev_abuse_no = list[176].find("☐  No") == -1
    cl_prev_abuse_yes = list[176].find("☐  Yes") == -1
    cl_prev_abuse_desc = re.split('explain', list[176])[1].strip()
    # print("First Name: " + str(cl_name_first) + " Last Nmae: " + str(cl_name_last) + " Age: " + str(cl_age) + " DOB: " + str(cl_DOB) + " Language: " + str(cl_language) + 
    # " Translation/Communication Needs: " + str(cl_TransComm) + " Level of Education: " + str(cl_education) + " Ethnicity: " + str(cl_ethnicity) + " Gender: " + str(cl_gender) +
    # " Marital Status: " + str(cl_marital) + " Address: " + str(cl_address) + " City: " + str(cl_city) + " Zip: " + str(cl_zip) +
    # " Telephone: " + str(cl_phone) + " Physician Name: " + str(cl_phys_name) + "  Physician Telephone: " + str(cl_phys_ph) + " Insurance: " + str(cl_insurance) + 
    # " Medications and Dosage: " + str(cl_medications) + " Illnesses and Addictions: " + str(cl_Illnesses) + "  Physical Functional Status: " + str(cl_functional_status) + 
    # " Cognitive Status: " + str(cl_cognitive_status) + " Living Setting: " + str(cl_living_setting) + " Lives With: " + str(cl_lives_with) + " Lives With: " + str(cl_lives_with_desc) +
    # " Previous Reports of Abuse No: " + str(cl_prev_abuse_no) + " Previous Reports of Abuse Yes: " + str(cl_prev_abuse_yes) + " Previous Reports of Abuse Describe: " + str(cl_prev_abuse_desc))

    ## Insert Data into clients table
    sql = """INSERT INTO clients (referral_id,cl_name_first,cl_name_last,cl_name_list,cl_age,cl_DOB,cl_language,cl_TransComm,cl_education,cl_ethnicity,
    cl_gender,cl_marital,cl_address,cl_city,cl_zip,cl_phone, cl_phys_name,cl_phys_ph,cl_insurance,cl_medications,cl_Illnesses,cl_functional_status,
    cl_cognitive_status,cl_living_setting,cl_lives_with,cl_lives_with_desc, cl_prev_abuse_no,cl_prev_abuse_yes,cl_prev_abuse_desc) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (referral_id,cl_name_first,cl_name_last,cl_name_list,cl_age,cl_DOB,cl_language,cl_TransComm,cl_education,cl_ethnicity,
    cl_gender,cl_marital,cl_address,cl_city,cl_zip,cl_phone, cl_phys_name,cl_phys_ph,cl_insurance,cl_medications,cl_Illnesses,cl_functional_status,
    cl_cognitive_status,cl_living_setting,cl_lives_with,cl_lives_with_desc, cl_prev_abuse_no,cl_prev_abuse_yes,cl_prev_abuse_desc)
    cursor.execute(sql, val)
    conn.commit()

    su_name_first = list[190].strip()
    su_name_last = list[192].strip()
    su_organization = list[194].strip()
    su_name_list = su_name_first + " " + su_name_last
    su_age = list[196].strip()
    try:
        su_DOB = datetime.strptime(list[198].strip(), '%m/%d/%Y').date()
    except:
        su_DOB = None
    su_ethnicity = list[208].strip()
    su_gender = list[210].strip()
    su_language = list[212].strip()
    su_TransComm = list[214].strip()
    su_PrimCrGvYES = list[226].find("☐ Y") == -1
    su_PrimCrGvNo = list[226].find("☐  N") == -1
    su_LivesWthYES = list[228].find("☐ Y") == -1
    su_relationship = list[224].strip()
    su_LivesWthNO = list[228].find("☐  N") == -1
    su_mental_ill = re.split('if', list[230])[0].strip()
    su_mental_ill_desc = list[230].split(':')[1].strip()
    su_AdAlchlYES = list[240].find("☐ Y") == -1
    su_AdAlchlNO = list[240].find("☐  N") == -1
    su_AdAlchlUNK = list[240].find("☐  Unknown") == -1
    su_AdDrugsYES = list[242].find("☐ Y") == -1
    su_AdDrugsNO = list[242].find("☐  N") == -1
    su_AdDrugsUNK = list[242].find("☐  Unknown") == -1
    su_AdPrepYES = list[244].find("☐ Y") == -1
    su_AdPrepNO = list[244].find("☐  N") == -1
    su_AdPrepUNK = list[244].find("☐  Unknown") == -1
    su_AdOther = list[246].strip()
    su_address = list[256].strip()
    su_city = list[258].strip()
    su_zip = list[260].strip()
    su_phone = list[262].strip()
    # print("First Name: " + str(su_name_first) + " Last Nmae: " + str(su_name_last) + " Orgnization: " + str(su_organization) + " Name List: " + str(su_name_list) +
    # " Age: " + str(su_age) + " DOB: " + str(su_DOB) + " Ethnicity: " + str(su_ethnicity) + " Gender: " + str(su_gender) + " Language: " + str(su_language) + 
    # " Translation/Communication Needs: " + str(su_TransComm) + " PrimCrGvYES: " + str(su_PrimCrGvYES) + " PrimCrGvNo: " + str(su_PrimCrGvNo) + " LivesWthYES: " + str(su_LivesWthYES) +
    # " Relationship to Client: " + str(su_relationship) + " LivesWthNO: " + str(su_LivesWthNO) + " Mental Illness: " + str(su_mental_ill) + " Mental Illness Describe: " + str(su_mental_ill_desc) +
    # " AdAlchlYES: " + str(su_AdAlchlYES) + " AdAlchlNO: " + str(su_AdAlchlNO) + " AdAlchlUNK: " + str(su_AdAlchlUNK) + " AdDrugsYES: " + str(su_AdDrugsYES) + 
    # " AdDrugsNO: " + str(su_AdDrugsNO) + " AdDrugsUNK: " + str(su_AdDrugsUNK) + " AdPrepYES: " + str(su_AdPrepYES) + 
    # " AdPrepNO: " + str(su_AdPrepNO) + " AdPrepUNK: " + str(su_AdPrepUNK) + " Addiction - Other: " + str(su_AdOther) + " Address: " + str(su_address) +
    # " City: " + str(su_city) + " Zip: " + str(su_zip) + " Telephone: " + str(su_phone)) 

    ## Insert Data into suspects table
    sql = """INSERT INTO suspects (referral_id, su_name_first, su_name_last, su_organization, su_name_list, su_age, su_DOB, 
    su_ethnicity, su_gender, su_language, su_TransComm, su_PrimCrGvYES, su_PrimCrGvNo, su_LivesWthYES, su_relationship, su_LivesWthNO, su_mental_ill, 
    su_mental_ill_desc, su_AdAlchlYES, su_AdAlchlNO, su_AdAlchlUNK, su_AdDrugsYES, su_AdDrugsNO, su_AdDrugsUNK, su_AdPrepYES, su_AdPrepNO, su_AdPrepUNK,
    su_AdOther, su_address, su_city, su_zip, su_phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (referral_id, su_name_first, su_name_last, su_organization, su_name_list, su_age, su_DOB, 
    su_ethnicity, su_gender, su_language, su_TransComm, su_PrimCrGvYES, su_PrimCrGvNo, su_LivesWthYES, su_relationship, su_LivesWthNO, su_mental_ill, 
    su_mental_ill_desc, su_AdAlchlYES, su_AdAlchlNO, su_AdAlchlUNK, su_AdDrugsYES, su_AdDrugsNO, su_AdDrugsUNK, su_AdPrepYES, su_AdPrepNO, su_AdPrepUNK,
    su_AdOther, su_address, su_city, su_zip, su_phone)
    cursor.execute(sql, val)
    conn.commit()

    ad_InvAgencies = list[272].strip()
    ad_RptingParty = list[274].strip()
    ad_Others = list[276].strip()
    ad_Abandon = list[280].find ("☐ Abandonment") == -1
    ad_Abduction = list[288].find ("☐ Abduction") == -1
    ad_Emotional = list[296].find ("☐ Emotional") == -1
    ad_FinanRlEst = list[304].find ("☐ Financial – Real Estate") == -1
    ad_FinanOth = list[282].find ("☐ Financial – Other") == -1
    ad_FinanLoss = list[290].split('$')[1].strip()
    ad_FinanLoss = ad_FinanLoss.replace(',', '')
    ad_Isolation = list[298].find ("☐ Isolation") == -1
    ad_Sexual = list[306].find ("☐ Sexual") == -1
    ad_SelfNeglec = list[284].find ("☐ Self-Neglect") == -1
    ad_NeglectOth = list[292].find ("☐ Neglect by Others") == -1
    ad_PhyAssault = list[300].find ("☐ Physical – Assault/Battery") == -1
    ad_PhyChemRst = list[308].find ("☐ Physical – Chemical Restraint") == -1
    ad_PhyCnstDpr = list[286].find ("☐ Physical – Constraint or Deprivation") == -1
    ad_PhyMedicat = list[294].find ("☐ Physical – Medication") == -1
    ad_UndueInflu = list[302].find ("☐ Undue Influence") == -1
    ad_Other = list[310].find ("☐ Other") == -1
    ad_Narrative = list[316].strip()
    # print("Other Agencies Involved: " + str(ad_InvAgencies) + " Reporting Party: " + str(ad_RptingParty) + " Others with knowledge of abuse: " + str(ad_Others) +
    # " Abandonment: " + str(ad_Abandon) + " Abduction: " + str(ad_Abduction) + " Emotional: " + str(ad_Emotional) + " Financial - Real Estate: " + str(ad_FinanRlEst) +
    # " Financial - Other: " + str(ad_FinanOth) + " Loss: " + ad_FinanLoss + " Isolation: " + str(ad_Isolation) + " Sexual: " + str(ad_Sexual) + " Self-Neglect: " + str(ad_SelfNeglec) + 
    # " Neglect by Others: " + str(ad_NeglectOth) + " Physical - Assault/Battery: " + str(ad_PhyAssault) + " Physical - Chemical Restraint: " + str(ad_PhyChemRst) +
    # " Physical - Constraint or Deprivation: " + str(ad_PhyCnstDpr) + " Physical - Medication: " + str(ad_PhyMedicat) + " Undue Influence: " + str(ad_UndueInflu) +
    # " Other: " + str(ad_Other) + " Narrative: " + str(ad_Narrative))

    ## Insert Data into suspects table
    sql = """INSERT INTO abuse_information (referral_id, ad_InvAgencies, ad_RptingParty, ad_Others, ad_Abandon, ad_Abduction, 
    ad_Emotional, ad_FinanRlEst, ad_FinanOth, ad_FinanLoss,ad_Isolation, ad_Sexual, ad_SelfNeglec, ad_NeglectOth, ad_PhyAssault, 
    ad_PhyChemRst, ad_PhyCnstDpr, ad_PhyMedicat, ad_UndueInflu, ad_Other, ad_Narrative) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s)"""
    val = (referral_id, ad_InvAgencies, ad_RptingParty, ad_Others, ad_Abandon, ad_Abduction, 
    ad_Emotional, ad_FinanRlEst, ad_FinanOth, ad_FinanLoss,ad_Isolation, ad_Sexual, ad_SelfNeglec, ad_NeglectOth, ad_PhyAssault, 
    ad_PhyChemRst, ad_PhyCnstDpr, ad_PhyMedicat, ad_UndueInflu, ad_Other, ad_Narrative)
    cursor.execute(sql, val)
    conn.commit()

    ## Add referral ID for attachments, goals, meeting_notes, outcome and recommendations tables
    # sql = """INSERT INTO attachments(referral_id) VALUES (%s)"""
    # val = (referral_id)
    # cursor.execute(sql, val)
    # conn.commit()
    sql = """INSERT INTO goals(referral_id) VALUES (%s)"""
    val = (referral_id)
    cursor.execute(sql, val)
    conn.commit()
    sql = """INSERT INTO meeting_notes(referral_id) VALUES (%s)"""
    val = (referral_id)
    cursor.execute(sql, val)
    conn.commit()
    sql = """INSERT INTO outcome(referral_id) VALUES (%s)"""
    val = (referral_id)
    cursor.execute(sql, val)
    conn.commit()
    sql = """INSERT INTO recommendations(referral_id) VALUES (%s)"""
    val = (referral_id)
    cursor.execute(sql, val)
    conn.commit()



    # for i in range(0, 3):
    #     print(list[i])
