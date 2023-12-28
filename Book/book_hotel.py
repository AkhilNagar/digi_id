from DBConn import db_conn
import face_recognition
import cv2
import numpy as np
from flask import jsonify
from datetime import datetime,timedelta

def book_hotel(data):
    dbu=db_conn.Connect("users")
    dbh=db_conn.Connect("hotel")
    #t_date = datetime.today().date().strftime(""%d-%m-%Y"")
    user=dbu.find_one({"phone":data["digiid"]})
    start_date = datetime.strptime(data["checkindate"], "%d-%m-%Y")
    end_date = datetime.strptime(data["checkoutdate"], "%d-%m-%Y")
    days_difference = (end_date - start_date).days

    # Iterate over the range of dates
    try:
        for i in range(days_difference + 1):
            current_date = start_date + timedelta(days=i)
            booking={
                "fullname":user["first_name"]+" "+user["last_name"],
                "encoding":user["encoding"],
                "Check-in":data["checkindate"],
                "Check-out":data["checkoutdate"]
            }
            dbh[current_date.strftime("%d-%m-%Y")].insert_one(booking)
    except Exception as e:
        print(e)
        return False
    return True
    