import mysql.connector
from datetime import date
import datetime

def main():
    conn = mysql.connector.connect(user='root', password='',
                      host='127.0.0.1',
                      database='DroneOp')
    cursor = conn.cursor()
    queryCrew = ("SELECT * FROM DroneOp.crew")
    queryEquip = ("SELECT * FROM DroneOp.Equipment")
    queryEquip_deet = ("SELECT * FROM DroneOp.equip_details")
    #
    # print("CREW")
    # cursor.execute(queryCrew)
    # myresult = cursor.fetchall()
    # for x in myresult:
    #     print(x)
    #
    # print("EQUIPMENT")
    #
    # cursor.execute(queryEquip)
    # myresult = cursor.fetchall()
    # for x in myresult:
    #     print(x)
    #
    # print("EQUIPMENT DETAILS")
    #
    # cursor.execute(queryEquip_deet)
    # myresult = cursor.fetchall()
    # for x in myresult:
    #     print(x)

    print("------------------")
    print("TEST \ncrew: Jon Caris \nModel: Mavic 4 Pro \nDrone: Pebble\n")
    queryCrew = "Jon Caris"
    # queryCrew = "test"
    queryModel = "Mavic 4 Pro"
    queryDrone = "Pebble"

    # query = ("SELECT * FROM DroneOp.crew WHERE pilot = 'Jon Caris'")
    query = ("SELECT * FROM DroneOp.crew WHERE pilot = '" + queryCrew + "'")
    cursor.execute(query)
    pilotInfo = cursor.fetchone()
    now = date.today()

    #pilot info
    pilot, pilot_pic_title, pilot_faa_uas_cert_num, pilot_iss_on, pilot_val_un ,pilot_ama_num = pilotInfo[0], pilotInfo[1], pilotInfo[2], pilotInfo[3], pilotInfo[4], pilotInfo[5]


    #model info
    query = ("SELECT * FROM DroneOp.equipment WHERE aircraft_mod = '" + queryModel + "'")
    cursor.execute(query)
    modelInfo = cursor.fetchone()
    aircraft_mod, drones = modelInfo[0], modelInfo[1]

    #drone info
    drone, drone_faa_reg, drone_iss_on, drone_val_un, drone_serial_num = 0,0,0,0,0
    drones = drones.split(",")
    for currDrone in drones:
        if (currDrone == queryDrone):
            query = ("SELECT * FROM DroneOp.equip_details WHERE drone = '" + currDrone + "'")
            cursor.execute(query)
            droneInfo = cursor.fetchone()
            drone, drone_faa_reg, drone_iss_on, drone_val_un, drone_serial_num  = droneInfo[0],droneInfo[1],droneInfo[2],droneInfo[3],droneInfo[4]


    print("------RESULTS----")
    print("PILOT " + pilot)
    print("pic title " + pilot_pic_title)
    print("faa uas cert num " + pilot_faa_uas_cert_num)
    print("issued on " + str(pilot_iss_on))
    print("valid until " + str(pilot_val_un))
    if(pilot_val_un < now):
        print("validation expired!!")
    print("ama num " + pilot_ama_num)

    print("MODEL " + aircraft_mod)
    print("drones " + str(drones))

    print("DRONE " + drone)
    print("drone faa reg " + drone_faa_reg)
    print("drone iss on " + str(drone_iss_on))
    print("drone val until " + str(drone_val_un))
    print("drone serial num " + drone_serial_num)

    cursor.close()
    conn.close()

main()
