from flask import Flask, render_template, json, request
import flask
# from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import pymysql
from datetime import date
import datetime
# from weather import Weather, Unit

app = Flask(__name__)

class Database:
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password = 'test'
        db = 'DroneOp'
        port=5000

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)

    def list_crew_names(self):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT pilot FROM DroneOp.crew")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        results = self.cur.fetchall()
        self.cur.close
        self.con.close
        return results

    def list_crew(self):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM DroneOp.crew")
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def get_pilot(self, name):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM DroneOp.crew WHERE pilot = '" + name +"'");
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def list_equipment(self):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM DroneOp.equipment")
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def list_models_equipment(self):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT aircraft_mod FROM DroneOp.equipment")
        row_headers=[x[0] for x in self.cur.description] #this will extract row headers
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def get_model(self, name):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM DroneOp.equipment WHERE aircraft_mod = '" + name +"'");
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def list_equip_details(self):
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM DroneOp.equip_details")
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

# def weather():
#     weather = Weather(unit=Unit.FAHRENHEIT)
#     # location = weather.lookup_by_location('northampton, ma')
#     # condition = location.condition
#     # temp = location.condition
#     # print(condition.text)
#     # print(condition.temp)
#
#     lookup = weather.lookup_by_latlng(42.318274,-72.637246)
#     condition = lookup.condition
#     temp = location.condition
#     # print(condition.text)
#     # print(condition.temp)
#     return condition.text, condition.temp
#

@app.route('/')
def init():
    return render_template('index1.html')
    # return 'test'

@app.route('/form', methods=['POST','GET'])
def form():
    def db_query():
        db = Database()
        crew = db.list_crew_names()
        model = db.list_models_equipment()
        return crew, model
    crewRes, modelRes = db_query()
    tempName = "Pilot's Name"
    tempModel = "Models"
    crewRes.insert(0,tempName)
    modelRes.insert(0, tempModel)
    # conditionText, temp = weather()
    # return render_template('form.html', crewRes=crewRes)
    return render_template('form.html', crewRes=crewRes, modelRes=modelRes)

# @app.route('/update')
# def update():
#     return render_template('update.html', content_type='application/json')
#
# @app.route('/calculate_result')
# def calculate_result():
#     a = int(request.args.get('val1'))
#     b = int(request.args.get('val2'))
#     return flask.jsonify({"result":a+b})

@app.route('/update_pilot_info')
def update_pilot_info():
    selectedPilot = request.args.get('selectedPilot')
    def db_query():
        db = Database()
        pilotInfo = db.get_pilot(selectedPilot)
        return pilotInfo
    r = json.dumps(db_query())
    res = json.loads(r)[0]
    return flask.jsonify({"PicTitle":str(res['pic_title']),
                            "FaaUasCertNum":str(res['faa_uas_cert_num']),
                            "IssueOn":str(res['issue_on']),
                            "ValidUntil":str(res['valid_until']),
                            "AmaNum":str(res['ama_num'])})

@app.route('/update_model_info')
def update_model_info():
    selectedModel = request.args.get('selectedModel')
    def db_query():
        db = Database()
        modelInfo = db.get_model(selectedModel)
        return modelInfo
    r = json.dumps(db_query())
    res = json.loads(r)[0]
    list = str(res['drones']).split(",")
    return flask.jsonify({"result":list})

@app.route('/update_drone_info')
def update_model_info():
    # selectedModel = request.args.get('selectedModel')
    # def db_query():
    #     db = Database()
    #     modelInfo = db.get_model(selectedModel)
    #     return modelInfo
    # r = json.dumps(db_query())
    # res = json.loads(r)[0]
    # list = str(res['drones']).split(",")
    list = 'test'
    return flask.jsonify({"result":list})



# @app.route('/update_pilot_info')
# def update_pilot_info():
#     selectedPilot = request.args.get('selectedPilot')
#     # def db_query():
#     #     db = Database()
#     #     pilotInfo = db.get_pilot()
#     #     return pilotInfo
#     # res = db_query()
#     # return res
#     return flask.jsonify({"result":selectedPilot})

# @app.route('/list_crew', methods=['POST','GET'])
# def crew():
#     def db_query():
#         db = Database()
#         crew = db.list_crew()
#         # crew = crew['pilot']
#         return crew
#     res = db_query()
#     return render_template('list_crew.html', result=res, content_type='application/json')



#
# @app.route('/list_equipment', methods=['POST','GET'])
# def equip():
#     def db_query():
#         db = Database()
#         # equipment = db.list_equipment()
#         self.cur.execute("SELECT * FROM DroneOp.equipment LIMIT 50")
#         equipment = self.cur.fetchall()
#         return equipment
#     res = db_query()
#     return render_template('list_equipment.html', result=res, content_type='application/json')
#
# @app.route('/list_equip_details', methods=['POST','GET'])
# def equip_details():
#     def db_query():
#         db = Database()
#         equip_details = db.list_equip_details()
#         return equip_details
#     res = db_query()
#     return render_template('list_equip_details.html', result=res, content_type='application/json')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
