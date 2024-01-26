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
    user=dbu.find_one({"phone":data["digiid"]})
    try:
        booking={
            "fullname":user["first_name"]+" "+user["last_name"],
            "Check-in":datetime.strptime(data["checkindate"], "%d-%m-%Y"),
            "Check-out":datetime.strptime(data["checkoutdate"], "%d-%m-%Y"),
            "encoding":user["encoding"]
            }
        dbh[str(data["eventcode"])].insert_one(booking)
    except Exception as e:
        print(e)
        return False
    return True
    