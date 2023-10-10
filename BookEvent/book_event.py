from flask import Flask,request

app = Flask(__name__)

# POST request /fetch 
# Body: Unique digi-id token
# Response: User Found, User not found

# POST request /book
# Body: Client name, Event name, Unique digi-id token
# Response: Booking Successful, Unsuccessful

if __name__=="__main__":
    app.run(port=5003)