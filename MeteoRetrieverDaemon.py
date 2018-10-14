import sys
import signal
import time
import daemon
import MeteoFranceInterface.MeteoFranceInterface
import RedisHandler.RedisHandler

def shutdown(signum, frame):  # signum and frame are mandatory
    print("EXITING NOW")
    sys.exit(0)
    
def get_meteo():
    while True:
        print("HELLO")
        global conn
        redisCnxStatus,conn = RedisHandler.RedisHandler.handleRedisCnx(conn)
        aCityCode = MeteoFranceInterface.MeteoFranceInterface.getCityCodeFromName("biot")
        city, extractionTime, resultDict = MeteoFranceInterface.MeteoFranceInterface.getDataFromMeteoFranceAPI2( aCityCode )
        #conn.hmset(city+'-'+extractionTime,resultDict)
        time.sleep(60)


conn = None 
with daemon.DaemonContext(stdout=sys.stdout,stderr=sys.stderr, signal_map={
            signal.SIGTERM: shutdown,
            signal.SIGTSTP: shutdown
        }):
    get_meteo()

