#DRIVER CODE
import pymongo
global db
global conn
global ev
global username
global password
from decouple import config
import certifi

def driver():
    global username
    global password
    username=config("DB_USERNAME")
    password=config("DB_PASSWORD")
    flag=True
    print("\n Perform step 1 then step 2 first before proceeding")
    print("1) Connect to client number")
    print("2) Connect to an event inside the client")
    print("3) View event details and number of users for the event")
    print("4) Add registrations for event")
    print("5) View registrations for event")
    print("6) Add event")
    print("7) Start Event entries")
    print("8) Page Event")
    print("\n")

    while(flag):
        ch=int(input("Enter a choice "))
        if ch==1:
            connect()
        elif ch==2:
            connect_event()
        elif ch==3:
            view_event()
        elif ch==4:
            add_registrations()
        elif ch==5:
            view_registrations()
        elif ch==6:
            add_event()
        elif ch==7:
            start_event()
        elif ch==8:
            page_event()
        
        else:
            flag=False




def connect():
  global conn
  ch=int(input("Enter client number "))
  if ch==1:
    conn = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@client.du8czbz.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    #db=client.client
  elif ch==2:
    conn = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@client.nraxkyn.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    #db=client.client
  print("Connection Successful \n")

def connect_event():
  global db
  global ev
  ev=input("Enter event name to connect to ")
  db=conn[ev]

def view_event():
    #to store list of collections of db
    #collections=db.list_collection_names()
    # ch=input("Enter event name to connect to ")
    print("Event Details")
    #To iterate through documents
    obj=db.details.find_one({},{"name":1,"capacity":1})
    print("Event Name", obj["name"])
    print("Capacity", obj["capacity"])
    #To find count of documents.  option 2--->  .count_documents({})
    count= db.users.count_documents({})
    print("Count",count)
    

def view_registrations():
  for doc in db.users.find():
    print(doc["f_name"])

def add_registrations():

    #Convert csv file to pandas df
    import pandas as pd
    import io
    df = pd.read_csv("mockdata.csv")
    

    #Add users from dataset to users collection
    import random
    i=int(input("Enter number of registrations to be added"))
    n=0
    for j in range(0,i):
        # use the below to randomise the users being added
        #n=random.randint(0,len(df))
      f_name=df.loc[n,'first_name']
      l_name=df.loc[n,'last_name']
      digi_id= random.choice([True, False])
      phone=int(df.loc[n,'phone_number'])

      person_document={
          "f_name":f_name,
          "l_name":l_name,
          "digi_id":digi_id,
          "phone":phone
      }
      db["users"].insert_one(person_document)
      n+=1
    print("Added Successfully")

def add_event():
  name=input("Enter name of event ")
  date=input("Enter date of event ")
  time=input("Enter time of event in military code ")
  cap=input("Enter capacity of event ")
  db=conn[name]
  collection=db["details"]
  event_doc={
      "name":name,
      "date": date,
      "time":time,
      "capacity":int(cap)
  }
  collection.insert_one(event_doc)

def page_event():
    paging=config('paging')
    url=f"{paging}{ev}"
    print(url)
    data=list(db.users.find({},{"_id":0}))
    headers={"Content-type":"application/json"}
    import requests
    response=requests.post(url,json=data,headers=headers)
    if response.status_code!=200:
        print(response.status_code)
    else:
        print("Created")

driver()