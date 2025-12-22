import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GROOK_API_KEY")
st.title("Badshah's ChatBot...")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = api_key
)

user_input = st.chat_input("Ask your question...")
if user_input:
    result = llm.stream(user_input)
    st.write_stream([chunk.content for chunk in result])