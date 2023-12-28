from DBConn import db_conn
import face_recognition
from datetime import datetime
import cv2
import numpy as np
def verify_user(username,frame):
    dbc=db_conn.Connect("clients")
    client=dbc.find_one({"username":username})
    cc=client["client_code"]

    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)[0]
    if len(faceEncoding)==0:
        return {"message":"No face detected"}
    if cc==11:
        db=db_conn.Connect("hotel")
        date=datetime.today().date().strftime("%d-%m-%Y")
        dbh=db[date]
        users= dbh.find()
        for user in users:
            result = face_recognition.compare_faces([user["encoding"]], faceEncoding)
            if result[0]:
                return {"message":"Welcome {}.".format(user["fullname"]),
                        "checkin":user["Check-in"],
                        "checkout":user["Check-out"],}
    return {"message":"No Booking"}