FROM orgoro/dlib-opencv-python
COPY ../ /
RUN pip install -r requirements.txt
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 user:app"]

#User is the module and app is the name of the instance
# app = Flask(__name__)