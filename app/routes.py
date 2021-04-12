""" Specifies routing for the application"""
from flask import render_template, request, jsonify, Flask
from app import app
from app import database as db_helper
import pandas as pd
import numpy as np
#from werkzeug import generate_password_hash, check_password_hash
# @app.route("/delete/<int:task_id>", methods=['POST'])
# def delete(task_id):
#     """ recieved post requests for entry delete """

#     try:
#         db_helper.remove_task_by_id(task_id)
#         result = {'success': True, 'response': 'Removed task'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    # items = db_helper.fetch_todo()
    ##print('lelelel')
    return render_template("index.html")

@app.route('/renderSignUp')
def renderSignUp():
    ##print('lelelele')
    return render_template("signup.html")

@app.route('/renderSignIn')
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
            db_helper.insert_new_user(_name,_dob,_password)
            result = {'success': True, 'response': 'Done'}
            return jsonify(result)
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

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
                return renderHome(_name)
    
            result = {'success': False, 'response': 'Done'}
            return jsonify(result)
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderHome')
def renderHome(name):
    return render_template("home.html", name=name)

@app.route('/search',methods=['POST'])
def search():
    try:
        print(request.form)
        print(request.form.getlist('name'))
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
        print(params)
        show_name = params['inputName']
        show_platform = params['platform']
        show_start_date = params['inputStartDate']
        name = request.form.getlist('name')[0]

        # validate the received values
        if show_name or show_platform or show_start_date:
            result = db_helper.lookup(show_name, show_platform, show_start_date)
            if result:
                keys=('Name','Type','Popularity', 'AverageRating','Platform')
                df = [dict(zip(keys, values)) for values in result]
                print(df)
                return renderSearched(df,name)
            
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderSearched')
def renderSearched(df, name):
    return render_template("searched.html", name=name, items=df)
    #return render_template("searched.html", name=name, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/review',methods=['POST'])
def review():
    try:
        print(request.form)
        username = request.form.getlist('user_name')[0]
        showname = request.form.getlist('showname')[0]
        title_id = request.form.getlist('title_id')[0]
        return renderReview(username, showname,title_id)

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/renderReview')
def renderReview(username, showname,title_id):
    return render_template("review.html", username=username, showname=showname, titleid=title_id)
    #return render_template("searched.html", name=name, tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/submitReview',methods=['POST'])
def submitReview():
    try:
        print(request.form)
        rating = request.form['inputScore']
        review = request.form['inputReview']

    except Exception as e:
        return jsonify({'error':str(e)})