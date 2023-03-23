from flask import Flask,request,jsonify
from decouple import config
import pymongo
import json
import certifi
import os
import face_recognition
import cv2
import numpy as np
import io
import socket
import redis

app = Flask(__name__)


@app.route('/', methods=["POST","GET"])
def index():
    text=f"Welcome to container no.: {socket.gethostname()}"
    return text

@app.route('/page/<string:eventname>', methods=['GET','POST'])
def paging(eventname):
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    db = client.users
    collection =db.userdata
    db1=client[eventname]
    #collname=uuid.uuid4().hex
    coll=db1[eventname]
    #response=[]
    if(request.method=="POST"):
        print("POSTYY")
        user=request.json
        #print ("USER")
        for obj in user:
            phone=obj["phone"]
            result=collection.find_one({"phone_number":phone},{"_id":0, "phone_number":1, "encoding":1})
            if result != None:
                coll.insert_one(result)
                print("value inserted ",result)
        return eventname
        
@app.route('/verify/<string:eventname>',methods=['POST'])
def verify(eventname):
    
    # Make connection
    #encs is an array of objects of encodings for the particular event
    redi.redis_conn()
    
    
    frame=request.data
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)[0]
    
    
    if r.exists(eventname):
        enc=redi.cache_hit(eventname)
        result = face_recognition.compare_faces(enc, faceEncoding)
        print(result)
        for i in result:
            if i == True:
                return "true"
        return "false"
        
    else:
        enc=redi.cache_miss(eventname)
        result = face_recognition.compare_faces(enc, faceEncoding)
        print(result)
        for i in result:
            if i == True:
                return "true"
        return "false"
    
    
    # print("encs",encs)
    # enc=[]
    # for obj in encs:
    #     enc.append(obj['encoding'])
    #     


    
class mongo():

    def mongoconn():
        global client
        username = config('DB_USERNAME')
        password = config('DB_PASSWORD')
        client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
        
    def get_data(eventname):
        mongo.mongoconn()    
        db=client[eventname]
        collection=db[eventname]
        data=collection.find({},{"_id":0,"phone_number":1,"encoding":1})
        # count=collection.find({},{"phone_no":1,"encoding":1}).count()
        # if count==0:
        #     paging(eventname)
        #     data=collection.find({},{"phone_no":1,"encoding":1})
        # else:
        #     data=collection.find({},{"phone_no":1,"encoding":1})
        return data



class redi():
    '''
    Structure of hashset: 
        client1{
                event1:['k1','k2','k3']
                event2:['k4','k5','k6']
                event3:['k7','k8','k9']
            }
    Structure of redis list:
        k1=[1,2,3]
    '''
        
    def redis_conn():
        global redis
        global r
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        return 0
    def cache_hit(eventname):
        cached_enc=[]
        user_id=r.smembers(eventname)
        for i in user_id:
            arr=r.lrange(i,0,-1)
            arr=np.array(arr)
            arr=arr.astype('float64')
            cached_enc.append(arr)
        
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
        





if __name__=="__main__":
    app.run()

