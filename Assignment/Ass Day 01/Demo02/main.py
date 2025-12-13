import requests

try:
    url="https://nilesh-g.github.io/learn-web/data/novels.json"
    response = requests.get(url)
    print("status code : ",response.status_code)
    data = response.json()
    print("resp data : ", data)

except:
    print("Some error occured ")