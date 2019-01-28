from flask import Flask, render_template, json, request
import flask
# from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import pymysql

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
        # json_data=[]
        # for result in results:
        #      json_data.append(dict(zip(row_headers,result)))
        self.cur.close
        self.con.close
        # return json.dumps(json_data)
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
        self.cur.execute("SELECT * FROM DroneOp.equipment LIMIT 50")
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

    def list_equip_details(self):
        self.cur.execute("SELECT * FROM DroneOp.equip_details LIMIT 50")
        result = self.cur.fetchall()
        self.cur.close
        self.con.close
        return result

@app.route('/')
def init():
    return render_template('index1.html')
    # return 'test'

@app.route('/form', methods=['POST','GET'])
def form():
    def db_query():
        db = Database()
        crew = db.list_crew_names()
        return crew
    res = db_query()
    temp = "Pilot's Name"
    res.insert(0,temp)
    return render_template('form.html', res=res)

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
    # def db_query():
    #     db = Database()
    #     pilotInfo = db.get_pilot()
    #     return pilotInfo
    # res = db_query()
    # return res
    return flask.jsonify({"result":selectedPilot})

@app.route('/list_crew', methods=['POST','GET'])
def crew():
    def db_query():
        db = Database()
        crew = db.list_crew()
        # crew = crew['pilot']
        return crew
    res = db_query()
    return render_template('list_crew.html', result=res, content_type='application/json')



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
