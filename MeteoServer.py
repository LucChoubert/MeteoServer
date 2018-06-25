import os

from flask import Flask, request
import MeteoFranceInterface.MeteoFranceInterface

import redis

def handleRedisCnx():
    global redisCnxStatus
    global conn
    try:
        if conn is None:
            conn = redis.StrictRedis(
                host=os.getenv('REDIS_HOST', 'redis_server'),
                port=6379)
        conn.ping()
        redisCnxStatus = 'OK'
    except Exception as exception:
        redisCnxStatus = 'Error - ' + exception.__class__.__name__ + " " + os.getenv('REDIS_HOST', 'redis_server')
        conn = None


app = Flask(__name__)

redisCnxStatus = None
conn = None

handleRedisCnx()

@app.route("/")
def root():
    var = "OK\n"
    return var

@app.route("/status")
def status():
    handleRedisCnx()
    var = "API Flask Server Up and Running\n"
    var = var + "Connection from: " + request.user_agent.string + "\n"
    var = var + "Redis Connection: " + redisCnxStatus + "\n"
    return var

@app.route("/meteo/biot/web")
def meteo1():
    handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_html_string()

@app.route("/meteo/biot/string")
def meteo2():
    handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    table = table
    return table.get_string() + "\n"