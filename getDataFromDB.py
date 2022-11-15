from flask import Flask
app = Flask(__name__)
import os #provides ways to access the Operating System and allows us to read the environment variables
from flaskext.mysql import MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("DatabaseUser")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DatabasePassword")
app.config['MYSQL_DATABASE_DB'] = os.getenv("DatabaseDB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("DatabaseHost")
# app.secret_key = 'super secret key'
# app.config['SESSION_TYPE'] = 'filesystem'
mysql.init_app(app)
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

def get_case_summary_from_db(id):
    #  search to get
    dic = dict()
    dic["name"] = "Mr Darcy"
    dic["presenter"] = "John Doe"
    dic["date"] = "2022-04-01"
    notesarr = []
    notesarr.append ("notes000")
    notesarr.append ("notes111")
    dic["notes"] = notesarr
    goalarr = []
    goalarr.append("Goal 1: goal1111")
    goalarr.append("Goal 2: goal2222")
    dic["goal"] = goalarr
    rcmdlist = []
    dicrcmd = dict()
    dicrcmd['ActionStep'] = 'work on goal 1'
    dicrcmd['PersonResponsilbe'] = 'Jorge L sole'
    dicrcmd['followupDate'] = '2022-01-01'
    dicrcmd['status'] = 'ukm'
    rcmdlist.append(dicrcmd)
    dicrcmd = dict()
    dicrcmd['ActionStep'] = 'work on goal 1'
    dicrcmd['PersonResponsilbe'] = 'Jorge L sole'
    dicrcmd['followupDate'] = '2022-01-01'
    dicrcmd['status'] = 'ukm'
    rcmdlist.append(dicrcmd)
    dic["rcmd"] = rcmdlist
    return dic

def delete_case(referral_id):
    delete_sql = "DELETE FROM clients WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM abuse_information WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM attachments WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM consultation_information WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM goals WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM meeting_notes WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM outcome WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM recommendations WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM referring_agency WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM suspects WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM case_number WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
    delete_sql = "DELETE FROM cases WHERE referral_id = " + str(referral_id)
    cursor.execute(delete_sql)
    conn.commit()
 
    
    return None

def search_cases_from_database(type, first_name,last_name, closedCase):
    # result =  [dict(link="https://www.google.com/",id="1234", name="John Doe4"),
    #             dict(link="https://www.google.com/",id="1235", name="John Doe5"),
    #             dict(link="https://www.google.com/",id="1236", name="John Doe6"),
    #             dict(link="https://www.google.com/",id="1237", name="John Doe7"),
    #             ]
    result = []
    # if (type == ''):
        # flash(u'Please Select a type', 'error')
    if (type == "client"):
        
        basic_sql = """
        WITH
        case_number_clients	AS (
            SELECT 
		        clients.referral_id,
		        clients.cl_name_first,
                clients.cl_name_last ,
                case_number.case_number
	    FROM 
		    clients 
	    INNER JOIN case_number 
        ON
		    case_number.referral_id = clients.referral_id
        ),
        all_cases AS (
            SELECT
	        cases.case_date,
            cases.case_closed,
            cases.referral_id,
            case_number_clients.cl_name_first,
            case_number_clients.cl_name_last,
            case_number_clients.case_number
        FROM cases
        INNER JOIN case_number_clients 
        ON
	        case_number_clients.referral_id = cases.referral_id
        )
        SELECT
	        all_cases.referral_id ,
	        all_cases.case_number,
            all_cases.cl_name_first,
            all_cases.cl_name_last,
            all_cases.case_date,
            all_cases.case_closed
        FROM all_cases
        WHERE
	    all_cases.case_closed = 
        """   + str(closedCase) + " ORDER BY all_cases.case_date DESC"

        if (first_name):
            basic_sql += " AND all_cases.cl_name_first = " + "\"" + first_name + "\" "
        if (last_name):
            basic_sql += " AND all_cases.cl_name_last = " + "\"" + last_name + "\" "
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for item in data:
            dic = dict()
            dic["link"] = "client_information/"+str(item[0])
            dic["referral_id"] = item[0]
            dic["case_number"] = item[1]
            dic["cl_name_first"] = item[2]
            dic["cl_name_last"] = item[3]
            dic["case_date"] = item[4]
            result.append(dic)
        # print (result)
    elif (type == "presenter"):
        basic_sql = """
WITH
case_number_clients	AS (
SELECT 
		clients.referral_id,
		clients.cl_name_first,
        clients.cl_name_last ,
        case_number.case_number
	FROM 
		clients 
	INNER JOIN case_number 
    ON
		case_number.referral_id = clients.referral_id
),
cte_cases AS (
SELECT
	cases.case_date,
    cases.case_closed,
    cases.referral_id,
    case_number_clients.cl_name_first,
    case_number_clients.cl_name_last,
    case_number_clients.case_number
FROM cases
INNER JOIN case_number_clients 
ON
	case_number_clients.referral_id = cases.referral_id
),
cte_all_cases AS (
SELECT
	cte_cases.referral_id ,
	cte_cases.case_number,
    cte_cases.cl_name_first,
    cte_cases.cl_name_last,
    cte_cases.case_date,
    cte_cases.case_closed,
    meeting_notes.meeting_presenters
FROM cte_cases
INNER JOIN meeting_notes
ON cte_cases.referral_id = meeting_notes.referral_id
)
SELECT
	cte_all_cases.referral_id ,
	cte_all_cases.case_number,
    cte_all_cases.cl_name_first,
    cte_all_cases.cl_name_last,
    cte_all_cases.case_date,
    cte_all_cases.case_closed,
    cte_all_cases.meeting_presenters

FROM cte_all_cases
WHERE
cte_all_cases.case_closed =
        """  + str(closedCase) + " ORDER BY cte_all_cases.case_date DESC"
        full_name = ""
        if (first_name):
            full_name += first_name.strip()
        if (last_name):
            full_name += " "
            full_name += last_name.strip()
        if (full_name):
            basic_sql += " AND cte_all_cases.meeting_presenters = " + "\"" + full_name + "\" "
        
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for item in data:
            dic = dict()
            dic["link"] = "client_information/"+str(item[0])
            dic["referral_id"] = item[0]
            dic["case_number"] = item[1]
            dic["cl_name_first"] = item[2]
            dic["cl_name_last"] = item[3]
            dic["case_date"] = item[4]
            arr = item[6].split(' ')
            arrln = arr[1:]
            dic["presenter_name_first"] = arr[0]
            dic["presenter_name_last"] = ' '.join(arrln)
            result.append(dic)
    else : # suspect
        basic_sql = """
WITH
case_number_clients	AS (
SELECT 
		clients.referral_id,
		clients.cl_name_first,
        clients.cl_name_last ,
        case_number.case_number
	FROM 
		clients 
	INNER JOIN case_number 
    ON
		case_number.referral_id = clients.referral_id
),
cte_cases AS (
SELECT
	cases.case_date,
    cases.case_closed,
    cases.referral_id,
    case_number_clients.cl_name_first,
    case_number_clients.cl_name_last,
    case_number_clients.case_number
FROM cases
INNER JOIN case_number_clients 
ON
	case_number_clients.referral_id = cases.referral_id
),
cte_all_cases AS (
SELECT
	cte_cases.referral_id ,
	cte_cases.case_number,
    cte_cases.cl_name_first,
    cte_cases.cl_name_last,
    cte_cases.case_date,
    cte_cases.case_closed,
    suspects.su_name_first,
    suspects.su_name_last
FROM cte_cases
INNER JOIN suspects
ON cte_cases.referral_id = suspects.referral_id
)
SELECT
	cte_all_cases.referral_id ,
	cte_all_cases.case_number,
    cte_all_cases.cl_name_first,
    cte_all_cases.cl_name_last,
    cte_all_cases.case_date,
    cte_all_cases.case_closed,
    cte_all_cases.su_name_first,
    cte_all_cases.su_name_last
FROM cte_all_cases
WHERE
cte_all_cases.case_closed = 
        """   + str(closedCase) + " ORDER BY cte_all_cases.case_date DESC"

        if (first_name):
            basic_sql += " AND cte_all_cases.su_name_first = " + "\"" + first_name + "\" "
        if (last_name):
            basic_sql += " AND cte_all_cases.su_name_last = " + "\"" + last_name + "\" "
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for item in data:
            dic = dict()
            dic["link"] = "client_information/"+str(item[0])
            dic["referral_id"] = item[0]
            dic["case_number"] = item[1]
            dic["cl_name_first"] = item[2]
            dic["cl_name_last"] = item[3]
            dic["case_date"] = item[4]
            dic["suspect_name_first"] = item[6]
            dic["suspect_name_last"] = item[7]
            result.append(dic)
        
    return result

def get_referral_info_from_db(referral_id):
    # size 10
    Dic = dict()
    cursor.execute(" SELECT * FROM referring_agency WHERE referral_id =  " + str(referral_id) + ";")
    data = cursor.fetchone()
    if data != None :
        Dic["referCaseNum"] = data[1]
        Dic["firstName"] = data[2]
        Dic["lastName"] = data[3]
        Dic["FCTeamMember"] = data[5]
        Dic["fcTeamOther"] = data[6]
        Dic["email"] = data[7]
        Dic["officePhone"] = data[8]
        Dic["officeTax"] = data[9]
        Dic["mobilePhone"] = data[10]
        Dic["supervisorName"] = data[11]
 
    return Dic