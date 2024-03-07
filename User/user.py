'''
Endpoints for:
1) User Login
2) Upload Biometrics
3) View Booked Events
'''
from flask import Flask,request,jsonify
import user_register
import user_login
import create_biometrics
import jwt
import socket

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return f"Hello User {socket.gethostname()}"

@app.route('/register', methods=['POST'])
def register():
    data=request.json
    username=data["username"]
    password=data["password"]
    return user_register.registration(username,password)


@app.route('/login', methods=['POST'])
def login():
    data=request.json
    username=data["username"]
    password=data["password"]
    return user_login.login(username,password)

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    return user_login.refresh(refresh_token)

@app.route('/logout', methods=['POST'])
def logout():
    access_token = request.json.get('access_token')
    return user_login.logout(access_token)



@app.route('/kyc', methods=['POST'])
def kyc():

    access_token = request.headers.get('Authorization')
    payload=verify_jwt(access_token)
    if payload == None:
        return jsonify({"message":"Auth Failed"})

    if 'image' not in request.files:
        return jsonify({"message":"No image found"}),400
    if 'username' not in payload:
        return jsonify({"message":"Please Login to continue!"}),400
    if not isinstance(request.form.get('username'),str):
        return jsonify({"message":"Invalid username"}),400
    
    user_info = request.form
    frame=request.files['image'].read()
    return create_biometrics.upload_biometrics(user_info,frame)


if __name__=="__main__":
    app.run()

def verify_jwt(token, secret_key='trial', algorithms='HS256'):
    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return decoded_payload
    except ExpiredSignatureError:
        print("JWT has expired.")
    except DecodeError:
        print("Failed to decode JWT.")
    return None