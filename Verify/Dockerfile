FROM orgoro/dlib-opencv-python

COPY ../ /
RUN pip install -r requirements.txt
CMD ["sh", "-c", "cd /Verify && gunicorn --bind 0.0.0.0:5002 verify:app"]
#Client is the module and app is the name of the instance
# app = Flask(__name__)