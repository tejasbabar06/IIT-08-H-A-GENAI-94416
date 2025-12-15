import streamlit as st

st.title("Hello, Streamlit")
st.header("Welcome to GenAi ")
st.write("Hello Guys!!!")

if st.button("Click me!!", type="primary"):
    st.toast("You clicked me...")