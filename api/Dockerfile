FROM orgoro/dlib-opencv-python
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:8000 app:app