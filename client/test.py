import requests
from decouple import config
import cv2
import glob
import time
import matplotlib.pyplot as plt



api_url=config("verify")
url=api_url+"/Pathaan"
print(url)

path = glob.glob("fdb/*.jpg")
count=0
x=[]
y=[]

for img in path:
    if count<25:  #Change count
        x.append(count)
        n = cv2.imread(img)
        count = count + 1
        frameBytes = cv2.imencode('.jpg',n)[1]
        headers = {"Content-type":"text/plain"}
        startTime = time.time()
        response = requests.post(url, headers = headers, data = frameBytes.tobytes())
        # print(response.content)
        executionTime =(time.time() - startTime)*1000
        y.append(executionTime)
        # print(count)
        # print(str(executionTime))

plt.plot(x,y)
plt.xlabel('Number of images')
plt.ylabel('Time in ms')
plt.savefig('myplot.png')

