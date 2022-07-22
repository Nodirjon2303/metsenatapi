import requests
from jwt_client import jwt_client


def write_tokens(data):
    f = open('jwt_client.py', 'w')
    f.write(f"jwt_client = {data}")
    f.close()
def renew_token():
    username = input('username')
    password = input('password')
    r = requests.post("http://localhost:8000/api/token/", data={'username': username, 'password': password})
    if r.status_code == 200:
        jwt_client = r.json()
        write_tokens(jwt_client)
    else:
        print(r.json())
    print(r.status_code)
    

access_token = jwt_client.get('access')
if access_token:
    headers = {'Authorization': f'Bearer {access_token}'}
    r = requests.get("http://localhost:8000/api/university/", headers=headers)
    print("university ", r.status_code, r.json())
    if r.status_code != 200:
        data = {
            'refresh': jwt_client.get('refresh')
        }
        r = requests.post("http://localhost:8000/api/token/refresh/", json=data)
        if r.status_code == 200:
            write_tokens(r.json())
        else:
            renew_token()
        print(r.status_code, r.json())


else:
    while True:
        username = input('username')
        password = input('password')
        r = requests.post("http://localhost:8000/api/token/", data={'username': username, 'password': password})
        if r.status_code == 200:
            jwt_client = r.json()
            write_tokens(jwt_client)
            break
        else:
            print(r.json())
print(jwt_client)
