import sys
from docx2python import docx2python #the main library that parse the word_doc (it is grabbing a library that I modified to display the right checkboxes)
import datetime
# pip install docx2python to install docx2python
# use command line type in "python3 worddocparser.py [path to docx]" (python3 worddocparser.py 1.docx)

def parse_file(file_path): #main function to open the file and return all the data
    doc = docx2python(file_path) #get the file
    dictc = {}
    everything_else, suspect_dict = parse_this(grabdata(doc)) #call funciton to parse it and reutrns 2 dictionary
    dictc["everything_else"] = everything_else #combining the 2 dictionary into one
    dictc["suspect"] = suspect_dict
    return dictc #return the whole thing

def grabdata(doc): #first get all the data from the document and return it into a list
    lista = []
    for section in doc.body: #this is goes through all tables, getting all the information. (If the document changes, this will break)
        for table in section:
            for data in table:
                lista.append(data)
    return lista

def clean(line): #this function is a just a help to clean up some of the weird formatting this old .docx has
    line = line.replace("\n","")
    line = line.replace("\t","")
    line = line.replace("\u2002","")
    return line

def remove_blanks(listb): #this function removes blanks from a list, which allows for me to figure out the exact index in the list
    listb = list(filter(lambda word: word != "", listb))
    return listb

def dropdown(dictc, words, key): #this function handles dropdown menus, mostly just defaulting the Select... to None
    if (words == "Select..."):
        dictc[key] = None
    else:
        dictc[key] = words.strip()

def one_checkbox(dictc, words, key): #this function figures out if the checkboxes are checked or not
    if (words == "☐"):
        dictc[key] = False
    else:
        dictc[key] = True

def two_checkboxes(dictc, split, key): #this function return a single boolean from 2 checkboxes
    if split[0] == "☐" and split[2] != "☐":
        dictc[key] = True
    elif split[0] != "☐" and split[2] == "☐":
        dictc[key] = False
    elif split[0] == "☐" and split[2] == "☐":
        dictc[key] = False
    else:
        dictc[key] = True

def three_checkboxes(dictc, split, key): #YES", "su_AdPrepNO", "su_AdPrepUNK, this function return a single boolean from 3 checkboxes
    if split[0] == "☐" and split[2] == "☐" and split[4] == "☐":
        dictc[key] = False
    elif split[0] != "☐" and split[2] == "☐" and split[4] == "☐":
        dictc[key] = True
    elif split[0] != "☐" and split[2] != "☐" and split[4] == "☐":
        dictc[key] = True
    elif split[0] != "☐" and split[2] != "☐" and split[4] != "☐":
        dictc[key] = True
    elif split[0] == "☐" and split[2] != "☐" and split[4] == "☐":
        dictc[key] = False
    elif split[0] == "☐" and split[2] != "☐" and split[4] != "☐":
        dictc[key] = False
    elif split[0] == "☐" and split[2] == "☐" and split[4] != "☐":
        dictc[key] = ""

def delete_empty(check_this): #this handy function remove all keys that are blank, reducing the size of the dictionary
    delete_list = []
    for key, value in check_this.items():
        if (type(value) is str):
            if (value.isspace()) or (not value):
                delete_list.append(key)
    for key in delete_list:
        check_this.pop(key)

def change_to_int(dictc, key): #this function just changes all numbers from string to ints
    if key in dictc:
        if dictc[key].isnumeric():
            value = dictc[key].strip()
            dictc[key] = int(value)

def get_date(date): #this function converst a number of formats for dates into the format the database wants
    date_patterns = ["%Y-%m-%d", "%m-%d-%Y", "%Y-%m-%d",
                     "%Y/%m/%d", "%m/%d/%Y", "%Y/%m/%d"]
    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(date, pattern).strftime("%Y/%m/%d")
        except:
            pass
    return ""

def change_to_date(dictc, key): #mostly for DOB and seeing if it is Unknown or an actual date format
    if key in dictc:
        value = dictc[key].strip()
        if "UNK" in value or "Unknown" in value or "unknown" in value:
            dictc[key] = ""
        else:
            try:
                dictc[key] = datetime.datetime.strptime(get_date(dictc[key]),"%Y/%m/%d")
            except:
                dictc[key] = ""

def parse_this(list):
    dicta = {}
    dictb = {}
    count = 0
    for item in list:
        #print(item)
        for words in item: #Go through the list and grab column values and map them. This is hardcoded, if the form changes this will break.
            words = clean(words)
            if (count == 0): #This is for urgent and routine
                split = remove_blanks(words.split(" "))
                one_checkbox(dicta, split[3], "status_urgent")
                one_checkbox(dicta, split[5], "status_routine")
            elif (count == 1): #This is for case date
                split = remove_blanks(words.split(":"))
                dicta["case_date"] = str(split[1].replace(" ",""))
            elif (count == 2): #This is for case number
                split = remove_blanks(words.split(":"))
                dicta["case_number"] = str(split[1].strip()).replace(" ","")
            elif (count == 5):
                one_checkbox(dicta, words[0], "consult_aps")
            elif (count == 6):
                one_checkbox(dicta, words[0], "consult_mental_health")
            elif (count == 7):
                one_checkbox(dicta, words[0], "consult_district_att")
            elif (count == 8):
                one_checkbox(dicta, words[0], "consult_regional")
            elif (count == 9):
                one_checkbox(dicta, words[0], "consult_coroner")
            elif (count == 10):
                one_checkbox(dicta, words[0], "consult_law_enf")
            elif (count == 11):
                one_checkbox(dicta, words[0], "consult_att_oth")
            elif (count == 12):
                one_checkbox(dicta, words[0], "consult_psychologist")
            elif (count == 13):
                one_checkbox(dicta, words[0], "consult_physician")
            elif (count == 14):
                one_checkbox(dicta, words[0], "consult_ombudsman")
            elif (count == 15):
                one_checkbox(dicta, words[0], "consult_pub_guard")
            elif (count == 16):
                one_checkbox(dicta, words[0], "consult_other")
                if dicta["consult_other"] == False:
                    dicta["consult_other_desc"] = ""
                else:
                    dicta["consult_other_desc"] = words.split(":")[1]
            elif (count == 17):
                split = remove_blanks(words.split(" "))
                dicta["ra_case_no"] = split[-1]
            elif (count == 22):
                dicta["ra_fname"] = words.strip()
            elif (count == 23):
                dicta["ra_lname"] = words.strip()
            elif (count == 24):
                split = words.split("other:")
                dropdown(dicta, split[0], "ra_fc_team")
                dicta["ra_fc_other"] = split[1]
            elif (count == 25):
                dicta["ra_email"] = words.strip()
            elif (count == 30):
                dicta["ra_ph_office"] = words.strip()
            elif (count == 31):
                dicta["ra_fx_office"] = words.strip()
            elif (count == 32):
                dicta["ra_ph_mobile"] = words.strip()
            elif (count == 33):
                dicta["ra_supervisor_name"] = words.strip()
            elif (count == 41):
                dicta["cl_name_first"] = words.strip()
            elif (count == 42):
                dicta["cl_name_last"] = words.strip()
            elif (count == 43):
                dicta["cl_age"] = words.strip()
            elif (count == 44):
                dicta["cl_DOB"] = words.strip()
            elif (count == 45):
                dicta["cl_language"] = words.strip()
            elif (count == 46):
                dicta["cl_TransComm"] = words.strip()
            elif (count == 51):
                dropdown(dicta, words, "cl_education")
            elif (count == 52):
                dropdown(dicta, words, "cl_ethnicity")
            elif (count == 53):
                dropdown(dicta, words, "cl_gender")
            elif (count == 54):
                dropdown(dicta, words, "cl_marital")
            elif (count == 59):
                dicta["cl_address"] = words.strip()
            elif (count == 60):
                dicta["cl_city"] = words.strip()
            elif (count == 61):
                dicta["cl_zip"] = words.strip()
            elif (count == 62):
                dicta["cl_phone"] = words.strip()
            elif (count == 67):
                dicta["cl_phys_name"] = words.strip()
            elif (count == 68):
                dicta["cl_phys_ph"] = words.strip()
            elif (count == 69):
                dicta["cl_insurance"] = words.strip()
            elif (count == 71):
                dicta["cl_medications"] = words.strip()
            elif (count == 74):
                dicta["cl_Illnesses"] = words.strip()
            elif (count == 79):
                dropdown(dicta, words, "cl_functional_status")
            elif (count == 80):
                dropdown(dicta, words, "cl_cognitive_status")
            elif (count == 85):
                dropdown(dicta, words, "cl_living_setting")
            elif (count == 86):
                if ("(describe)" in words): #descriptions requires a split to grab describe data
                    split = words.split("(describe)")
                    dicta["cl_lives_with"] = split[0]+"(describe)"
                    dicta["cl_lives_with_desc"] = split[1].strip()
                else:
                    dropdown(dicta, words, "cl_lives_with")
                    dicta["cl_lives_with_desc"] = ""
            elif (count == 88):
                split = remove_blanks(words.split("explain"))
                if words[0] == "☐" and words[10] != "☐": #this is a special checkbox with desc
                    dicta["cl_prev_abuse"] = True
                    dicta["cl_prev_abuse_desc"] = split[1].strip()
                elif words[0] != "☐" and words[10] == "☐":
                    dicta["cl_prev_abuse"] = False
                    dicta["cl_prev_abuse_desc"] = ""
                elif words[0] == "☐" and words[10] == "☐":
                    dicta["cl_prev_abuse"] = False
                    dicta["cl_prev_abuse_desc"] = ""
                else:
                    dicta["cl_prev_abuse"] = True
                    dicta["cl_prev_abuse_desc"] = split[1].strip()
            elif (count == 95): #suspects data is gathered into another dict
                dictb["su_name_first"] = words.strip() 
            elif (count == 96):
                dictb["su_name_last"] = words.strip()
            elif (count == 97):
                dictb["su_organization"] = words.strip()
            elif (count == 98):
                dictb["su_age"] = words.strip()
            elif (count == 99):
                dictb["su_DOB"] = words.strip()
            elif (count == 104):
                dropdown(dictb, words, "su_ethnicity")
            elif (count == 105):
                dropdown(dictb, words, "su_gender")
            elif (count == 106):
                dictb["su_language"] = words.strip()
            elif (count == 107):
                dictb["su_TransComm"] = words.strip()
            elif (count == 112):
                dropdown(dictb, words, "su_relationship")
            elif (count == 113):
                split = remove_blanks(words.split(" "))
                two_checkboxes(dictb, split, "su_PrimCrGv")
            elif (count == 114):
                split = remove_blanks(words.split(" "))
                two_checkboxes(dictb, split, "su_LivesWth")
            elif (count == 115):
                split = words.split("if yes:")
                dropdown(dictb, split[0], "su_mental_ill")
                dictb["su_mental_ill_desc"] = split[1]
            elif (count == 120):
                split = remove_blanks(words.split(" "))
                three_checkboxes(dictb, split, "su_AdAlchl")
            elif (count == 121):
                split = remove_blanks(words.split(" "))
                three_checkboxes(dictb, split, "su_AdDrugs")
            elif (count == 122):
                split = remove_blanks(words.split(" "))
                three_checkboxes(dictb, split, "su_AdPrep")
            elif (count == 123):
                dictb["su_AdOther"] = words.strip()
            elif (count == 128):
                dictb["su_address"] = words.strip()
            elif (count == 129):
                dictb["su_city"] = words.strip()
            elif (count == 130):
                dictb["su_zip"] = words.strip()
            elif (count == 131):
                dictb["su_phone"] = words.strip()
            elif (count == 136):
                dicta["ad_InvAgencies"] = words.strip()
            elif (count == 137):
                dropdown(dicta,words,"ad_RptingParty")
            elif (count == 138):
                dicta["ad_Others"] = words.strip()
            elif (count == 140):
                one_checkbox(dicta, words[0], "ad_Abandon")
            elif (count == 141):
                one_checkbox(dicta, words[0], "ad_FinanOth")
            elif (count == 142):
                one_checkbox(dicta, words[0], "ad_SelfNeglec")
            elif (count == 143):
                one_checkbox(dicta, words[0], "ad_PhyCnstDpr")
            elif (count == 144):
                one_checkbox(dicta, words[0], "ad_Abduction")
            elif (count == 145):
                split = remove_blanks(words.split("Est. loss $ "))
                dicta["ad_FinanLoss"] = split[0].strip()
            elif (count == 146):
                one_checkbox(dicta, words[0], "ad_NeglectOth")
            elif (count == 147):
                one_checkbox(dicta, words[0], "ad_PhyMedicat")
            elif (count == 148):
                one_checkbox(dicta, words[0], "ad_Emotional")
            elif (count == 149):
                one_checkbox(dicta, words[0], "ad_Isolation")
            elif (count == 150):
                one_checkbox(dicta, words[0], "ad_PhyAssault")
            elif (count == 151):
                one_checkbox(dicta, words[0], "ad_UndueInflu")
            elif (count == 152):
                one_checkbox(dicta, words[0], "ad_FinanRlEst")
            elif (count == 153):
                one_checkbox(dicta, words[0], "ad_Sexual")
            elif (count == 154):
                one_checkbox(dicta, words[0], "ad_PhyChemRst")
            elif (count == 155):
                one_checkbox(dicta, words[0], "ad_Other")
            elif (count == 158):
                dicta["ad_Narrative"] = words.strip()
            count += 1
    change_to_int(dicta, "cl_age") #converting age to ints
    #change_to_int(dicta, "cl_zip")
    change_to_int(dictb, "su_age")
    #change_to_int(dictb, "su_zip")
    change_to_date(dicta, "case_date") #converting str to dates
    change_to_date(dicta, "cl_DOB")
    change_to_date(dictb, "su_DOB")
    delete_empty(dicta) #removing empty values in both dicts
    delete_empty(dictb)
    if ("ad_RptingParty" in dicta): #change the dropdown menu weird first letter to U
        if dicta["ad_RptingParty"] == "unknown":
            dicta["ad_RptingParty"] = "Unknown"
    return dicta, dictb #return both

if __name__ == '__main__':
    doc = docx2python(sys.argv[1])
    print(doc.text)