import os
import redis

def handleRedisCnx(conn):
    try:
        if conn is None:
            print("Connecting to Redis")
            conn = redis.StrictRedis(
                host=os.getenv('REDIS_HOST', 'redis-server'),
                port=6379)
        conn.ping()
        redisCnxStatus = 'OK'
    except Exception as exception:
        redisCnxStatus = 'Error - ' + exception.__class__.__name__ + " " + os.getenv('REDIS_HOST', 'redis-server') 
        print(redisCnxStatus)
        conn = None
    return redisCnxStatus,conn

