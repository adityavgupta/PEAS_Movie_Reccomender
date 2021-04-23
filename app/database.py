"""Defines all the functions related to the database"""
from app import db
import sys

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
        return user_id
    except Exception as e:
        print(e)
    conn.close()
    return 0

def delete_user(uname:str):
    conn=db.connect()
    try:
        user_id=conn.execute('SELECT MAX(Users.user_id) FROM Users WHERE name="{}";'.format(uname)).fetchall()[0][0]
        
    except:
        print("in except")
        return 1
    try:
        update = 'DELETE FROM Users WHERE user_id={};'.format(int(user_id))
        conn.execute(update)
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

def update_review(uname:str,title_id:str,type_id:str,rating:str,review:str)->int:
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
        update = 'UPDATE {} SET score={},comments="{}" WHERE user_id={} AND title_id="{}" AND type_id="{}";'.format(review_table,rating,review,int(user_id),title_id,type_id)
        conn.execute(update)
        print(update)
    except Exception as e:
        print(e)
    conn.close()
    return 0

def delete_review(uname:str,show_name:str,title_id:str,type_id:str)->int:
    conn = db.connect()
    review_table = 'Review_movie' if (type_id == 'movie') else 'Review_tv'
    try:
        user_id=conn.execute('SELECT MAX(Users.user_id) FROM Users WHERE name="{}";'.format(uname)).fetchall()[0][0]
        print(user_id)
        
    except:
        print("in except")
        return 1
    try:
        update = 'DELETE FROM {} WHERE user_id={} AND title_id="{}" AND type_id="{}";'.format(review_table, int(user_id),title_id,type_id)
        print(update)
        conn.execute(update)
    except Exception as e:
        print(e)
    conn.close()
    return 0

def insert_into_watched(username:str,list_of_movies:str,list_of_tv_shows:str,list_of_tv_show_impressions:str,list_of_movie_impressions:str)->int:
    print('insert_into_watched is being executed')
    print(list_of_movies,list_of_movie_impressions,list_of_tv_shows,list_of_tv_show_impressions)
    conn = db.connect()
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(username)
        user_id=conn.execute(query_uid).fetchall()[0][0]
        print(user_id)

        if(list_of_movies):
            movies_list = list_of_movies.split(",")
            movie_imp_list = list_of_movie_impressions.split(",")

            for i in range(len(movies_list)):
                query_mid = 'SELECT Movie.title_id FROM Movie WHERE Movie.name="{}";'.format(movies_list[i])
                movie_id=conn.execute(query_mid).fetchall()[0][0]
                insertion = 'INSERT INTO WATCHED_M VALUES("{}",{});'.format(movie_id, user_id)

                conn.execute(insertion)
                if i < len(movie_imp_list):
                    i_insertion = 'INSERT INTO Impressions_M VALUES("{}",{},{});'.format(movie_id, user_id, movie_imp_list[i])
                    print("i_insertion", i_insertion)
                    conn.execute(i_insertion)
    except:
        try:
            update_watched(username,list_of_movies,[],[],list_of_movie_impressions)
        except Exception as o:
            print('secondary update '+o)

    try:
        if(list_of_tv_shows):
            tv_imp_list = list_of_tv_show_impressions.split(",")
            tv_list = list_of_tv_shows.split(",")
            print(tv_list,tv_imp_list)
            for i in range(len(tv_list)):
                query_tid = 'SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}";'.format(tv_list[i])
                tv_id=conn.execute(query_tid).fetchall()[0][0]
                insertion = 'INSERT INTO WATCHED_T VALUES("{}",{});'.format(tv_id,user_id)
                #print(insertion)
                conn.execute(insertion)
                if i < len(tv_imp_list):
                    i_insertion = 'INSERT INTO Impressions_T VALUES("{}",{},{});'.format(tv_id, user_id, tv_imp_list[i])
                    print(i_insertion)
                    conn.execute(i_insertion)
    except:
        try:
            update_watched(username,[],list_of_tv_shows,list_of_tv_show_impressions,[])
        except Exception as o:
            print('secondary update '+o)
    conn.close()
    return 1


def update_watched(username:str,list_of_movies:str,list_of_tv_shows:str,list_of_tv_show_impressions:str,list_of_movie_impressions:str)->int:
    print('update_watched is being executed')
    conn = db.connect()
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(username)
        user_id=conn.execute(query_uid).fetchall()[0][0]
        print(user_id)
        if list_of_movies:
            movies_list = list_of_movies.split(",")
            movie_imp_list = list_of_movie_impressions.split(",")
            print(movies_list)
            for i in range(len(movies_list)):
                query_mid = 'SELECT Movie.title_id FROM Movie WHERE Movie.name="{}";'.format(movies_list[i])
                # print('movie_id: ')
                movie_id=conn.execute(query_mid).fetchall()[0][0]
                # print(movie_id)
                #insertion = 'UPDATE WATCHED_M SET user_id={} WHERE title_id="{}";'.format(movie_id, user_id)
                #conn.execute(insertion)
                if i < len(movie_imp_list):
                    i_insertion = 'UPDATE Impressions_M SET impression={} WHERE title_id="{}" AND user_id={};'.format(movie_imp_list[i],movie_id, user_id)
                    #print("i_insertion", i_insertion)
                    conn.execute(i_insertion)
        print('Loop one passed')

        if list_of_tv_shows:
            tv_imp_list = list_of_tv_show_impressions.split(",")
            tv_list = list_of_tv_shows.split(",")

            for i in range(len(tv_list)):
                query_tid = 'SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}";'.format(tv_list[i])
                print(query_tid)
                print('tv_id: ')
                tv_id=conn.execute(query_tid).fetchall()[0][0]
                print(tv_id)
                # insertion = 'UPDATE WATCHED_T SET user_id={} WHERE title_id="{}";'.format(tv_id,user_id)
                # conn.execute(insertion)
                if i < len(tv_imp_list):
                    i_insertion = 'UPDATE Impressions_T SET impression={} WHERE title_id="{}" AND user_id={};'.format(tv_imp_list[i],tv_id, user_id)
                    conn.execute(i_insertion)
        conn.close()
        return 0

    except Exception as e:
        #user doesn't exist
        conn.close()
        print(e)
        return 1

def lookup_watched(username:str,list_of_movies:str,list_of_tv_shows:str):
    conn = db.connect()
    results = []
    imp_val = {-1:'Bad',0:'Meh',1:"Good"}
    try:
        #verify if user exist
        query_uid = 'SELECT Users.user_id FROM Users WHERE Users.name="{}";'.format(username)
        user_id=conn.execute(query_uid).fetchall()[0][0]
        if list_of_movies:
            for movie in list_of_movies.split(','):
                try:
                    query_impression = 'SELECT im.impression FROM impressions_m im WHERE im.user_id = {} AND im.title_id = (SELECT Movie.title_id FROM Movie WHERE Movie.name="{}");'.format(user_id,movie)
                    #print(query_impression)
                    impression = conn.execute(query_impression).fetchall()[0][0]
                    results.append([movie,'Movie','Yes',imp_val[impression]])
                except:
                     results.append([movie,'Movie','No','N/A'])
        


        if list_of_tv_shows:
            for tv_show in list_of_tv_shows.split(','):
                try:
                    query_impression = 'SELECT im.impression FROM impressions_t im WHERE im.user_id = {} AND im.title_id = (SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}");'.format(user_id,tv_show)
                    #print(query_impression)
                    impression = conn.execute(query_impression).fetchall()[0][0]
                    results.append([tv_show,'TVShow','Yes',imp_val[impression]])
                except:
                    results.append([tv_show,'TVShow','No','N/A'])

        return results

    except Exception as e:
        print(e)        


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
            conn.execute(delete_watched_m)

        if tv_show != None:
            query_tid = 'SELECT TV_Show.title_id FROM TV_Show WHERE TV_Show.name="{}";'.format(tv_show)
            tv_id=conn.execute(query_tid).fetchall()[0][0]
            delete_impression_t = 'DELETE FROM Impressions_T WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(tv_id, user_id)
            conn.execute(delete_impression_t)
            delete_watched_t = 'DELETE FROM WATCHED_T WHERE title_id LIKE "{}" AND user_id LIKE {};'.format(tv_id, user_id)
            conn.execute(delete_watched_t)
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
    conn.close()
    return result

def paulQuery():
    conn = db.connect()
    try:
        query = 'SELECT * from ((select movie.release_year as ry, AVG(movie.avg_rating) as ar , "Movie" as type\
                from movie group by movie.release_year)\
                  union \
                (select tv_show.start_year, AVG(tv_show.avg_rating) as avg_ratings, "TV" as type\
                from tv_show group by tv_show.start_year)) as a\
                    order by a.ar desc;'
        #print(query)
        result = conn.execute(query).fetchall()
        #print(result)
        return result
    except Exception as e:
        print(e)
    conn.close()
    return result


def lookup_reviews(name:str, platforms:str, show_name:str):
    """
    Select * from
    (select m.name as title, rm.type_id as type, rm.score as rating, rm.comments as review, m.avg_rating as avg_sc
    from Review_movie rm join movie m on rm.title_id = m.title_id 
    where rm.user_id = {}
    union
    select t.name, rt.type_id, rt.score, rt.comments, t.avg_rating
    from Review_tv rt join tv_show t on rt.title_id = t.title_id 
    where rt.user_id = {}
    ) as a
    order by a.rating
    """

    result = None
    conn = db.connect()
    platforms = platforms.split(" ")
    contains_movie = "movie" in platforms
    contains_tv = "tv" in platforms
    # show_name = "%%" + show_name + "%%"
    print(show_name)
    try:
        user_id=conn.execute('SELECT MAX(Users.user_id) FROM Users WHERE name="{}";'.format(name)).fetchall()[0][0]
        print(user_id, contains_movie, contains_tv)
        
    except:
        print("in except")
        return 1

    
    #print(platform_where)
    try:
        if (contains_movie and contains_tv) or (not contains_movie and not contains_tv):
            query= 'Select * from\
                    (select m.name as title, rm.title_id as tid, rm.type_id as type, rm.score as rating, rm.comments as review, m.avg_rating as avg_sc\
                    from Review_movie rm join movie m on rm.title_id = m.title_id \
                    where rm.user_id = {} and m.name like "%%{}%%"\
                    union\
                    select t.name, rt.title_id, rt.type_id, rt.score, rt.comments, t.avg_rating\
                    from Review_tv rt join tv_show t on rt.title_id = t.title_id \
                    where rt.user_id = {} and t.name like "%%{}%%"\
                    ) as a\
                    order by a.rating'.format(user_id, show_name, user_id, show_name)
        elif contains_movie:
            query= 'select m.name as title, rm.title_id as tid, rm.type_id as type, rm.score as rating, rm.comments as review, m.avg_rating as avg_sc\
                    from Review_movie rm join movie m on rm.title_id = m.title_id \
                    where rm.user_id = {} and m.name like "%%{}%%"'.format(user_id, show_name)
        else:
            query= 'select m.name as title, rm.title_id as tid, rm.type_id as type, rm.score as rating, rm.comments as review, m.avg_rating as avg_sc\
                    from Review_tv rm join tv_show m on rm.title_id = m.title_id \
                    where rm.user_id = {} and m.name like "%%{}%%"'.format(user_id, show_name)
        print(query)
        result = conn.execute(query).fetchall()
       
    except Exception as e:
        print(e)
    return result


def getName(uid):
    conn = db.connect()
    query = "select name from users where user_id = '{}'".format(str(uid))
    user_name = conn.execute(query).fetchall()[0][0]
    return user_name


def getId(username, pswd):
    conn = db.connect()
    query = "select user_id from users where name = '{}' and passwd = '{}'".format(str(username),str(pswd))
    uid = conn.execute(query).fetchall()[0][0]
    return uid