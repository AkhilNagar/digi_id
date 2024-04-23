import db_conn
import redis_conn
from flask import Flask,request,jsonify
import face_recognition
from datetime import datetime,timedelta
import cv2
import numpy as np
import jwt
import json
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

    event_name="{}-{}".format(payload["event_code"],date.strftime("%d-%m-%Y"))
    yest_event_name="{}-{}".format(payload["event_code"],yest.strftime("%d-%m-%Y"))

    if event_name not in dbc.list_collection_names():
        result = dbe.find({
            "Check-in": {"$lte": date},
            "Check-out": {"$gte": date}
        })
        if result:
            dbc[event_name].insert_many(result)
        
        if yest_event_name in dbc.list_collection_names():
            dbc[yest_event_name].drop()

                
    # Add a caching mechanism right here
    # get_event()
    # if returns list of encodings -> Cache hit
    #                              -> use the list to compare encodings
    # else -> Cache Miss
    #      -> Delete yesterday event header
    #      -> create_event
    #      -> populate event(user["encoding"])
    #      -> use the list to compare encodings
    count=dbc[event_name].count_documents({})
    all_encodings=redis_conn.get_event(event_name,count)
    if all_encodings is not None:
        print("Cache Hit")
        for key,value in all_encodings.items():
            value=json.loads(value)
            result = face_recognition.compare_faces([np.array(value["encoding"])], faceEncoding)
            if result[0]:
                    return {"message":"Welcome {}.".format(key),
                            "checkin":value["checkin"],
                            "checkout":value["checkout"],}
        return {"message":"No Booking"} 
    else:
        print("Cache Miss")
        users= list(dbc[event_name].find())
        try:
            redis_conn.delete_event(yest_event_name)
            redis_conn.populate_event(event_name,users)
        except:
            print("Could not delete/populate event")
        finally:
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
        return "JWT has expired."
    except DecodeError:
        print("Failed to decode JWT.")
        return "Failed to decode JWT."
    return None

if __name__=="__main__":
    app.run()