import requests

url = 'http://localhost:3000/get_user'
myobj = {'phone_num': '2268993629'}

x = requests.post(url, data = myobj)

print(x.json()["user"])