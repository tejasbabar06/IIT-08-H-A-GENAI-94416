import pandas as pd
from pandasql import sqldf
import requests
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

csv_df = None
chat_history = []

@tool
def csv_tool(question: str) -> str:
    global csv_df
    if csv_df is None:
        return "csv file not loaded"
    if "count" in question.lower():
        query = "select count(*) from data"
    elif "average" in question.lower():
        cols = csv_df.select_dtypes(include="number").columns
        if len(cols) == 0:
            return "no numeric column available"
        query = f"select avg({cols[0]}) from data"
    else:
        query = "select * from data limit 5"
    try:
        result = sqldf(query, {"data": csv_df})
        return str(result)
    except Exception as e:
        return str(e)

@tool
def sunbeam_tool(question: str) -> str:
    r = requests.get("https://sunbeaminfo.in")
    if r.status_code != 200:
        return "unable to access website"
    content = r.text.lower()
    if "internship" in question.lower():
        return "sunbeam offers practical internships with placement oriented training"
    if "batch" in question.lower():
        return "sunbeam conducts regular batches like dac dai dbda and other courses"
    return "relevant information not found"

llm = ChatOpenAI(temperature=0)

agent = initialize_agent(
    tools=[csv_tool, sunbeam_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def load_csv(path):
    global csv_df
    csv_df = pd.read_csv(path)
    return csv_df.head()

def ask_agent(question):
    chat_history.append({"role": "user", "content": question})
    reply = agent.run(question)
    chat_history.append({"role": "assistant", "content": reply})
    return reply

