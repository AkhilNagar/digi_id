import redis
import verify
import numpy as np
import json
import os
class RedisConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True)
            cls._instance.r = redis.Redis(connection_pool=pool)
        return cls._instance

def redis_conn():
    return RedisConnection().r



def delete_event(event_name):
    conn = redis_conn()
    if conn.sismember('events', event_name):
        conn.delete(event_name)
        conn.srem('events', event_name)
        return True  # Header and its key-value pairs deleted successfully
    else:
        return False  # Header doesn't exist

def populate_event(event_name,attendees):
    conn = redis_conn()
    for user in attendees:
        serialized_enc = json.dumps({
                                    "checkin":str(user["Check-in"]),
                                    "checkout":str(user["Check-out"]),
                                    "encoding":user["encoding"]})
        conn.hset(event_name, user["fullname"], serialized_enc)
    return None


def get_event(event_name,count):

    conn = redis_conn()
    if conn.exists(event_name) and count==conn.hlen(event_name):
        print("Cache Hit")
        event_data = conn.hgetall(event_name)
        return event_data
    else:
        return None

#  event1{
#   "name":{checkin checkout encoding},
#   "name":{checkin checkout encoding},
# }


















def cache_hit(eventname):
    r= redis_conn
    cached_enc=[]
    user_id=r.smembers(eventname)
    for i in user_id:
        arr=r.lrange(i,0,-1)
        arr=np.array(arr)
        arr=arr.astype('float64')
        cached_enc.append(arr)
    #PERFORM FACE RECOG HERE
    '''
    for i in client[eventname]:
        enc=r.get(client.eventname[i])
        flag=enc.compare_faces([enc],faceEncoding)
        if flag[0]==True:
            return True
    return False
    '''
    print("Cache Hit")
    return cached_enc
def cache_miss(eventname):
    r=redis_conn()
    data=mongo.get_data(eventname)
    enc=[]
    for obj in data:
        #print(obj)
        phone=obj['phone_number']
        encoding=obj['encoding']
        if r.exists(phone) == False:
            print("Entered :(")
            r.rpush(phone, *encoding) #pushes every element of the 'encoding' array into a list with key 'phone'
        r.sadd(eventname,phone)
        enc.append(encoding)
    print("Cache Miss")
    return enc