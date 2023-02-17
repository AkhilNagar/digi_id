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
            result=collection.find_one({"phone_number":phone},{"_id":0, "encoding":1})
            if result != None:
                coll.insert_one(result)
                print("value inserted ",result)
        return eventname
        
@app.route('/verify/<string:eventname>',methods=['POST'])
def verify(eventname):
    
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    frame=request.data
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)[0]
    #print(faceEncoding)
    
    db=client[eventname]
    collection=db[eventname]
    encs=collection.find({},{"encoding":1})
    print("encs",encs)
    enc=[]
    for obj in encs:
        enc.append(obj['encoding'])
    result = face_recognition.compare_faces(enc, faceEncoding)
    print(result)
    for i in result:
        if i == True:
            return "true"
    return "false"

if __name__=="__main__":
    app.run()

'''
route 1
client calls post request on api and passes json list of all users in the body
host receives list of all users for that event
performs query operations on the mongo db
a new temporary table is created with only registered users at host site
'''

'''
route 2
client calls api for a person
quick checking from table generated
returns true or false
'''