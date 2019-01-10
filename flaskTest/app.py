from flask import Flask, render_template, json, request
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# export FLASK_APP=signup.py
# flask run
# ps -fA | grep python


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'test'
app.config['MYSQL_DATABASE_DB'] = 'DroneOp'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

# conn = mysql.connector.connect(user='root', password='test',
#                                host='127.0.0.1',
#                                database='DroneOp',
#                                auth_plugin='mysql_native_password')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

#
# @app.route('/signUp',methods=['POST','GET'])
# def signUp():
#     try:
#         _name = request.form['inputName']
#         _email = request.form['inputEmail']
#         _password = request.form['inputPassword']
#
#         # validate the received values
#         if _name and _email and _password:
#
#             # All Good, let's call MySQL
#
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             _hashed_password = generate_password_hash(_password)
#             cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
#             data = cursor.fetchall()
#
#             if len(data) is 0:
#                 conn.commit()
#                 return json.dumps({'message':'User created successfully !'})
#             else:
#                 return json.dumps({'error':str(data[0])})
#         else:
#             return json.dumps({'html':'<span>Enter the required fields</span>'})
#
#     except Exception as e:
#         return json.dumps({'error':str(e)})
#     finally:
#         cursor.close()
#         conn.close()

@app.route('/form',methods=['POST','GET'])
def form():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputPilot']
        return _name
        # validate the received values
        # if inputPilot:
        #     queryCrew = "SELECT * FROM DroneOp.crew"
        #     # query = ("SELECT * FROM DroneOp.crew WHERE pilot = '" + queryCrew + "'")
        #     cursor.execute(queryCrew)
        #
        #     # pilotInfo = cursor.fetchone()
        #     data = cursor.fetchall()
        #     return data
    #     else:
    #         return json.dumps({'html':'<span>Enter the required fields</span>'})
    #
    # except Exception as e:
    #     return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
    # return render_template('form.html')

if __name__ == "__main__":
    app.run(port=5000)
