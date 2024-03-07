import db_conn
import bcrypt
from flask import jsonify
import jwt
from datetime import datetime, timedelta

def login(username,password):
    db=db_conn.Connect("clients")
    try:
        user=db.find_one({"username":username})
    except:
        return jsonify({"message":"Username not present"}),400

    if user and bcrypt.checkpw(password.encode('utf-8'),user["password"]):
        access_expiry_time=datetime.utcnow()+timedelta(minutes=15)
        access_payload={"client_code":user["client_code"],"event_code":user["event_code"],"exp":access_expiry_time}
        access_token=jwt.encode(access_payload,"trial",algorithm="HS256")

        refresh_expiry_time=datetime.utcnow()+timedelta(days=7)
        refresh_payload={"username":username,"exp":refresh_expiry_time}
        refresh_token=jwt.encode(refresh_payload,"trial",algorithm="HS256")

        return jsonify({"message":"Login successful","access_token":access_token,"refresh_token":refresh_token}),200
    else:
        return jsonify({"message":"Invalid credentials"}),400

def refresh(refresh_token):
    db=db_conn.Connect("client")
    try:
        # Verify the refresh token
        payload = jwt.decode(refresh_token, 'trial', algorithms=['HS256'])
        username = payload['username']
        user = db.find_one({'username': username})
        if not user:
            raise jwt.InvalidTokenError('Invalid refresh token')

        # Generate a new access token
        access_expiry_time = datetime.utcnow() + timedelta(minutes=15)
        access_payload = {'username': username, 'exp': access_expiry_time}
        access_token = jwt.encode(access_payload, 'trial', algorithm='HS256')

        return jsonify({'access_token': access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401

def logout(access_token):
    db=db_conn.Connect("client")
    try:
        payload=jwt.decode(access_token,'trial',algorithms=['HS256'])
        username=payload['username']
        return jsonify({"message":"Logout successful"}),200
    except jwt.ExpiredSignatureError:
        return jsonify({"message":"Token has expired"}),401
    except jwt.InvalidTokenError:
        return jsonify({"message":"Invalid token"}),401