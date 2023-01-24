from time import time
from flask import Flask, render_template, Response
import cv2
import numpy as np
import requests
from decouple import config

app=Flask(__name__)

#Video capture object
vid = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("haarcascade_frontalface_default.xml"))
flag = True
api_url=config("verify")

def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns the input image
   
    frame_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
   
    if faces == ():
        return None
   
    # Crop all faces found
    for (x,y,w,h) in faces:
        x=x-10
        y=y-10
        cropped_face = img[y:y+h+50, x:x+w+50]

    return cropped_face


def gen_frames(): 
    apif = 0  
    while True:
        ret, frame = vid.read()

        if face_extractor(frame) is not None:

            # face = cv2.resize(cropped_face, (400,400))
            if apif==0:
                apif=1
                face = cv2.resize(face_extractor(frame), (400,400))
                frameBytes = cv2.imencode('.jpg', face)[1]
                url = api_url
                headers = {"Content-type":"text/plain"}
                response = requests.post(url, headers = headers, data = frameBytes.tobytes())
                print(response.content)
    
        ret, buffer = cv2.imencode('.jpg', frame)
        frame1 = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')
        
    

@app.route('/')
def index():
    # return render_template('index.html')
    return "Welcome!"

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run()