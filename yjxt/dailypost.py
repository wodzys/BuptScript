import requests
import time
import json

info = {}
USERNAME = ''
PASSWORD = ''

LOGIN_URL = 'https://app.bupt.edu.cn/uc/wap/login/check'
UPDATE_URL = 'https://app.bupt.edu.cn/ncov/wap/default/save'

session: requests.Session = requests.Session()


def login(username, password):
   session.post(LOGIN_URL, data={
       'username': username,
       'password': password
   })


def update():
    info["date"] = time.strftime("%Y%m%d", time.localtime())
    session.post(UPDATE_URL, data=info)


if __name__ == "__main__":
    login(USERNAME, PASSWORD)
    update()