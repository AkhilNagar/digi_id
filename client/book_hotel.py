import db_conn
import face_recognition
import cv2
import numpy as np
from flask import jsonify
from datetime import datetime,timedelta

def book_hotel(data):
    try:
        dbu=db_conn.Connect("users")
        dbh=db_conn.Connect(str(data["clientcode"]))
        #t_date = datetime.today().date().strftime("%d-%m-%Y")
        user=dbu.find_one({"phone":data["digiid"]})
        existing_user = dbh[str(data["eventcode"])].find_one({"fullname": user["first_name"] + " " + user["last_name"]})
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
                upsert=True
            )
        else:
            booking = {
                "fullname": user["first_name"] + " " + user["last_name"],
                "Check-in": datetime.strptime(data["checkindate"], "%d-%m-%Y"),
                "Check-out": datetime.strptime(data["checkoutdate"], "%d-%m-%Y"),
                "encoding": user["encoding"]
            }
            dbh[str(data["eventcode"])].insert_one(booking)
    except Exception as e:
        print(e)
        return False
    return True

    