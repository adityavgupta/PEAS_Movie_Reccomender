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

def insert_new_review(uname:str,title_id:str,type_id:str,rating:str,review:str)->int:
    conn = db.connect()
    review_table = 'Review_movie' if (type_id == 'movie') else 'Review_tv'
    rating = float(rating)
    try:
        user_id=conn.execute('SELECT MAX(Users.user_id) FROM Users WHERE name="{}";'.format(uname)).fetchall()[0][0]
        print(user_id)
        
    except:
        print("in except")
        return 1
    try:
        insertion = 'INSERT INTO {} VALUES({},"{}","{}",{},"{}");'.format(review_table,int(user_id),title_id,type_id,rating,review)
        conn.execute(insertion)
        print(insertion)
    except Exception as e:
        print(e)
    conn.close()
    return 0

def insert_into_watched(username:str,list_of_movies:str,list_of_tv_shows:str,list_of_tv_show_impressions:str,list_of_movie_impressions:str)->int:
    conn = db.connect()
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(username)
        user_id=conn.execute(query_uid).fetchall()[0][0]
        print(user_id)

        movies_list = list_of_movies.split(",")
        tv_list = list_of_tv_shows.split(",")
        tm_imp_list = list_of_tv_show_impressions.split(",")
        movie_imp_list = list_of_movie_impressions.split(",")

        for i in range(len(movies_list)):
            query_mid = 'SELECT Movie.title_id FROM Movie WHERE Movie.name="{}";'.format(movies_list[i])
            movie_id=conn.execute(query_mid).fetchall()[0][0]
            insertion = 'INSERT INTO WATCHED_M VALUES("{}",{});'.format(movie_id, user_id)
            #conn.execute(insertion)
            if i < len(movie_imp_list):
                i_insertion = 'INSERT INTO Impressions_M VALUES("{}",{},{});'.format(movie_id, user_id, movie_imp_list[i])
                print("i_insertion", i_insertion)
                #conn.execute(i_insertion)
        
        print("wanna do something col")
        for i in range(len(tv_list)):
            query_tid = 'SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}";'.format(tv_list[i])
            tv_id=conn.execute(query_tid).fetchall()[0][0]
            insertion = 'INSERT INTO WATCHED_T VALUES("{}",{});'.format(tv_id,user_id)
            #conn.execute(insertion)
            if i < len(tv_imp_list):
                i_insertion = 'INSERT INTO Impressions_T VALUES("{}",{},{});'.format(tv_id, user_id, tv_imp_list[i])
                conn.execute(i_insertion)
        conn.close()

    except:
        #user doesn't exist
        conn.close()
        print("could not carry out request")
        return 1

def delete_from_watched(username:str,movie:str,tv_show:str)->int:
    print("yooo")
    conn = db.connect()
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(username)
        user_id=conn.execute(query_uid).fetchall()[0][0]

        if movie != None:
            query_mid = 'SELECT Movie.title_id FROM Movie WHERE Movie.name="{}";'.format(movie)
            movie_id=conn.execute(query_mid).fetchall()[0][0]
            delete_impression_m = 'DELETE FROM Impressions_M WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(movie_id, user_id)
            conn.execute(delete_impression_m)
            delete_watched_m = 'DELETE FROM WATCHED_M WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(movie_id, user_id)
            conn.execute(delete_impression_m)

        if tv_show != None:
            query_tid = 'SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}";'.format(tv_show)
            tv_id=conn.execute(query_tid).fetchall()[0][0]
            delete_impression_t = 'DELETE FROM Impressions_T WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(tv_id, user_id)
            conn.execute(delete_impression_t)
            delete_watched_t = 'DELETE FROM WATCHED_T WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(tv_id, user_id)
            conn.execute(delete_impression_t)
        conn.close()

    except:
        #user doesn't exist
        print("could not carry out request")
        conn.close()
        return 1

def emma_advanced_query():
    result = None
    conn = db.connect()
    try:
        query = 'select movie.title_id, AVG(Review_movie.score) as avg_score \
        from movie natural join Review_movie \
        group by movie.title_id \
        union \
        select tv_show.title_id, AVG(Review_tv.score) as avg_score \
        from tv_show natural join Review_tv \
        group by tv_show.title_id;'
        #print(query)
        result = conn.execute(query).fetchall()
        #print(result)
    except Exception as e:
        print(e)
    conn.close()
    return result

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

    platform_where = ''
    for i in range(1,len(platforms)):
        strn = platforms[i]
        if i == 1:
            platform_where += 'WHERE platform LIKE "%%'+strn+'%%" '
        else:
            platform_where += 'or platform LIKE "%%'+strn+'%%" '

    conn.close()
    
    try:
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

def paulQuery():
    conn = db.connect()
    try:
        query = 'select movie.release_year, AVG(movie.avg_rating) as avg_ratings, "Movie" as type from movie group by movie.release_year union select tv_show.start_year, AVG(tv_show.avg_rating) as avg_ratings, "TV" as type from tv_show group by tv_show.start_year'
        print(query)
        result = conn.execute(query).fetchall()
        print(result)
        return result
    except Exception as e:
        print(e)
    conn.close()
    return result

