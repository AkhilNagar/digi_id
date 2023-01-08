from crypt import methods
from flask import Flask,request,jsonify
from decouple import config
import pymongo
import json
import certifi
#import uuid
import os



app = Flask(__name__)


@app.route('/', methods=["POST","GET"])
def index():
    text={"title":"WELCOME"}
    return jsonify(text)

@app.route('/page/<string:eventname>', methods=['GET','POST'])
def paging(eventname):
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    db = client.users
    collection =db.userdata
    db1=client[eventname]
    #collname=uuid.uuid4().hex
    coll=db1[eventname]
    #response=[]
    if(request.method=="POST"):
        print("POSTYY")
        user=request.json
        print ("USER",type(user))
        for obj in user:
            phone=obj["phone"]
            # print(phone)
            # print(type(phone))
            result=collection.find_one({"phone_number":phone},{"_id":0, "encodings":1})
            # print(result)
            if result != None:
                coll.insert_one(result)
        return eventname
        #Look for each element in host collection
        #Create new collection for event in host-->refs of 

@app.route('/verify/<string:eventname>',methods=['POST'])
def verify(eventname):
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@host.ejnsy4a.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    t_encoding=request.json
    db=client[eventname]
    collection=db[eventname]
    encs=collection.find({},{"encodings":1})
    for obj in encs:
        f_encoding=obj["encodings"]
        
        print(f_encoding)
        #Compare face encodings
        #if true return true else false
    
    return "True"



if __name__=="__main__":
    app.run(debug=True)

'''
route 1
client calls post request on api and passes json list of all users in the body
host receives list of all users for that event
performs query operations on the mongo db
a new temporary table is created with only registered users at host site
'''

'''
route 2
client calls api for a person
quick checking from table generated
returns true or false
'''