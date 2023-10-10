from flask import Flask,request

app = Flask(__name__)

@app.route('/verify',methods=['POST'])
def verify(eventname):
    return "Verified",201

if __name__=="__main__":
    app.run(port=5003)