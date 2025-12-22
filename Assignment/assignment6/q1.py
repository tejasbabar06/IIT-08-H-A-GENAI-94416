import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv("GROOK_API_KEY")

st.title("Lm Studio & Grook AI Chat BOT")
user_input = st.chat_input("Ask Your Question...")
if "chat_history" not in st.session_state:
      st.session_state.chat_history = []
if "input_history" not in st.session_state:
      st.session_state.input_history = []
with st.sidebar:
  st.sidebar.header("Model Selection")
  model_choice = st.sidebar.radio(
  "Choose LLM:",
  ["Groq (Cloud)", "LM Studio (Local)"]
  ) 

  st.divider()
  
  st.write("Chat History")
  
  st.session_state.input_history.append(user_input)
  for item in st.session_state.input_history:
    if isinstance(item, str):
        st.write(item)



def groq_response(prompt):
    conversation=[]
    conversation.append(prompt)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    req_data = {
        "model": "llama-3.3-70b-versatile",
         "messages": st.session_state.chat_history
    }
    
    response = requests.post(url, data=json.dumps(req_data),headers=headers)
    return response.json()["choices"][0]["message"]["content"]



def lmstudio_response(prompt):
    conversation=[]
    conversation.append(prompt)
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        }

    req_data = {
        "model": "google/gemma-3n-e4b",
        "messages": st.session_state.chat_history
    }

    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    return response.json()["choices"][0]["message"]["content"]

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if model_choice == "Groq (Cloud)":
            reply = groq_response(user_input)

        else:
            reply = lmstudio_response(user_input)

        print(reply)
        st.markdown(reply)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    