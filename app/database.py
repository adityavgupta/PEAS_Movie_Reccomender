"""Defines all the functions related to the database"""
from app import db
import sys

# def fetch_todo() -> dict:
#     """Reads all tasks listed in the todo table

#     Returns:
#         A list of dictionaries
#     """

#     conn = db.connect()
#     query_results = conn.execute("Select * from tasks;").fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "id": result[0],
#             "task": result[1],
#             "status": result[2]
#         }
#         todo_list.append(item)

#     return todo_list


# def update_task_entry(task_id: int, text: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def insert_new_task(text: str) ->  int:
#     """Insert new task to todo table.

#     Args:
#         text (str): Task description

#     Returns: The task ID for the inserted entry
#     """

#     conn = db.connect()
#     query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
#         text, "Todo")
#     conn.execute(query)
#     query_results = conn.execute("Select LAST_INSERT_ID();")
#     query_results = [x for x in query_results]
#     task_id = query_results[0][0]
#     conn.close()

#     return task_id


# def remove_task_by_id(task_id: int) -> None:
#     """ remove entries based on task ID """
#     conn = db.connect()
#     query = 'Delete From tasks where id={};'.format(task_id)
#     conn.execute(query)
#     conn.close()

def insert_new_user(_name:str,_dob:str,_password:str)->int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    streaming_platforms='default'
    conn = db.connect()
    
    try:
        user_id=conn.execute("SELECT MAX(Users.user_id) FROM Users;").fetchall()[0][0]+1
        print(user_id)
        
    except:
        print("in except")
        user_id=1
    # query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
    #     text, "Todo")
    try:
        insertion = 'INSERT INTO Users VALUES({},"{}",CAST("{}" as DATE),"{}","{}");'.format(user_id,_name,_dob,streaming_platforms,_password)
        conn.execute(insertion)
        print(insertion, file=sys.stderr)
    except Exception as e:
        print(e)
    conn.close()
    return 0

def verify_user_info(_name:str,_password:str)->int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """
    conn = db.connect()
    
    ##change:verify user info
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(_name)
        user_id=conn.execute(query_uid).fetchall()[0][0]
        #verify password
        query_pwd = 'SELECT Users.passwd FROM Users WHERE Users.name="{}";'.format(_name)
        pswd = conn.execute(query_pwd).fetchall()[0][0]
        
        if pswd == _password:
            return 0
        else:
            print('Wrong pswd')
            return 1
    except:
        #user doesn't exist
        print("No such user")
        return 1
    # query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
    #     text, "Todo")
    conn.close()
    return 1

def lookup(name:str, platform:str, date:str):
    result = None
    conn = db.connect()
    platforms = platform.split(',') # ['Netflix', 'Hulu', 'Prime', 'Disney']
    year = date.split('-')[0]
    movie_where = 'WHERE release_year > "{}"'.format(year)
    tv_where = 'WHERE CAST(start_year as unsigned) > "{}"'.format(year)
    if name:
        movie_where += ' AND (m.name LIKE "%%{}%%")'.format(name)
        tv_where += ' AND (t.name LIKE "%%{}%%")'.format(name)

    platform_where = 'WHERE (platform LIKE'
    for i in range(len(platforms)):
        strn = platforms[i]
        if i == 0:
            platform_where += ' "%%'+strn+'%%" '
        else:
            platform_where += 'or platform LIKE "%%'+strn+'%%" '
    platform_where += ') '

    
    #print(platform_where)
    try:
        # query = '(SELECT m.name, "Movie" as type from movie m where m.name LIKE "%%{}%%" ORDER BY m.popularity LIMIT 10)\
        #          UNION \
        #         (SELECT t.name, "TV Show" as type from tv_show t where t.name LIKE "%%{}%%" ORDER BY t.popularity LIMIT 10)'.format(name, name)
        # print(query)
        # query = 'SELECT title_name, type_mt, pop, ar, platform\
        #     FROM ((SELECT m.name as title_name, m.type_id as type_mt, m.popularity as pop, avg_rating as ar, available_on as platform\
        #          FROM movie m '+movie_where+' ORDER BY m.popularity DESC LIMIT 500) UNION\
        #             (SELECT t.name, t.type_id, t.popularity, avg_rating, available_on FROM tv_show t'+tv_where+' ORDER BY t.popularity DESC LIMIT 500)) AS topmt\
        #             '+platform_where+' ORDER BY ar DESC;'.format(date,name,date,name)
        query = 'SELECT title_name, type_mt, mtitle_id, pop, ar, platform\
            FROM(\
            (SELECT m.name as title_name, m.type_id as type_mt, m.title_id as mtitle_id, m.popularity as pop, avg_rating as ar, available_on as platform FROM movie m '+movie_where+' ORDER BY m.popularity DESC LIMIT 20)\
                UNION\
                (SELECT t.name, t.type_id, t.title_id, t.popularity, avg_rating, available_on FROM tv_show t '+tv_where+' ORDER by popularity DESC LIMIT 20)) AS topmt\
                '+platform_where+'ORDER BY ar DESC;'
        result = conn.execute(query).fetchall()
       
    except Exception as e:
        print(e)
    return result