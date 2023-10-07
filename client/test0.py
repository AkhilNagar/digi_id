import requests
from decouple import config
import cv2

def trial():
    api_url=config("verify")
    url=api_url+"/event1"
    print(url)
    img = cv2.imread('img.jpg')
    frameBytes = cv2.imencode('.jpg',img)[1]
    headers = {"Content-type":"text/plain"}
    response = requests.post(url, headers = headers, data = frameBytes.tobytes())
    print(response.content)

trial()

