import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("login"):
        if username == password and username != "":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Login")

else:
    st.title("Weather Information")

    city = st.text_input("Enter City")

    if st.button("Get Weather"):
        if city != "":
            api_key = os.getenv("API_KEY")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                st.write("City", data["name"])
                st.write("Temprature", data["main"]["temp"] , "C")
                st.write("Weather", data["weather"][0]["description"])
                st.write("Humidity", data["main"]["humidity"], "%")
            else:
                st.error("City Not found")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("Thanks For using app")
        st.rerun()