from flask import Flask, request
import MeteoFranceInterface.MeteoFranceInterface

app = Flask(__name__)

@app.route("/")
def hello():
    var = "Server Up and Running\n" + request.user_agent.string + "\n"
    return var

@app.route("/meteo/biot/web")
def meteo1():
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    return table.get_html_string()

@app.route("/meteo/biot/string")
def meteo2():
    aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
    table = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI( aCityCode )
    table = table
    return table.get_string() + "\n"