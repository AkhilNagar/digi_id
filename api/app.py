from flask import Flask,request,jsonify,redirect,url_for,flash
import bcrypt
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
import random
app = Flask(__name__)

global conn
global db
global ev

def connect_to_mongodb():
    global conn
    global db
    global username
    global password
    # username = config('DB_USERNAME')
    # password = config('DB_PASSWORD')
    conn = pymongo.MongoClient(f"mongodb+srv://kaushik:kaushiksdb@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    db = conn.users

connect_to_mongodb()

@app.route('/register', methods=['POST'])
def register():
    data=request.json
    username=data["username"]
    password=data["password"]

    if db.users.find_one({"username":username}):
        return jsonify({"message":"Username already exists"}),400
    
    hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    user_object={
        "username":username,
        "password":hashed
    }
    db.users.insert_one(user_object)
    return jsonify({"message":"User created successfully"}),201

@app.route('/collections', methods=['GET'])
def list_collections():
    # List all collections in the current database
    collection_names = db.list_collection_names()

    if collection_names:
        return jsonify({"collections": collection_names}), 200
    else:
        return jsonify({"message": "No collections found in the database"}), 404

@app.route('/login', methods=['POST'])
def login():
    data=request.json
    username=data["username"]
    password=data["password"]
    user=db.users.find_one({"username":username})
    if user and bcrypt.checkpw(password.encode('utf-8'),user["password"]):
        return jsonify({"message":"Login successful"}),200
    else:
        return jsonify({"message":"Invalid credentials"}),400
    



@app.route('/', methods=["POST","GET"])
def index():
    if random.random() < 0.5:  # 50% chance of failure (for testing purposes)
        # Simulate a failure by returning a 500 status code
        return "Internal Server Error", 500
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