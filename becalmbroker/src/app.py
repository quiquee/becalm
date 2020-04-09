# This is becalmbroker v1.0
# Released under
# Copyright: Copyright (C) 2020 Enrique Melero <enrique.melero@gmail.com>
# License: GPL-3
# The full text of the GPL is distributed as in
#  /usr/share/common-licenses/GPL-3 on Debian systems.
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json
from flask_apscheduler import APScheduler

sensorurl="http://localhost:8888"
sensorurl2="http://localhost:8887"
temperature = "-1"
pressure = "-1"
heartbeat= "-1"
SpO2= "-1"

scheduler = APScheduler()


@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=10)
def job1():
    with scheduler.app.app_context():

        # Gather data from sensor microsercice
        r = requests.get(sensorurl + '/rest/api/v1.0/temperature')

        if r.status_code == 200:
            print "Temp returns: " + r.text
            temperature=r.text
        else:
            print "Error: " + str(r.status_code)
            return

        r = requests.get(sensorurl + '/rest/api/v1.0/pressure')

        if r.status_code == 200:
            print "Press returns: " + r.text
            pressure=r.text
        else:
            print "Error: " + str(r.status_code)
            return

        # Gather data from pulsioximeter
        r = requests.get(sensorurl2 + '/rest/api/v1.0/heartbeat')

        if r.status_code == 200:
            print "HBR returns: " + r.text
            heartbeat=r.text
        else:
            print "Error: " + str(r.status_code)
            return

        r = requests.get(sensorurl2 + '/rest/api/v1.0/spo2')

        if r.status_code == 200:
            print "Press returns: " + r.text
            SpO2=r.text
        else:
            print "Error: " + str(r.status_code)
            return



    tempJ = {}
    presJ = {}
    hbrJ= {}
    spo2= {}
    tempJ['measure_type'] = 't'
    tempJ['measure_value'] = temperature.__str__()
    tempJ['date_generation'] = datetime.now().__str__()

    presJ['measure_type'] = 'p'
    presJ['measure_value'] = pressure.__str__()
    presJ['date_generation'] = datetime.now().__str__()

    hbrJ['measure_type'] = 'h'
    hbrJ['measure_value'] = heartbeat.__str__()
    hbrJ['date_generation'] = datetime.now().__str__()
 
    spo2J['measure_type'] = 'o'
    spo2J['measure_value'] = spo2.__str__()
    spo2J['date_generation'] = spo2.now().__str__()
 


# Post results to central server
    payload = []
    payload.append(tempJ)
    payload.append(presJ)
    payload.append(hbrJ)
    payload.append(spo2J)
    print json.dumps(payload) ;
    headers = {'Content-type': 'application/json'}
    r = requests.post('http://becalm.ngrok.io/data-sensor/2?id_device=1', headers=headers, json=payload) 

    if r.status_code == 201:
        print "Posted to server"
    else:
        print "Error posting to server: " + str(r.status_code)


app = Flask(__name__)

@app.route('/rest/api/v1.0/temperature', methods=['GET'])
def temp():
    r = requests.get(sensorurl + '/rest/api/v1.0/temperature')
    if r.status_code == 200:
        temperature=r.text
        print temperature
    else:
        print "Error: " + str(r.status_code)

    return temperature

@app.route('/rest/api/v1.0/pressure', methods=['GET'])
def press():
    r = requests.get(sensorurl + '/rest/api/v1.0/pressure')

    if r.status_code == 200:
        pressure=r.text
        print pressure
    else:
        print "Error: " + str(r.status_code)

        return pressure

@app.route('/rest/api/v1.0/debug', methods=['GET'])
def home2():
    r = requests.get(sensorurl + '/debug')
    return  r.json()

if __name__ == '__main__':
   scheduler.api_enabled = True
   scheduler.init_app(app)
   scheduler.start()
   app.run(debug = True,host='0.0.0.0', port=8081)
