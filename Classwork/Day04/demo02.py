import requests
import time
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
api_key = "dummy_keyh"
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_prompt = input("Ask anything: ")
    if user_prompt == "exit":
        break

    req_data = {
        "model": "google/gemma-3n-e4b",
        "messages":[
            {"role":"user","content":user_prompt}
        ],
    }

    t1 = time.perf_counter()
    response = requests.post(url, json=req_data, headers=headers)
    t2 = time.perf_counter()

    print("Status:", response.status_code)

    resp = response.json()
    #print(resp)
    print(resp["choices"][0]["message"]["content"])


    print(f"Time required: {t2 - t1:.2f} sec\n")
