from flask import Flask, render_template, json, request
import flask
from werkzeug import generate_password_hash, check_password_hash
import pymysql
from datetime import date
import datetime
from darksky import forecast
import time

app = Flask(__name__)

class Database:
    # database related to obtaining info
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password = 'test'
        db = 'DroneOp'
        port=5000
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, autocommit=True, cursorclass=pymysql.cursors.DictCursor)

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
        self.cur.execute("SELECT * FROM DroneOp.crew WHERE pilot = '" + name +"'")
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
        self.cur.execute("SELECT * FROM DroneOp.equipment WHERE aircraft_mod = '" + name +"'")
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

    # def submit_form(self, date,pilot, pilot_pic_title, pilot_faa_uas_cert_num,
    #     pilot_issue_on, pilot_valid_until, pilot_ama_num, drone_model, drone, lat, long,
    #      temp, tempText):

    #INSERT INTO `DroneOp`.`log` (`date`, `camera_oppilot`, `camera_opfaa_uas_cert_num`, `camera_opissue_on`, `camera_opvalid_until`, `camera_opama_num`, `drone_oppilot`, `selected_model`, `lat`, `long`, `temp`, `tempText`) VALUES ('12/12/12', 'te', 'b', 'mn', 'm', 'm', 'v', 'b', 'b', 'b', 'b', 'b');

    def submit_form(self,camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
            drone_oppilot,

            selected_model,lat,long, temp, temp_text, mission):
        #submit_form(self,camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,selected_model,lat,long, temp, temp_text):

        self.cur = self.con.cursor()
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        #figure out long - neg decimal??
        print(camera_oppilot)
        print(camera_oppic_title)
        print(camera_opfaa_uas_cert_num)
        statement = "INSERT INTO DroneOp.log (date, camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,drone_oppilot, selected_model,lat,long, temp, temp_text, mission) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(statement, (now, camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
                drone_oppilot,

                selected_model,str(lat),str(long), str(temp), temp_text, mission))
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return now

@app.route('/')
def init():
    return render_template('index.html')

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
#
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
#
@app.route('/update_drone_info')
def update_drone_info():
    selectedDrone = request.args.get('selectedDrone')
    # def db_query():
    #     db = Database()
    #     modelInfo = db.get_model(selectedModel)
    #     return modelInfo
    # r = json.dumps(db_query())
    # res = json.loads(r)[0]
    # list = str(res['drones']).split(",")
    # list = 'test'
    return flask.jsonify({"result":selectedDrone})

@app.route('/get_weather')
def weather():
    key = "fd3f206d4c0f54c400bb09fd3ed45d55"
    latlng = request.args.get('latlng').replace(" ", "")
    lat = latlng.split(",")[0]
    long = latlng.split(",")[1]
    currLocation = forecast(key, lat, long)
    #TODO -- get all darksky info
    return flask.jsonify({"temp": currLocation.temperature, "text": currLocation.summary})

@app.route('/submit')
def submit():

    camera_oppilot = request.args.get('camera_oppilot')
    camera_oppic_title = request.args.get('camera_oppic_title')
    camera_opfaa_uas_cert_num= request.args.get('camera_opfaa_uas_cert_num')
    camera_opissue_on= request.args.get('camera_opissue_on')
    camera_opvalid_until= request.args.get('camera_opvalid_until')
    camera_opama_num= request.args.get('camera_opama_num')
    drone_oppilot = request.args.get('drone_oppilot')
    # drone_oppic_title = request.args.get('drone_oppic_title')
    # drone_opfaa_uas_cert_num= request.args.get('drone_opfaa_uas_cert_num')
    # drone_opissue_on= request.args.get('drone_opissue_on')
    # drone_opvalid_until= request.args.get('drone_opvalid_until')
    # drone_opama_num= request.args.get('drone_opama_num')
    # vis_obspilot = request.args.get('vis_obspilot')
    # vis_obspic_title = request.args.get('vis_obspic_title')
    # vis_obsfaa_uas_cert_num= request.args.get('vis_obsfaa_uas_cert_num')
    # vis_obsissue_on= request.args.get('vis_obsissue_on')
    # vis_obsvalid_until= request.args.get('vis_obsvalid_until')
    # vis_obsama_num= request.args.get('vis_obsama_num')
    selected_model= request.args.get('selected_model')
    lat= request.args.get('lat')
    long= request.args.get('long')
    temp= request.args.get('temp')
    temp_text= request.args.get('temp_text')
    mission= request.args.get('mission')

# vis_obs
# pilot, pic_title,faa_uas_cert_num, issue_on, valid_until, ama_num
    def db_query(camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,drone_oppilot,
            selected_model,lat,long, temp, temp_text,mission):
            db = Database()
            submit = db.submit_form(camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,drone_oppilot,
            selected_model,lat,long, temp, temp_text,mission)
            return submit
            # (camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
            #         drone_oppilot, drone_oppic_title,drone_opfaa_uas_cert_num, drone_opissue_on, drone_opvalid_until, drone_opama_num,
            #         vis_obspilot, vis_obspic_title,vis_obsfaa_uas_cert_num, vis_obsissue_on, vis_obsvalid_until, vis_obsama_num,
            #         selected_model,lat,long, temp, temp_text):
    res = db_query(camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
        drone_oppilot,
        selected_model,lat,long, temp, temp_text, mission)
    return flask.jsonify({"results": res})
    #     submit = db.submit_form(camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
    #     drone_oppilot, drone_oppic_title,drone_opfaa_uas_cert_num, drone_opissue_on, drone_opvalid_until, drone_opama_num,
    #     selected_model,lat,long, temp, temp_text)
    #     # db.commit()
    #     return submit
    # res = db_query(camera_oppilot, camera_oppic_title,camera_opfaa_uas_cert_num, camera_opissue_on, camera_opvalid_until, camera_opama_num,
    #     drone_oppilot, drone_oppic_title,drone_opfaa_uas_cert_num, drone_opissue_on, drone_opvalid_until, drone_opama_num,
    #     selected_model,lat,long, temp, temp_text)
    # return flask.jsonify({"results": res})

    #curr date
    # //pilot
    # selectedPilot
    # PicTitle
    # FaaUasCertNum
    # IssueOn
    # ValidUntil
    # AmaNum
    # //model
    # inputAircraftMod
    #
    # //drone
    # selectedDrone
    #
    # //location/weather
    # currLat
    # currLong
    # weatherTemp
    # weatherSumm



# @app.route('/update_pilot_info')
# def update_pilot_info():
#     selectedPilot = request.args.get('selectedPilot')
#     def db_query():
#         db = Database()
#         pilotInfo = db.get_pilot()
#         return pilotInfo
#     res = db_query()
#     return res
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



"""

camera_oppilot = request.args.get('camera_oppilot')
camera_oppic_title = request.args.get('camera_oppic_title')
camera_opfaa_uas_cert_num= request.args.get('camera_opfaa_uas_cert_num')
camera_opissue_on= request.args.get('camera_opissue_on')
camera_opvalid_until= request.args.get('camera_opvalid_until')
camera_opama_num= request.args.get('camera_opama_num')
drone_oppilot = request.args.get('drone_oppilot')
# drone_oppic_title = request.args.get('drone_oppic_title')
# drone_opfaa_uas_cert_num= request.args.get('drone_opfaa_uas_cert_num')
# drone_opissue_on= request.args.get('drone_opissue_on')
# drone_opvalid_until= request.args.get('drone_opvalid_until')
# drone_opama_num= request.args.get('drone_opama_num')
# vis_obspilot = request.args.get('vis_obspilot')
# vis_obspic_title = request.args.get('vis_obspic_title')
# vis_obsfaa_uas_cert_num= request.args.get('vis_obsfaa_uas_cert_num')
# vis_obsissue_on= request.args.get('vis_obsissue_on')
# vis_obsvalid_until= request.args.get('vis_obsvalid_until')
# vis_obsama_num= request.args.get('vis_obsama_num')
selected_model= request.args.get('selected_model')
lat= request.args.get('lat')
long= request.args.get('long')
temp= request.args.get('temp')
temp_text= request.args.get('temp_text')
mission= request.args.get('mission')


CREATE TABLE `DroneOp`.`log` (
  `datetime` DATETIME NOT NULL,
  `camera_oppilot` VARCHAR(45) NULL,
  `camera_opfaa_uas_cert_num` VARCHAR(45) NULL,
  `camera_opissue_on` VARCHAR(45) NULL,
  `camera_opvalid_until` VARCHAR(45) NULL,
  `camera_opama_num` VARCHAR(45) NULL,
  `drone_oppilot` VARCHAR(45) NULL,
  `selected_model` VARCHAR(45) NULL,
  `lat` VARCHAR(45) NULL,
  `long` VARCHAR(45) NULL,
  `temp` VARCHAR(45) NULL,
  `tempText` VARCHAR(45) NULL,
  `mission` VARCHAR(500) NULL,
  PRIMARY KEY (`date`));



INSERT INTO `DroneOp`.`flight_log` (`date`, `pilot`, `pilot_pic_title`, `pilot_faa_uas_cert_num`,
    `pilot_issue_on`, `pilot_valid_until`, `pilot_ama_num`, `drone_model`, `drone`, `lat`, `long`,
     `temp`, `tempText`) VALUES
     ('01-01-01', 'fgdh', 'fgh', 'dgfhdfgh', 'gfh', 'ssfg', 'rewgrg',
     'wreg', 'gwre', '456', '53', '34', 'dgfh');




CREATE TABLE `DroneOp`.`new_table` (
  `datetime` DATETIME NOT NULL,
  `pilot` VARCHAR(45) NULL,
  `faa_uas_cert_num` VARCHAR(45) NULL,
  `temp` FLOAT NULL,
  `tempSum` VARCHAR(45) NULL,
  `lat` FLOAT NULL,
  PRIMARY KEY (`datetime`));


CREATE TABLE `DroneOp`.`logs` (
  `datetime` DATETIME NOT NULL,
  `pilot` VARCHAR(45) NULL,
  `pic_title` VARCHAR(45) NULL,
  `faa_uas_cert_num` VARCHAR(45) NULL,
  `issue_on` VARCHAR(45) NULL,
  `valid_until` VARCHAR(45) NULL,
  `ama_num` VARCHAR(45) NULL,
  `selected_model` VARCHAR(45) NULL,
  `lat` DECIMAL(10,6) NULL,
  `long` DECIMAL(10,6) NULL,
  `temp` DECIMAL(10,6) NULL,
  `temp_text` VARCHAR(45) NULL,
  PRIMARY KEY (`datetime`));



camera_op


CREATE TABLE `DroneOp`.`logs1` (
  `datetime` DATETIME NOT NULL,
  `camera_oppilot` VARCHAR(45) NULL,
  `camera_oppic_title` VARCHAR(45) NULL,
  `camera_opfaa_uas_cert_num` VARCHAR(45) NULL,
  `camera_opissue_on` VARCHAR(45) NULL,
  `camera_opvalid_until` VARCHAR(45) NULL,
  `camera_opama_num` VARCHAR(45) NULL,
  `selected_model` VARCHAR(45) NULL,
  `lat` DECIMAL(10,6) NULL,
  `long` DECIMAL(10,6) NULL,
  `temp` DECIMAL(10,6) NULL,
  `temp_text` VARCHAR(45) NULL,
  PRIMARY KEY (`datetime`));


  CREATE TABLE `DroneOp`.`logs2` (
    `datetime` DATETIME NOT NULL,
    `camera_oppilot` VARCHAR(45) NULL,
    `camera_oppic_title` VARCHAR(45) NULL,
    `camera_opfaa_uas_cert_num` VARCHAR(45) NULL,
    `camera_opissue_on` VARCHAR(45) NULL,
    `camera_opvalid_until` VARCHAR(45) NULL,
    `camera_opama_num` VARCHAR(45) NULL,
    `drone_oppilot` VARCHAR(45) NULL,
    `drone_oppic_title` VARCHAR(45) NULL,
    `drone_opfaa_uas_cert_num` VARCHAR(45) NULL,
    `drone_opissue_on` VARCHAR(45) NULL,
    `drone_opvalid_until` VARCHAR(45) NULL,
    `drone_opama_num` VARCHAR(45) NULL,
    `vis_obspilot` VARCHAR(45) NULL,
    `vis_obspic_title` VARCHAR(45) NULL,
    `vis_obsfaa_uas_cert_num` VARCHAR(45) NULL,
    `vis_obsissue_on` VARCHAR(45) NULL,
    `vis_obsvalid_until` VARCHAR(45) NULL,
    `vis_obsama_num` VARCHAR(45) NULL,
    `selected_model` VARCHAR(45) NULL,
    `lat` DECIMAL(10,6) NULL,
    `long` DECIMAL(10,6) NULL,
    `temp` DECIMAL(10,6) NULL,
    `temp_text` VARCHAR(45) NULL,
    PRIMARY KEY (`datetime`));



pilot, pic_title,faa_uas_cert_num, issue_on, valid_until, ama_num, selected_model,lat,long, temp, temp_text)

"""
