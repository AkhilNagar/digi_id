import sys
sys.path.append('..')
import os
print("HELOOOO")
from flask import Flask,request,jsonify
main_project_folder = os.path.dirname(os.path.abspath(__file__))
    # Get a list of all directories in the main project folder
all_dirs = [d for d in os.listdir(main_project_folder) if os.path.isdir(os.path.join(main_project_folder, d))]

# Print the list of folders
print("Folders in the main project folder:")
for folder in all_dirs:
    print(folder)   
import client_register
import client_login
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
    return client_register.registration(data)

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
    if payload == None:
        return jsonify({"message":"Auth Failed"}),400
    if payload["digiid"] != 0:
        data["digiid"]=payload["digiid"]
    else:
        return jsonify({"message":"Please complete KYC to book"}),400
    if (book_hotel.book_hotel(data)):
        return jsonify({"message":"Booking Successful"}),200
    else:
        return jsonify({"message":"Booking Failed"}),400
    
if __name__=="__main__":
    app.run()

def verify_jwt(token, secret_key='trial', algorithms='HS256'):
    if token is None:
        return None 
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