from time import time
from flask import Flask, render_template, Response, request
import cv2
from decouple import config
# import face_recognition
import numpy as np
import requests
# import base64

global switch
switch =1 


app=Flask(__name__, template_folder = './templates')

#Define a video capture object
vid = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("haarcascade_frontalface_default.xml"))
flag = True


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

# def api_call(face):
#     apif = 0
#     print('method entered')
#     while True:
#         ret, frame = vid.read()
#         if face_extractor(frame) is not None:
#             if apif==0:
#                 apif=1
#                 face = cv2.resize(face_extractor(frame), (400,400))
#                 frameBytes = cv2.imencode('.jpg', face)[1]
#                 url = "http://127.0.0.1:8000/verify"
#                 headers = {"Content-type":"text/plain"}
#                 response = requests.post(url, headers = headers, data = frameBytes.tobytes())
#                 print(response.content)

#     # url="http://127.0.0.1:5000/verify"
#     # data={'id': '123', 'type': 'jpg', 'box': [0, 0, 100, 100], 'image': face}
#     # response=requests.post(url,data=data)

#     # return response.content

def gen_frames(): 
    apif = 0  
    while True:
        ret, frame = vid.read()  # read the camera frame
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)
        faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)

        for (x,y,w,h) in faces:
            x=x-10
            y=y-10
            cropped_face = frame[y:y+h+50, x:x+w+50]

        
        if face_extractor(frame) is not None:

            # face = cv2.resize(cropped_face, (400,400))
            if apif==0:
                print("entered")
                apif=1
                face = cv2.resize(face_extractor(frame), (400,400))
                frameBytes = cv2.imencode('.jpg', face)[1]
                api_url=config("verify")
                url=api_url+"/Pathaan"
                # url = "http://127.0.0.1:8000/verify/Pathaan"
                headers = {"Content-type":"text/plain"}
                response = requests.post(url, headers = headers, data = frameBytes.tobytes())
                print(response.content)
    
        ret, buffer = cv2.imencode('.jpg', frame)
        frame1 = buffer.tobytes()
        if apif==1:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')

@app.route('/')
def index():
    # return render_template('index.html')
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # return render_template('temp.html')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, vid
    if request.method == 'POST':

        if request.form.get('click') == 'Capture':
            ret, frame = vid.read()
            # api_call()     

        if request.form.get('stop') == 'Stop/Start':

            if(switch == 1):
                switch = 0
                vid.release()
                cv2.destroyAllWindows()

            else:
                vid = cv2.VideoCapture(0)
                switch = 1
            
        elif request.method == 'GET':
            return render_template('index.html')

        return render_template('index.html')

if __name__=='__main__':
    app.run()