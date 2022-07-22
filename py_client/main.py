import requests
from faker import Faker
from random import randint, choice
from faker.providers import company

username = input('username')
password = input('password')
r = requests.post("https://senat.metsenat1.uz/api/token/", data={'username': username, 'password': password})
if r.status_code == 200:
    access = r.json()['access']
    fake = Faker()
    fakecompany = Faker()
    fakecompany.add_provider(company)

    headers = {"Authorization": f"Bearer {access}"}

    for i in range(105):
        homiy = randint(2, 175)
        data = {
            "amount": randint(1, 3) * 10 ** 5,
            "homiy": homiy,
            "student": randint(1, 151)
        }
        r = requests.post("https://senat.metsenat1.uz/api/homiy/", headers=headers, json=data)
        print(r.json())
