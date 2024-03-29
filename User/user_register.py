import db_conn
import bcrypt
from flask import jsonify
def registration(username,password):
    db=db_conn.Connect("users")
    if db.find_one({"username":username}):
        return jsonify({"message":"Username already exists"}),400
    
    hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    
    user_object={
        "username":username,
        "password":hashed
    }
    db.insert_one(user_object)
    return jsonify({"message":"User created successfully ","username":username}),201


