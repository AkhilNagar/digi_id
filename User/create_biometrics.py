import db_conn
import face_recognition
import cv2
import numpy as np
from flask import jsonify

def upload_biometrics(user_info,frame):
    db=db_conn.Connect("users")
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)
    if len(faceEncoding)==0:
        return jsonify({"message":"No face detected"}),400
    faceEncoding=faceEncoding[0]

    encoding_array=faceEncoding.tolist()
    
    db.update_one(
    {"username": user_info.get('username')},
    {
        "$set": {
            "encoding": encoding_array,
            "first_name": user_info.get('username'),  
            "last_name": user_info.get('lastname'),  
            "phone": int(user_info.get('phone')),  
            "email": user_info.get('email')  
        }
    }
)
    return jsonify({"message":"{}'s encoding uploaded successfully".format(user_info.get('username'))}),200
