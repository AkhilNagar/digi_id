FROM orgoro/dlib-opencv-python
COPY ../ /
RUN pip install -r requirements.txt
CMD ["sh", "-c", "cd /User && flask --app user --debug run -h 127.0.0.1 -p 5000"]

#User is the module and app is the name of the instance
# app = Flask(__name__)