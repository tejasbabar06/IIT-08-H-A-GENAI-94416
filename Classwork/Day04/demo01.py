import os
import requests
import json
import time
from dotenv import load_dotenv
import pandas as pd 
load_dotenv()
api_key = os.getenv("GROOK_API_KEY")


url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_promt = input("Ask Anything: ")
    if user_promt == "exit":
        break
    req_data={
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user","content":user_promt}
        ],
    }

    time1 =time.perf_counter()
    response = requests.post(url, json=req_data, headers=headers)
    time2 = time.perf_counter()
    print("Status:", response.status_code)
#   print(response.json())
    resp = response.json()
    print(resp["choices"][0]["message"]["content"])
    print(f"Time Required: {time2-time1:.2f} sec")