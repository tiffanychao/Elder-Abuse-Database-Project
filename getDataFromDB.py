
def get_case_summary_from_db(id, cursor, conn):
    #  search to get
    dict_all_info = dict()
    sql_name = """
SELECT
	cl_name_first,
    cl_name_last
FROM
	clients
WHERE
	referral_id = 
    """ + str(id)
    cursor.execute(sql_name)
    data = cursor.fetchone()
    
    if data == None :
        return dict_all_info
    dict_all_info['name'] = data[0] +" "+ data[1]

    arr_notes = []
    sql_notes = """
    SELECT 
        meeting_id,
	    meeting_date,
        Meeting_presenters,
        meeting_narrative
    FROM meeting_notes
    WHERE
	    referral_id = 
    """ + str(id) + " ORDER BY meeting_date DESC"

    cursor.execute(sql_notes)
    data = cursor.fetchall()
        
    for itemori in data:
        item = convertNonetoNull(itemori)
        dic = dict()
        dic['meeting_id'] = item[0]
        dic['date'] = item[1]
        dic['presenter'] = item[2]
        dic['meeting_note'] = item[3]
        arr_notes.append(dic)

    dict_all_info['notes'] = arr_notes
  
    
    sql_goal = """
SELECT 
	goal
FROM goals
WHERE
	referral_id = 
    """ + str(id)
    goalarr = []
    cursor.execute(sql_goal)
    data = cursor.fetchall()
    for item in data:
        goalarr.append(item)

    dict_all_info["goal"] = goalarr

    sql_remd = """
SELECT 
	action_step,
    person_responsible,
    followup_date,
    action_status
FROM
	recommendations
WHERE
	referral_id = 
    """ + str(id) + " ORDER BY followup_date DESC"

    rcmdlist = []

    cursor.execute(sql_remd)
    data = cursor.fetchall()
    for itemori in data:
        item = convertNonetoNull(itemori)
        dicrcmd = dict()
        dicrcmd['ActionStep'] = item[0]
        dicrcmd['PersonResponsilbe'] = item[1]
        dicrcmd['followupDate'] = item[2]
        dicrcmd['status'] = item[3]
        rcmdlist.append(dicrcmd)    

    dict_all_info["rcmd"] = rcmdlist
    return dict_all_info

def delete_case(referral_id, cursor, conn):
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

def search_cases_from_database(type, first_name,last_name,full_name, closedCase, cursor, conn):
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
	    LEFT JOIN case_number 
        ON
		    case_number.referral_id = clients.referral_id
UNION

            SELECT 
		        clients.referral_id,
		        clients.cl_name_first,
                clients.cl_name_last ,
                case_number.case_number
	    FROM 
		    clients 
	    RIGHT JOIN case_number 
        ON
		    case_number.referral_id = clients.referral_id
        ),
        cte_all_cases AS (
            SELECT
	        cases.case_date,
            cases.case_closed,
            cases.referral_id,
            case_number_clients.cl_name_first,
            case_number_clients.cl_name_last,
            case_number_clients.case_number
        FROM cases
        LEFT JOIN case_number_clients 
        ON
	        case_number_clients.referral_id = cases.referral_id
UNION

            SELECT
	        cases.case_date,
            cases.case_closed,
            cases.referral_id,
            case_number_clients.cl_name_first,
            case_number_clients.cl_name_last,
            case_number_clients.case_number
        FROM cases
        RIGHT JOIN case_number_clients 
        ON
	        case_number_clients.referral_id = cases.referral_id
        )
        SELECT
	        cte_all_cases.referral_id ,
	        cte_all_cases.case_number,
            cte_all_cases.cl_name_first,
            cte_all_cases.cl_name_last,
            cte_all_cases.case_date,
            cte_all_cases.case_closed
        FROM cte_all_cases
        WHERE
	    cte_all_cases.case_closed = 
        """   + str(closedCase) 

        if (first_name):
            basic_sql += " AND cte_all_cases.cl_name_first LIKE " + "\"%" + first_name.strip() + "%\" "
        if (last_name):
            basic_sql += " AND cte_all_cases.cl_name_last LIKE " + "\"%" + last_name.strip() + "%\" "
        
        basic_sql += " ORDER BY cte_all_cases.case_date DESC"
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for itemori in data:
            item = convertNonetoNull(itemori)
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
	LEFT JOIN case_number 
    ON
		case_number.referral_id = clients.referral_id
    UNION
SELECT 
		clients.referral_id,
		clients.cl_name_first,
        clients.cl_name_last ,
        case_number.case_number
	FROM 
		clients 
	RIGHT JOIN case_number 
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
LEFT JOIN case_number_clients 
ON
	case_number_clients.referral_id = cases.referral_id

UNION

SELECT
	cases.case_date,
    cases.case_closed,
    cases.referral_id,
    case_number_clients.cl_name_first,
    case_number_clients.cl_name_last,
    case_number_clients.case_number
FROM cases
RIGHT JOIN case_number_clients 
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
LEFT JOIN meeting_notes
ON cte_cases.referral_id = meeting_notes.referral_id

UNION
SELECT
	cte_cases.referral_id ,
	cte_cases.case_number,
    cte_cases.cl_name_first,
    cte_cases.cl_name_last,
    cte_cases.case_date,
    cte_cases.case_closed,
    meeting_notes.meeting_presenters
FROM cte_cases
RIGHT JOIN meeting_notes
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
        """  + str(closedCase) 
        # print(full_name)
        basic_sql += " AND cte_all_cases.meeting_presenters LIKE " + "\"%" + full_name.strip() + "%\" "
        basic_sql += " ORDER BY cte_all_cases.case_date DESC"
        # print(basic_sql)
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for itemori in data:
            item = convertNonetoNull(itemori)
            dic = dict()
            dic["link"] = "client_information/"+str(item[0])
            dic["referral_id"] = item[0]
            dic["case_number"] = item[1]
            dic["cl_name_first"] = item[2]
            dic["cl_name_last"] = item[3]
            dic["case_date"] = item[4]
            dic["presenter_name_full"] = item[6]
        
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
	LEFT JOIN case_number 
    ON
		case_number.referral_id = clients.referral_id

UNION

SELECT 
		clients.referral_id,
		clients.cl_name_first,
        clients.cl_name_last ,
        case_number.case_number
	FROM 
		clients 
	RIGHT JOIN case_number 
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
LEFT JOIN case_number_clients 
ON
	case_number_clients.referral_id = cases.referral_id

UNION

SELECT
	cases.case_date,
    cases.case_closed,
    cases.referral_id,
    case_number_clients.cl_name_first,
    case_number_clients.cl_name_last,
    case_number_clients.case_number
FROM cases
RIGHT JOIN case_number_clients 
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
LEFT JOIN suspects
ON cte_cases.referral_id = suspects.referral_id

UNION

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
RIGHT JOIN suspects
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
        """   + str(closedCase) 

        if (first_name):
            basic_sql += " AND cte_all_cases.su_name_first LIKE " + "\"%" + first_name.strip() + "%\" "
        if (last_name):
            basic_sql += " AND cte_all_cases.su_name_last LIKE " + "\"%" + last_name.strip() + "%\" "
        
        basic_sql += " ORDER BY cte_all_cases.case_date DESC"
        cursor.execute(basic_sql)
        data = cursor.fetchall()
        
        for itemori in data:
            item = convertNonetoNull(itemori)
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

def get_referral_info_from_db(referral_id, cursor, conn):
    # size 10
    Dic = dict()
    cursor.execute(" SELECT * FROM referring_agency WHERE referral_id =  " + str(referral_id) + ";")
    dataori = cursor.fetchone()
    if dataori != None :
        data = convertNonetoNull(dataori)
       
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
def convertNonetoNull(dataori):
    data = []
    for x in dataori :
        if(x == None):
            data.append('')
        else :
            data.append(x)
    return data

def getBarInfo(referral_id, cursor, conn):
    str_sql = """
SELECT
	status_urgent,
    status_routine,
    case_date,
    case_closed
FROM cases
WHERE
	referral_id = 
    """ + str(referral_id)

    dic = dict()
    dic['status_urgent'] = ''
    dic['status_routine'] = ''
    dic['case_date'] = ''
    dic['case_closed'] = ''
    dic['case_number'] = ''
    
    cursor.execute(str_sql)
    dataori = cursor.fetchone()
    # print(dataori)
    if dataori != None :
        data = convertNonetoNull(dataori)
        dic['status_urgent'] = data[0]
        dic['status_routine'] = data[1]
        dic['case_date'] = data[2]
        dic['case_closed'] = data[3]
    

    str_sql = """
SELECT
	case_number
FROM case_number
WHERE
	referral_id =
    """ + str(referral_id)
    cursor.execute(str_sql)
    dataori = cursor.fetchone()
    if dataori != None :
        data = convertNonetoNull(dataori)
        dic['case_number'] = data[0]

    # print(dic)
    return dic