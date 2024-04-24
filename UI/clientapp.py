import streamlit as st
import cv2
import face_recognition as fr
import requests

st.set_page_config(layout="wide")

st.sidebar.title("Settings")


#Tolerance
# tolerance = st.sidebar.slider("Tolerance", 0.0, 1.0, 0.5, 0.01)
# st.sidebar.info("Tolerance is the threshold for face recognition. The lower the tolerance, the more strict the face recognition. The higher the tolerance, the more loose the face recognition.")

CLIENT_API_URL = 'http://localhost:5001/'
VERIFY_API_URL = 'http://localhost:5002/'

#Information section
# st.sidebar.title("Student Information")
# name_container = st.sidebar.empty()
# name_container.info('Name: Unknown')

def client_login():
    data = {'username': "ITC-Mumbai", 'password': "ITC-Mumbai"}
    response = requests.post(f'{CLIENT_API_URL}/login', json=data)
    return response

def verify_picture():
    st.title("Face Recognition App")
    st.write("Please upload an image for verification")

    if "access_token" not in st.session_state:
        st.warning("Please login to access KYC.")
        return
    
    uploaded_images = st.file_uploader("Upload", accept_multiple_files=False)
    print(type(uploaded_images))
    # print(len(uploaded_images))
    if st.button("Submit image"):
        files = {'image': uploaded_images}
        headers = {"Authorization": f"{st.session_state.access_token}"}
        print("Reaching here 1")
        response = requests.post(f'{VERIFY_API_URL}', files=files, headers=headers)
        print("Reaching here 2")
        if response.status_code == 200:
            st.success("verified")
            st.write(response.json())
        else:
            st.error("verify API failed. Please try again.")
        # print("Loop")
        #Read uploaded image with face_recognition
        # for image in uploaded_images:
            
            # image, name, id = recognize(image,TOLERANCE) 
            # name_container.info(f"Name: {name}")
            # id_container.success(f"ID: {id}")
            # st.image(image)

    # files = {"image": uploaded_file}
    # headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    # response = requests.post(f"{API_URL}/kyc", data=data, files=files, headers=headers)
    # if response.status_code == 200:
    #     st.success("KYC submitted successfully!")
    #     st.write(response.json())
    # else:
    #     st.error("KYC submission failed. Please try again.")

def detect_faces(frame, message):
    # Load the pre-trained Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, message, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

def verify_face(image):    
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = buffer.tobytes()

    files = {'image': image_bytes}
    headers = {"Authorization": f"{st.session_state.access_token}"}
    print("Reaching here 1")
    response = requests.post(f'{VERIFY_API_URL}', files=files, headers=headers)
    print("Reaching here 2")
    if response.status_code == 200:
        # st.success("verified")
        # st.write(response.json())
        verified = True
        return response.json(), verified
    else:
        verified = False
        return {"message": "Face verification failed"}, verified

def verify_webcam():
    if "access_token" not in st.session_state:
        st.warning("Please login to access verify.")
        return
    
    st.title("Face Recognition App")
    st.write("This app recognizes faces in a live video stream. To use it, simply press start and allow access to your webcam.")

    #Camera Settings
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])
    
    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            st.info("Please turn off the other app that is using the camera and restart app")
            st.stop()

        result, verified = verify_face(frame)

        if verified:
            st.success("Face verified")
            st.write(result)
            message = result["message"]
        else:            
            st.error(result["message"])
            message = result["message"]

        # Process the frame to detect faces
        frame_with_faces = detect_faces(frame, message)

        # Convert BGR to RGB for displaying in Streamlit
        frame_with_faces_rgb = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)

        # Display the processed frame
        FRAME_WINDOW.image(frame_with_faces_rgb)

        
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # FRAME_WINDOW.image(frame)

        #convert frame to bytes
        # _, buffer = cv2.imencode('.jpg', frame)
        # image_bytes = buffer.tobytes()

        # files = {'image': image_bytes}
        # headers = {"Authorization": f"{st.session_state.access_token}"}
        # print("Reaching here 1")
        # response = requests.post(f'{VERIFY_API_URL}', files=files, headers=headers)
        # print("Reaching here 2")
        # if response.status_code == 200:
        #     st.success("verified")
        #     st.write(response.json())
        # else:
        #     st.error("verify API failed. Please try again.")
        # image, name, id = recognize(frame,TOLERANCE)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #Display name and ID of the person
        
        # name_container.info(f"Name: {name}")
        # id_container.success(f"ID: {id}")
        # FRAME_WINDOW.image(image)

    # st.title("Face Recognition App")

def main():
    st.title("Client")
    st.sidebar.title("Navigation")

    if "login_done" not in st.session_state:
        response = client_login()
        if response.status_code == 200:
            st.session_state.access_token = response.json().get("access_token")
            st.session_state.login_done = True
            st.success("Login successful!")
            st.write("You are logged in.")
    if "login_done" in st.session_state:
        menu = ["Picture", "Webcam"]
        choice = st.sidebar.selectbox("Input type", menu)
            
        if choice == "Picture":
            verify_picture()
        elif choice == "Webcam":
            verify_webcam()
        else:
            st.error("Login failed. Please check your credentials.")

    # login_button = st.sidebar.button("Login")

    # if "access_token" not in st.session_state:
    # response = client_login()
    
    # if response.status_code == 200:
    #     st.session_state.access_token = response.headers.get("access_token")
    #     st.success("Login successful!")
    #     st.write("You are logged in.")
    #     menu = ["Picture", "Webcam"]
    #     choice = st.sidebar.selectbox("Input type", menu)
            
    #     if choice == "Picture":
    #         verify_picture()
    #     elif choice == "Webcam":
    #         verify_webcam()
    #     else:
    #         st.error("Login failed. Please check your credentials.")
    
    # if login_button:

if __name__ == "__main__":
    main()