from DBConn import db_conn
import bcrypt
def registration(username,password):
    import bcrypt
    db=db_conn.Connect("clients")
    if db.clients.find_one({"username":username}):
        return jsonify({"message":"Username already exists"}),400
    
    hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    user_object={
        "username":username,
        "password":hashed
    }
    db.clients.insert_one(user_object)
    return jsonify({"message":"User created successfully"}),201


