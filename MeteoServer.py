import RedisHandler.RedisHandler

from flask import Flask, request
import MeteoFranceInterface.MeteoFranceInterface

def handleRedisCnx(): 
    global conn
    redisCnxStatus,conn = RedisHandler.RedisHandler.handleRedisCnx(conn)
    return redisCnxStatus

app = Flask(__name__)
conn = None

@app.route("/")
def root():
    var = "OK\n"
    return var

@app.route("/status")
def status():
    redisCnxStatus = handleRedisCnx()
    var = "API Flask Server Up and Running\n"
    var = var + "Connection from: " + request.user_agent.string + "\n"
    var = var + "Redis Connection: " + redisCnxStatus + "\n"
    return var

@app.route("/meteo/biot/web")
def meteo1():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_html_string()

@app.route("/meteo/biot/string")
def meteo2():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_string() + "\n"

@app.route("/meteo/biot/redis")
def meteo3():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    city, extractionTime, resultDict = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI2( aCityCode )
    conn.hmset(city+'-'+extractionTime,resultDict)
    return "OK"
