import streamlit as st
import requests

# Constants
API_URL = 'http://localhost:5000/'
BOOK='http://localhost:5001/'

# Function to make API requests with JWT token in headers
def make_api_request(url, headers=None):
    if headers is None:
        headers = {}
    access_token = st.session_state.access_token
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(url, headers=headers)
    return response

# Register Section
def register_user():
    st.header("Register")
    # Streamlit input fields for registration
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    # Register button
    if st.button("Register"):
        if not username or not password:
            st.error('Username and password are required.')
        else:
            data = {'username': username, 'password': password}
            response = requests.post(f'{API_URL}/register', json=data)
            if response.status_code == 201:
                st.success('Registration successful!')
                st.json(response.json())
            elif response.status_code == 400:
                st.error('Registration failed. Username already exists.')
            else:
                st.error('Registration failed. Please try again.')

# Login Section
def login_user():
    st.header("Login")
    # Streamlit input fields for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    # Login button
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.access_token = response.headers.get("access_token")
            st.success("Login successful!")
            st.write("You are logged in.")
        else:
            st.error("Login failed. Please check your credentials.")

# KYC Upload Section
def kyc_upload():
    st.header("KYC Upload")
    # Check if logged in before displaying KYC Upload section
    if "access_token" not in st.session_state:
        st.warning("Please login to access KYC.")
        return
    
    # Streamlit form for KYC
    st.write("Fill in the KYC details:")
    username = st.text_input("Username")
    lastname = st.text_input("Last Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    uploaded_file = st.file_uploader("Upload Image File (JPG, PNG)")
    if st.button("Submit KYC"):
        if not (username and lastname and phone and email and uploaded_file):
            st.error("All fields and image are required for KYC.")
        else:
            data = {
                "username": username,
                "lastname": lastname,
                "phone": phone,
                "email": email
            }
            files = {"image": uploaded_file}
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.post(f"{API_URL}/kyc", data=data, files=files, headers=headers)
            if response.status_code == 200:
                st.success("KYC submitted successfully!")
                st.write(response.json())
            else:
                st.error("KYC submission failed. Please try again.")
def book_hotel():
    if "access_token" not in st.session_state:
        st.warning("Please login to access KYC.")
        return
    st.write("Please enter details:")
    checkin = st.text_input("Check-In")
    checkout = st.text_input("Check-Out")
    clientcode=9617
    eventcode=4499
    if st.button("Book Hotel"):
        if not (checkin and checkout):
            st.error("All fields and image are required for KYC.")
        else:
            data = {
                "clientcode": clientcode,
                "eventcode": eventcode,
                "checkindate": checkin,
                "checkoutdate": checkout
            }
            headers = {"Authorization": f"Bearer {st.session_state.access_token}","Content-Type": "application/json"}
            response = requests.post(f"{BOOK}/bookhotel", json=data, headers=headers)
            if response.status_code == 200:
                st.success("Hotel Booked successfully!")
                st.write(response.json())
            else:
                st.error("Hotel Booking failed. Please try again.")

# Main Streamlit App
def main():
    st.title("User Authentication and KYC Upload")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Register", "Login", "KYC Upload", "Book Hotel"])

    if page == "Register":
        register_user()
    elif page == "Login":
        login_user()
    elif page == "KYC Upload":
        kyc_upload()
    elif page == "Book Hotel":
        book_hotel()
if __name__ == "__main__":
    main()
