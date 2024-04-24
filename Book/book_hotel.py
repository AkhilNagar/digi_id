from DBConn import db_conn
import face_recognition
import cv2
import numpy as np
from flask import jsonify
from datetime import datetime,timedelta

def book_hotel(data):
    dbu=db_conn.Connect("users")
    dbh=db_conn.Connect(str(data["clientcode"]))
    #t_date = datetime.today().date().strftime("%d-%m-%Y")
    try:
        user=dbu.find_one({"phone":data["digiid"]})
        existing_user = dbu.find_one({"fullname": user["first_name"] + " " + user["last_name"]})
        
        if existing_user:
            # If the document exists, create the new booking document
            booking = {
                "fullname": user["first_name"] + " " + user["last_name"],
                "Check-in": datetime.strptime(data["checkindate"], "%d-%m-%Y"),
                "Check-out": datetime.strptime(data["checkoutdate"], "%d-%m-%Y"),
                "encoding": user["encoding"]
            }

            # Replace the existing booking document with the new one
            dbh[str(data["eventcode"])].replace_one(
                {"fullname": user["first_name"] + " " + user["last_name"]},
                booking,
                upsert=True  # If no matching document is found, insert the new one
            )
    except Exception as e:
        print(e)
        return False
    return True
    