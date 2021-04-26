""" Specifies routing for the application"""
from flask import render_template, request, jsonify, Flask, redirect, url_for
from app import app
from app import database as db_helper
from app import recommender as rec
import pandas as pd
import numpy as np

@app.route("/")
def homepage():
    """ returns rendered homepage """
    # items = db_helper.fetch_todo()
    ##print('lelelel')
    if request.cookies.get('UserIdCookie'):
        return renderHome()
    return render_template("index.html")

@app.route('/renderSignUp',methods=['POST'])
def renderSignUp():
    ##print('lelelele')
    return render_template("signup.html")

@app.route('/renderSignIn',methods=['POST'])
def renderSignIn():
    return render_template("signin.html")

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _dob = request.form['inputDOB']
        _password = request.form['inputPassword']
        print(_name, _dob, _password)

        # validate the received values
        if _name and _dob and _password:
            data = request.get_json()
            user_id = db_helper.insert_new_user(_name,_dob,_password)
            response = redirect(url_for("renderHome", variable='home'))
            response.set_cookie('UserIdCookie', user_id)
            return response
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    try:
        print(request.form.getlist('name')[0])
        #print(request.form.getlist('user_name')[0])
        username = request.form.getlist('name')[0]
        db_helper.delete_user(username)
        return signOut()

    except:
        print("ooooo")

@app.route('/signIn',methods=['POST'])
def signIn():
    try:
        _name = request.form['inputName']
        _password = request.form['inputPassword']
        #print(_name, _password)

        # validate the received values
        if _name and _password:
            data = request.get_json()
            if db_helper.verify_user_info(_name,_password) == 0:
                uid = db_helper.getId(_name, _password)
                response = redirect(url_for("renderHome"))
                response.set_cookie('UserIdCookie',str(uid))
                return response
    
            result = {'success': False, 'response': 'Done'}
            return jsonify(result)
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/signOut',methods=['POST'])
def signOut():
    response = redirect(url_for(".homepage"))
    response.set_cookie('UserIdCookie', '', expires=0)
    print(response)
    return response

@app.route('/renderHome')
def renderHome():
    user_name = db_helper.getName(request.cookies.get('UserIdCookie'))
    movie_recs = rec.get_recommendation(request.cookies.get('UserIdCookie'))
    keys=('Name', 'Type', 'Popularity', 'AverageRating','Platform', 'Genre')
    df = [dict(zip(keys, values)) for values in movie_recs]
    return render_template("home.html",name=user_name, items=df)

@app.route('/search',methods=['POST'])
def search():
    try:
        #print(request.form)
        #print(request.form.getlist('name'))
        #name = request.form[0][1]
        inputs = request.form.getlist('form')[0].split('&')
        split_inputs = [x.split('=') for x in inputs]
        params = dict()

        params['platform'] = ''
        for i in split_inputs:
            if i[0] in params:
                params[i[0]] += (','+i[1])
            else:
                params[i[0]] = ''+i[1]
        #print(params)
        show_name = params['inputName']
        show_platform = params['platform']
        show_start_date = params['inputStartDate']
        name = request.form.getlist('name')[0]

        # validate the received values
        if show_name or show_platform or show_start_date:
            result = db_helper.lookup(show_name, show_platform, show_start_date)
            if result:
                keys=('Name','Type','Title_id','Popularity', 'AverageRating','Platform')
                df = [dict(zip(keys, values)) for values in result]
                #print(df)
                return renderSearched(df)
            
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderSearched')
def renderSearched(df):
    user_name = db_helper.getName(request.cookies.get('UserIdCookie'))
    return render_template("searched.html", name=user_name, items=df)
    #return render_template("searched.html", name=name, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/leaveImpression',methods=['POST'])
def updateImpression():
    username = request.form.getlist('user_name')[0]
    showname = request.form.getlist('showname')[0]
    title_id = request.form.getlist('title_id')[0]
    type_ = request.form.getlist('type')[0]
    impression = request.form.getlist('impression')[0]
    imp_d = {'Dislike':0,'Like':1}
    print(title_id)
    try:
        if type_ == 'tvSeries':
            db_helper.insert_into_watched(username,'','{}'.format(showname),'{}'.format(str(imp_d[impression])),'')
        else:
            db_helper.insert_into_watched(username,'{}'.format(showname),'','','{}'.format(str(imp_d[impression])))
        result = {'success': True, 'response': 'Done'}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/review',methods=['POST'])
def review():
    try:
        print(request.form)
        username = request.form.getlist('user_name')[0]
        showname = request.form.getlist('showname')[0]
        title_id = request.form.getlist('title_id')[0]
        type_ = request.form.getlist('type')[0]
        update_type = request.form.getlist('update_type')[0]
        return renderReview(showname,title_id, type_, update_type)

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderReview')
def renderReview(showname,titleid, type_, update_type):
    user_name = db_helper.getName(request.cookies.get('UserIdCookie'))
    return render_template("review.html", username=username, showname=showname, titleid=titleid, type=type_, update_type=update_type)
    #return render_template("searched.html", name=name, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/submitReview',methods=['POST'])
def submitReview():
    try:
        print(request.form)
        user_name = request.form.getlist('user_name')[0]
        rating = request.form.getlist('rating')[0]
        review = request.form.getlist('review')[0]
        title_id = request.form.getlist('title_id')[0]
        type_ = request.form.getlist('type')[0]
        ##call helper function from database.py
        db_helper.insert_new_review(user_name, title_id, type_, rating, review)

        return renderHome()

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/updateReview',methods=['POST'])
def updateReview():
    try:
        print(request.form)
        user_name = request.form.getlist('user_name')[0]
        rating = request.form.getlist('rating')[0]
        review = request.form.getlist('review')[0]
        title_id = request.form.getlist('title_id')[0]
        type_ = request.form.getlist('type')[0]
        ##call helper function from database.py
        db_helper.update_review(user_name, title_id, type_, rating, review)

        return renderHome()

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/deleteReview',methods=['POST'])
def deleteReview():
    try:
        print(request.form)
        user_name = request.form.getlist('user_name')[0]
        show_name = request.form.getlist('showname')[0]
        title_id = request.form.getlist('title_id')[0]
        type_ = request.form.getlist('type')[0]
        ##call helper function from database.py
        db_helper.delete_review(user_name, show_name, title_id, type_)

        return renderHome()

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderWatched')
def renderWatched():
    return render_template("watched.html")

@app.route('/renderWatched_delete')
def renderWatched_delete():
    return render_template("watched_delete.html")

@app.route('/renderEmma')
def renderemma():
    result = db_helper.emma_advanced_query()
    keys=('_id','Score')
    df = [dict(zip(keys, values)) for values in result]
    return render_template("emma.html", items=df)

@app.route('/insertwatched',methods=['POST'])
def insertwatched():
    print("no")
    try:
        username = request.form['inputUsername']
        list_of_movies = request.form['inputMovies']
        list_of_tv_shows = request.form['inputTvShows']
        list_of_tv_show_impressions = request.form['inputTvShowImpressions']
        list_of_movie_impressions = request.form['inputMovieImpressions']

        # validate the received values
        print(username, list_of_movies)
        if username and (list_of_movies or list_of_tv_shows) and (list_of_tv_show_impressions or list_of_movie_impressions):
            #data = request.get_json()
            db_helper.insert_into_watched(username, list_of_movies, list_of_tv_shows, list_of_tv_show_impressions, list_of_movie_impressions)
            result = {'success': True, 'response': 'Done'}
            return jsonify(result)
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/updatewatched',methods=['POST'])
def updatewatched():
    print("no")
    try:
        username = request.form['inputUsername']
        list_of_movies = request.form['inputMovies']
        list_of_tv_shows = request.form['inputTvShows']
        list_of_tv_show_impressions = request.form['inputTvShowImpressions']
        list_of_movie_impressions = request.form['inputMovieImpressions']

        # validate the received values
        print(username, list_of_movies)
        if username and (list_of_movies and list_of_movie_impressions)or(list_of_tv_shows and list_of_tv_show_impressions ):
            #data = request.get_json()
            db_helper.update_watched(username, list_of_movies, list_of_tv_shows, list_of_tv_show_impressions, list_of_movie_impressions)
            result = {'success': True, 'response': 'Done'}
            return jsonify(result)
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/searchwatched',methods=['POST'])
def searchwatched():
    print("no")
    try:
        username = request.form['inputUsername']
        list_of_movies = request.form['inputMovies']
        list_of_tv_shows = request.form['inputTvShows']
        result = db_helper.lookup_watched(username,list_of_movies,list_of_tv_shows)
        print(result)
        if result:
            keys=('Name','Type','Watched','Impression')
            df = [dict(zip(keys, values)) for values in result]
            return render_template("watched.html",items=df)

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/w_deleted',methods=['POST'])
def w_deleted():
    try:
        username = request.form['deleteUsername']
        movie = request.form['deleteMovieImpression']
        tv_show = request.form['deleteTvShowImpressions']
        print("hai", username)

        data = request.get_json()
        db_helper.delete_from_watched(username, movie, tv_show)
        result = {'success': True, 'response': 'Done'}

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/paulQuery',methods=['GET'])
def paulQuery():
    try:
        result = db_helper.paulQuery()
        ret_result = []
        if result:
            for row in result:
                print(round(row[1],2))
                return_row = tuple((row[0],str(round(row[1],2)),row[2]))
                if row[0] != '\\N' and row[0] != '0':
                    ret_result.append(return_row)
            #ret_result = [tuple(x if isinstance(x, str) else round(x,2) for x in row) for row in result]
            # for one in ret_result:
            #     one[1] = round(one[1],2)
            print(ret_result)
            keys=('Year','avgRating','Type')
            df = [dict(zip(keys, values)) for values in ret_result]
            return renderPaulQuery(df)
        return jsonify({'error':'Nothing found'})
    except:
        return jsonify({'error':str(e)})

@app.route('/renderPaulQuery')
def renderPaulQuery(result):
    return render_template('Paul.html',items=result)

@app.route('/renderSearchReview',methods=['POST'])
def renderSearchReview():
    print(request.form)
    username = request.form.getlist('name')[0]
    return render_template('review_search.html', name=username)

@app.route('/searchReview',methods=['POST'])
def searchReview():
    try:
        # name = request.form[0][1]
        print(request.form)
        inputs = request.form.getlist('form')[0].split('&')
        split_inputs = [x.split('=') for x in inputs]
        params = dict()

        params['platform'] = ''
        for i in split_inputs:
            if i[0] in params:
                params[i[0]] += (i[1]+" ")
            else:
                params[i[0]] = i[1]
        show_platform = params['platform']
        show_name = params['inputName']
        name = request.form.getlist('name')[0]
        # print(params)
        # print(name, show_platform)

        # validate the received values
        if name or show_platform:
            result = db_helper.lookup_reviews(name, show_platform, show_name)
            if result:
                keys=('Title','Title_id', 'Type','Score','Review', 'AverageRating')
                df = [dict(zip(keys, values)) for values in result]
                #print(df)
                return renderSearchedReview(df,name)
            
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderSearchedReview')
def renderSearchedReview(df, name):
    return render_template("review_search.html", name=name, items=df)

@app.route('/goHome',methods=['POST'])
def goHome():
    ##username = request.form.getlist('name')[0]
    return renderHome()

@app.route('/getGallery',methods=['POST'])
def getGallery():
    items = []
    user_name = db_helper.getName(request.cookies.get('UserIdCookie'))
    # inputs = request.form.getlist('form')[0].split('&')
    # print(inputs)
    return renderGallery(user_name, items)

@app.route('/searchGallery',methods=['POST'])
def searchGallery():
    items = []
    user_name = db_helper.getName(request.cookies.get('UserIdCookie'))
    inputs = request.form.getlist('form')[0].split('&')
    print(inputs)
    print('ssss')
    return renderGallery(user_name, items)


def renderGallery(username, items):
    return render_template('gallery.html',name = username, items=items)