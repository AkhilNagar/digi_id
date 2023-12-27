'''
Endpoints for:
Client Login
Create Event
'''

from flask import Flask,request
import client_register
import client_login
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


if __name__=="__main__":
    app.run()