import requests
import json 
try:
    data=requests.get("https://jsonplaceholder.typicode.com/todos")
    x=data
    edata=x.json()
    li=[i for i in edata if i['completed']==True]
    for i in li:
        print(i)
except:
    print("error")