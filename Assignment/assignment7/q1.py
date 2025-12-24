import streamlit as st
import pandas as pd
import pandasql as ps
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

st.title("Find Your Data From CSV File")

data_file = st.file_uploader("Upload a CSV file", type=["csv"])

df = None
if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)

user_input = st.chat_input("Enter your question...")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

if df is not None and user_input:

    llm_input = f"""
Table Name: data
Table Schema:
{df.dtypes}

Question:
{user_input}

Instructions:
- Write a SQL query
- Return ONLY query
- No explanation
- If not possible return Error
"""
    result = llm.invoke(llm_input)
    query = result.content.strip()

    st.subheader("Generated SQL")
    st.code(query, language="sql")

    try:
        query_result = ps.sqldf(query, {"data": df})
        st.subheader("Query Result")
        st.dataframe(query_result)

    
        llm_input2 = f"""
Query Result:
{query_result.head()}

Instructions:
- Explain the result in one simple line
"""
        result2 = llm.invoke(llm_input2)
        st.subheader("Explanation")
        st.write(result2.content)

    except Exception as e:
        st.error("Invalid SQL generated")
        st.write(str(e))

elif user_input and df is None:
    st.warning("Please upload a CSV file first")
