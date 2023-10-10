from DBConn import db_conn
import face_recognition

def upload_biometrics(username,frame):
    db=db_conn.Connect("users")
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    faceEncoding=face_recognition.face_encodings(image)
    if len(faceEncoding)==0:
        return jsonify({"message":"No face detected"}),400
    faceEncoding=faceEncoding[0]

    encoding_array=faceEncoding.tolist()

    collection=db.users
    collection.update_one({"username":username},{"$set":{"encoding":encoding_array}})
    return jsonify({"message":"Encoding uploaded successfully"}),200
