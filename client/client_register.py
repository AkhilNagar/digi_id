import db_conn
from flask import jsonify
import bcrypt
import random

def registration(data):
    import bcrypt
    db=db_conn.Connect("clients")
    hashed=bcrypt.hashpw(data["password"].encode('utf-8'),bcrypt.gensalt())
    username=data["username"]
    event_code=random.randint(1000, 9999)
    if db.find_one({"username":username}):
        return jsonify({"msg":"username taken"})
    if db.find_one({"client_code":data["clientcode"]}):
        user_object={
        "username":username,
        "password":hashed,
        "client_code": data["clientcode"],
        "event_code": event_code
         }
        db.insert_one(user_object)
        return jsonify({"message":"Client Registration Successful","Client Code":data["clientcode"],"Event Code":event_code}),200
    else:
        client_code=random.randint(1000, 9999)
        user_object={
        "username":username,
        "password":hashed,
        "client_code": client_code,
        "event_code": event_code
         }
        db.insert_one(user_object)
        return jsonify({"message":"Client Registration Successful","Client Code":client_code,"Event Code":event_code}),200

    

    
    
    return jsonify({"message":"User created successfully"}),201


