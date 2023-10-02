from flask import Flask,request,jsonify,redirect,url_for,flash
import bcrypt
from decouple import config
import pymongo
import certifi
import face_recognition
import cv2
import numpy as np
import socket
import random
import jwt
from datetime import datetime, timedelta
app = Flask(__name__)
app.config['SECRET_KEY'] = "testing"

global conn
global db
global ev

def connect_to_mongodb():
    global conn
    global db
    global username
    global password
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    conn = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
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
        access_expiry_time=datetime.utcnow()+timedelta(minutes=15)
        access_payload={"username":username,"exp":access_expiry_time}
        access_token=jwt.encode(access_payload,"trial",algorithm="HS256")

        refresh_expiry_time=datetime.utcnow()+timedelta(days=7)
        refresh_payload={"username":username,"exp":refresh_expiry_time}
        refresh_token=jwt.encode(refresh_payload,"trial",algorithm="HS256")

        return jsonify({"message":"Login successful","access_token":access_token,"refresh_token":refresh_token}),200
    else:
        return jsonify({"message":"Invalid credentials"}),400
    

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    try:
        # Verify the refresh token
        payload = jwt.decode(refresh_token, 'trial', algorithms=['HS256'])
        username = payload['username']
        user = db.users.find_one({'username': username})
        if not user:
            raise jwt.InvalidTokenError('Invalid refresh token')

        # Generate a new access token
        access_expiry_time = datetime.utcnow() + timedelta(minutes=15)
        access_payload = {'username': username, 'exp': access_expiry_time}
        access_token = jwt.encode(access_payload, 'trial', algorithm='HS256')

        return jsonify({'access_token': access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401

@app.route('/upload_encoding', methods=['POST'])
def upload_encoding():
    if 'image' not in request.files:
        return jsonify({"message":"No image found"}),400
    if 'username' not in request.form:
        return jsonify({"message":"No username found"}),400
    if not isinstance(request.form.get('username'),str):
        return jsonify({"message":"Invalid username"}),400
    
    username=request.form.get('username')
    frame=request.files['image'].read()
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)
    if len(faceEncoding)==0:
        return jsonify({"message":"No face detected"}),400
    faceEncoding=faceEncoding[0]

    encoding_array=faceEncoding.tolist()

    collection=db.users
    collection.update_one({"username":username},{"$set":{"encoding":encoding_array}})
    return jsonify({"message":"Encoding uploaded successfully"}),200


@app.route('/logout', methods=['POST'])
def logout():
    access_token = request.json.get('access_token')
    try:
        payload=jwt.decode(access_token,'trial',algorithms=['HS256'])
        username=payload['username']
        return jsonify({"message":"Logout successful"}),200
    except jwt.ExpiredSignatureError:
        return jsonify({"message":"Token has expired"}),401
    except jwt.InvalidTokenError:
        return jsonify({"message":"Invalid token"}),401
    
@app.route('/', methods=["POST","GET"])
def index():
    if random.random() < 0.5:  # 50% chance of failure (for testing purposes)
        # Simulate a failure by returning a 500 status code
        return "Internal Server Error", 500
    text=f"Welcome to container no.: {socket.gethostname()}"
    return text

@app.route('/page/<string:eventname>', methods=['GET','POST'])
def paging(eventname):
    db = conn.users
    collection =db.userdata
    db1=conn[eventname]
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
    # username = config('DB_USERNAME')
    # password = config('DB_PASSWORD')
    # client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    frame=request.data
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)[0]
    #print(faceEncoding)
    
    db=conn[eventname]
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
