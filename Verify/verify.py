import os
print("FIRSTTTTT")
main_project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Get a list of all directories in the main project folder
all_dirs = [d for d in os.listdir(main_project_folder) if os.path.isdir(os.path.join(main_project_folder, d))]

# Print the list of folders
print("Folders in the main project folder:")
for folder in all_dirs:
    print(folder)

import sys
sys.path.append('..')
print("SECOND")
main_project_folder = os.path.dirname(os.path.abspath(__file__))
    # Get a list of all directories in the main project folder
all_dirs = [d for d in os.listdir(main_project_folder) if os.path.isdir(os.path.join(main_project_folder, d))]

# Print the list of folders
print("Folders in the main project folder:")
for folder in all_dirs:
    print(folder)


import db_conn
from flask import Flask,request,jsonify
import face_recognition
from datetime import datetime,timedelta
import cv2
import numpy as np
import jwt
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "Up and Running!"

@app.route('/',methods=['POST'])
def verify_user():
    frame=request.files['image'].read()

    access_token = request.headers.get('Authorization')
    payload=verify_jwt(access_token)
    if payload == None:
        return jsonify({"message":"Auth Failed"})
    if payload["client_code"]!=0:
        output_data=verify_user(payload,frame)
    else:
        return jsonify({"message":"Login with Client Credentials"})
    if output_data:
        return jsonify(output_data),200
    else:
        return jsonify({"message":"Failed to Verify"})

def verify_user(payload,frame):
    dbc=db_conn.Connect(str(payload["client_code"]))
    dbe=dbc[str(payload["event_code"])]

    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    try:
        faceEncoding=face_recognition.face_encodings(image)[0]
        if len(faceEncoding)==0:
            return {"message":"No face detected"}
    except:
        return {"message":"No face detected, Re-Scan"}

    date=datetime.today()
    yest= date - timedelta(days=1)
    if "{}-{}".format(payload["event_code"],date.strftime("%d-%m-%Y")) not in dbc.list_collection_names():
        result = dbe.find({
            "Check-in": {"$lte": date},
            "Check-out": {"$gte": date}
        })
        if result:
            dbc["{}-{}".format(payload["event_code"],date.strftime("%d-%m-%Y"))].insert_many(result)
        
        if "{}-{}".format(payload["event_code"],yest.strftime("%d-%m-%Y")) in dbc.list_collection_names():
            dbc["{}-{}".format(payload["event_code"],yest.strftime("%d-%m-%Y"))].drop()

                

    users= dbc["{}-{}".format(payload["event_code"],date.strftime("%d-%m-%Y"))].find()


    for user in users:
        result = face_recognition.compare_faces([user["encoding"]], faceEncoding)
        if result[0]:
            return {"message":"Welcome {}.".format(user["fullname"]),
                    "checkin":user["Check-in"],
                    "checkout":user["Check-out"],}
    return {"message":"No Booking"}



def verify_jwt(token, secret_key='trial', algorithms='HS256'):
    if token is None:
        return None 
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return decoded_payload
    except ExpiredSignatureError:
        print("JWT has expired.")
        return None
    except DecodeError:
        print("Failed to decode JWT.")
        return None
    return None

if __name__=="__main__":
    app.run()