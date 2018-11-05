import sys
import signal
import time
import daemon
import MeteoFranceInterface.MeteoFranceInterface
import RedisHandler.RedisHandler

def shutdown(signum, frame):  # signum and frame are mandatory
    print("MeteoRetrieverDaemon - EXITING NOW")
    sys.exit(0)
    
def get_meteo():
    global conn
    while True:
        print("MeteoRetrieverDaemon - Retrieving Meteo France data - "+time.strftime("%d/%m/%Y %H:%M:%S"))
        try:
            redisCnxStatus,conn = RedisHandler.RedisHandler.handleRedisCnx(conn)
            aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
            city, extractionTime, resultDict = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI2( aCityCode )
            conn.hmset(city+'-'+extractionTime,resultDict)
        except Exception as exception:
            print("...Exception caught")
        time.sleep(600)


conn = None 
with daemon.DaemonContext(stdout=sys.stdout,stderr=sys.stderr, signal_map={
            signal.SIGTERM: shutdown,
            signal.SIGTSTP: shutdown
        }):
    get_meteo()

