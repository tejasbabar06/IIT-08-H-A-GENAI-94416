import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ------------------ FILE SETUP ------------------
USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

# Create files if not exist
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "username", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["userid", "filename", "upload_time"]).to_csv(HISTORY_FILE, index=False)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "userid" not in st.session_state:
    st.session_state.userid = None

# ------------------ SIDEBAR MENU ------------------
st.sidebar.title("Menu")

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Select", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Select", ["Explore CSV", "See History", "Logout"])

# ------------------ HOME ------------------
if menu == "Home":
    st.title("Welcome")
    st.write("Please Login or Register to continue")

# ------------------ REGISTER ------------------
elif menu == "Register":
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = pd.read_csv(USERS_FILE)

        if username in users["username"].values:
            st.error("User already exists")
        else:
            userid = len(users) + 1
            new_user = pd.DataFrame([[userid, username, password]],
                                    columns=["userid", "username", "password"])
            new_user.to_csv(USERS_FILE, mode="a", header=False, index=False)
            st.success("Registration Successful")

# ------------------ LOGIN ------------------
elif menu == "Login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USERS_FILE)

        user = users[(users["username"] == username) & (users["password"] == password)]

        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.userid = int(user.iloc[0]["userid"])
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------ EXPLORE CSV ------------------
elif menu == "Explore CSV":
    st.title("Upload & Explore CSV")

    file = st.file_uploader("Upload CSV File", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.write("CSV Data")
        st.dataframe(df)

        # Save upload history
        history = pd.DataFrame([[st.session_state.userid,
                                 file.name,
                                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                               columns=["userid", "filename", "upload_time"])

        history.to_csv(HISTORY_FILE, mode="a", header=False, index=False)
        st.success("Upload history saved")

# ------------------ SEE HISTORY ------------------
elif menu == "See History":
    st.title("Upload History")

    history = pd.read_csv(HISTORY_FILE)
    user_history = history[history["userid"] == st.session_state.userid]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

# ------------------ LOGOUT ------------------
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.userid = None
    st.success("Logged out successfully")
    st.rerun()
