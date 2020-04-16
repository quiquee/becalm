
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
import board
import busio
import adafruit_bmp280
import json

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()


temperature = -1
pressureh = -1
pressurel = -1
lpressure= -1
lastmeasure = datetime.now()
lbreath= datetime.now()
rr = -1
ra = -1
tmpPhase=""

def job1():

    global lpressure, pressureh, pressurel,temperature, rr, lbreath, tmpPhase, ra

    temperature=bmp280.temperature
    tmpPressure=bmp280.pressure
    lastBreath=datetime.now()
    if pressurel==-1:
        pressurel=tmpPressure
    if pressureh==-1:
        pressureh=tmpPressure
    print('This is job1')

    # Inspira
    if tmpPressure < (pressureh+pressurel)/2:
        # Cambiamos a Inspirar
        # podemos medir el ritmo respiratorio
        # y debemos guardar la amplitud respiratoria
        if tmpPhase == 'E' :
            rr=60 / ( datetime.now() - lbreath ).total_seconds()
            lbreath=datetime.now()
            ra=pressureh-pressurel

        if tmpPressure < pressurel:
            pressurel = tmpPressure

        tmpPhase="I"

    # Expira
    if tmpPressure > (pressureh+pressurel)/2:
        # Cambiamos a Expirar
        # podemos medir el ritmo respiratorio
        if tmpPhase == 'I'  :
            rr=60 / (datetime.now() - lbreath).total_seconds()
            lbreath=datetime.now()
            ra=pressureh-pressurel

            pressureh = (pressureh+pressurel)/2

        if tmpPressure > pressureh:
            pressureh=tmpPressure

        tmpPhase="E"

    lpressure = tmpPressure
    lastmeasure = datetime.now()

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
bmp280.sea_level_pressure = 1013.25

job = scheduler.add_job(job1, 'interval', seconds=2)

@app.route('/rest/api/v1.0/temperature', methods=['GET'])
def get_tasks():
    return  str(temperature)

@app.route('/rest/api/v1.0/pressure', methods=['GET'])
def get_val2():
    return str(lpressure)


@app.route('/debug', methods=['GET'])
def debug():
    output = dict()
    output['Temperatura'] = round(temperature,2)
    output['Presión Actual'] = round(lpressure,2)
    output['Amplitud Respiratoria'] = round(ra, 2)
    output['Presión Expiración'] = round(pressureh,2)
    output['Presión Inspiración'] = round(pressurel,2)
    output['Respiraciones por Minuto'] = round(rr,2)
    output['Última Respiración'] = str(lbreath)
    output['Fase Respiratoria'] = tmpPhase
    return json.dumps(output, ensure_ascii=False)

if __name__ == '__main__':

    app.debug = True
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host='0.0.0.0', port=8888)
