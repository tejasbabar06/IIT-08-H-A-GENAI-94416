import streamlit as st
import time

st.title("💬 Simple Chat Bot")

# ✅ ALWAYS initialize session_state FIRST
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.5)  # delay for chat-like effect

if user_input:
    # User message
    st.session_state["messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Bot reply (echo)
    reply = f"You said: {user_input}"

    st.session_state["messages"].append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write_stream(stream_reply(reply))
