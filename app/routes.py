""" Specifies routing for the application"""
from flask import render_template, request, jsonify, Flask
from app import app
from app import database as db_helper
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
    return render_template("index.html")

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _dob = request.form['inputDOB']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _dob and _password:
            
            # All Good, let's call MySQL
            # conn = mysql.connect()
            # cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            # cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            # data = cursor.fetchall()
            data = request.get_json()
            db_helper.insert_new_user(_name,_dob,_password)
            result = {'success': True, 'response': 'Done'}
            return jsonify(result)
            # if len(data) is 0:
            #     conn.commit()
            #     return json.dumps({'message':'User created successfully !'})
            # else:
            #     return json.dumps({'error':str(data[0])})
        else:
            return jsonify({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error':str(e)})
    # finally:
    #     cursor.close() 
    #     conn.close()

    