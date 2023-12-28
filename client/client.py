from flask import Flask,request,jsonify
import client_register
import client_login
import verify
from Book import book_hotel
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "HelloWorld"

@app.route('/register', methods=['POST'])
def register():
    data=request.json
    username=data["username"]
    password=data["password"]
    return client_register.registration(username,password)

@app.route('/login', methods=['POST'])
def login():
    data=request.json
    username=data["username"]
    password=data["password"]
    return client_login.login(username,password)

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    return client_login.refresh(refresh_token)

@app.route('/logout', methods=['POST'])
def logout():
    access_token = request.json.get('access_token')
    return client_login.logout(access_token)

@app.route('/createevent', methods=['POST'])
def create_event():
    return create_event.create_event()

@app.route('/bookhotel', methods=['POST'])
def bookhotel():
    data= request.json
    access_token = request.headers.get('Authorization')
    payload=verify_jwt(access_token)
    data["digiid"]=payload["digiid"]
    if (book_hotel.book_hotel(data)):
        return jsonify({"message":"Booking Successful"}),200
    else:
        return jsonify({"message":"Booking Failed"}),400

@app.route('/verify', methods=['POST'])
def verify_user():
    frame=request.files['image'].read()

    access_token = request.headers.get('Authorization')
    payload=verify_jwt(access_token)
    if payload == None:
        return jsonify({"message":"Auth Failed"})
        
    output_data=verify.verify_user(payload["username"],frame)
    if output_data:
        return jsonify(output_data)
    else:
        return jsonify({"message":"Failed to Verify"})

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