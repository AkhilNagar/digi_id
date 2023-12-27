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

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return "HelloWorld"

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



@app.route('/upload_encoding', methods=['POST'])
def upload_encoding():
    if 'image' not in request.files:
        return jsonify({"message":"No image found"}),400
    if 'username' not in request.form:
        return jsonify({"message":"No username found"}),400
    if not isinstance(request.form.get('username'),str):
        return jsonify({"message":"Invalid username"}),400
    
    username=request.form.get('username')
    frame=request.files['image'].read()
    return create_biometrics.upload_biometrics(username,frame)


if __name__=="__main__":
    app.run()