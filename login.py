from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, ProxyHandler
from urllib.error import URLError
import requests


url = 'http://awpo.com.cn/login'


def index(username, password):
    global url
    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, password)
    auth_handler = HTTPBasicAuthHandler(p)
    opener = build_opener(auth_handler)
    try:
        result = opener.open(url)
        html = result.read().decode('utf-8')
        print(html)
    except URLError as e:
        print(e.reason)


def auth_post():
    data = {'name': 'administrator', 'password': '123456', '_token': 'IjsYZFxG9mP9GnU3SBR5tNQh3Qg9ftcG0Qf3efsB'}
    global url
    res = requests.post(url, data=data)
    json_data = res.json()
    print(res.cookies)
    print(res.headers)
    print(res.status_code)


if __name__ == '__main__':
    auth_post()
