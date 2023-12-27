import sys
sys.path.append('..')
from DBConn import db_conn
from flask import jsonify
import bcrypt
def registration(username,password):
    import bcrypt
    db=db_conn.Connect("clients")
    if db.find_one({"username":username}):
        return jsonify({"message":"Username already exists"}),400
    
    hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    user_object={
        "username":username,
        "password":hashed
    }
    db.insert_one(user_object)
    return jsonify({"message":"User created successfully"}),201


