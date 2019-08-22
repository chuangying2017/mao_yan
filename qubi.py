import csv
import requests
from multiprocessing import Pool, Process, ProcessError
from pyquery import PyQuery


url = 'https://www.xbiquge6.com/'
header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/76.0.3809.100 Safari/537.36",
          'Host': 'www.xbiquge6.com'}
local_url = 'http://192.168.1.7:8093/'
proxies = {
    "http": "http://113.116.58.38:9000",
    "https": "https://163.204.243.39:9999",
}


def index():
    pass


def get_proxies()-> dict:
    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"
    # 代理隧道验证信息
    proxyUser = "H8QV0261XG021Z1P"
    proxyPass = "3A301BD36D687FA0"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxy_handler = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    return proxy_handler


def request_post(tup):
    global url, header, local_url, proxies
    # res = requests.get(url, headers=header)
    prefix = tup[0]
    suffix_mode = tup[1]

    split = '_'
    request_param = str(prefix) + split + str(suffix_mode)
    url += request_param
    res = requests.get(url, headers=header)
    if res.status_code in (200, 201):
        jq = PyQuery(res.content)
        type_class_name = jq('div.box_con div.con_top a').eq(1).text()
        result_type = requests.post(local_url + 'polls/get_fiction/', data={'title': type_class_name}, proxies=proxies)
        json_data = result_type.json()
        maininfo = jq('#maininfo')
        info = maininfo.find('#info')
        title = info.find('h1').text()
        all_tup = ()
        all_p = info.find('p')
        for p in all_p.items():
            all_tup += (p.text().split('：')[1], )
        author, status_data, latest_update_time, latest_chapter = all_tup
        desc: str = info.siblings('div').find('p').eq(0).html()
        class_id = json_data['id']
        print(desc)




    elif res.status_code > 400:
        print('页面没找到')


def param(start_val, end_val=0) -> str:
    suffix_max_num = 999999
    prefix_min_num = 100
    num_val: int = 0
    for i in range(start_val, prefix_min_num):
        for j in range(end_val, suffix_max_num):
            num_val += 1
    print(num_val)



def parse_html():
    pass


if __name__ == '__main__':
    # param(90, 990000)
    # pool = Pool(processes=3)
    request_post((0, 1))
    exit()
    ls: list = []
    suffix = 99
    min_num = 999999
    v = 10
    while suffix > 9:
        suffix = suffix - v
        ls.append((suffix, min_num))
        if suffix <= 9:
            ls.append((0, min_num))
    print(ls)
