import RedisHandler.RedisHandler
import datetime

from flask import Flask, request
import MeteoFranceInterface.MeteoFranceInterface

def handleRedisCnx(): 
    global conn
    redisCnxStatus,conn = RedisHandler.RedisHandler.handleRedisCnx(conn)
    return redisCnxStatus

app = Flask(__name__)
conn = None

@app.route("/api")
def root():
    var = "MeteoServer API OK\n"
    return var

@app.route("/api/status")
def status():
    redisCnxStatus = handleRedisCnx()
    var = "API Flask Server Up and Running\n"
    var = var + "Connection from: " + request.user_agent.string + "\n"
    var = var + "Redis Connection: " + redisCnxStatus + "\n"
    return var

@app.route("/api/meteo/biot/web")
def meteo1():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_html_string()

@app.route("/api/meteo/biot/string")
def meteo2():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_string() + "\n"

@app.route("/api/meteo/biot/web/redis")
def meteo3():
    redisCnxStatus = handleRedisCnx()
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    #Let's look in redis instead of going live to MF website
    #city, extractionTime, resultDict = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI2( aCityCode )
    listKeys = conn.keys('Biot'+'*')
    lastKey = None
    #'Biot-15-October-2018-00:46'
    for k in listKeys:
       city, day, month, year, hourminute = k.decode('utf-8').split('-')
       hour, minute = hourminute.split(':')
       currentDateTime = datetime.datetime.strptime(day+'/'+month+'/'+year+' '+hour+':'+minute, "%d/%B/%Y %H:%M")
       if lastKey is not None:
          lastCity, lastDay, lastMonth, lastYear, lastHourlastMinute = lastKey.split('-')
          lastHour, lastMinute = lastHourlastMinute.split(':')
          lastDateTime = datetime.datetime.strptime(lastDay+'/'+lastMonth+'/'+lastYear+' '+lastHour+':'+lastMinute, "%d/%B/%Y %H:%M")
          if currentDateTime > lastDateTime:
             lastKey = k.decode('utf-8')
       else:
          lastKey = k.decode('utf-8')
    lastCity, lastDay, lastMonth, lastYear, lastHourlastMinute = lastKey.split('-')
    lastHour, lastMinute = lastHourlastMinute.split(':')
    table = MeteoFranceInterface.MeteoFranceInterface.format(lastCity, lastDay+'/'+lastMonth+'/'+lastYear+' '+lastHour+':'+lastMinute, conn.hgetall(lastKey))
    return table.get_html_string()
    #return lastKey
    #conn.hmset(city+'-'+extractionTime,resultDict)
    #return "OK-OK"
