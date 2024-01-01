from DBConn import db_conn
import face_recognition
from datetime import datetime,timezone
import cv2
import numpy as np
import isodate
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
    
    if "{}-master".format(payload["event_code"]) not in dbc.list_collection_names():
        date=datetime.today().date()         
        result = dbe.find({
            "Check-in": {"$lte": date},
            "Check-out": {"$gte": date}
        })
        print("result",result)
        if result:
            dbc["{}-master".format(payload["event_code"])].insert_many(result)
                

    users= dbc["{}-master".format(payload["event_code"])].find()


    for user in users:
        result = face_recognition.compare_faces([user["encoding"]], faceEncoding)
        if result[0]:
            return {"message":"Welcome {}.".format(user["fullname"]),
                    "checkin":user["Check-in"],
                    "checkout":user["Check-out"],}
    return {"message":"No Booking"}