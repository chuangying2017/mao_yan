from multiprocessing import Pool
import random
import requests
import time
from pyquery import PyQuery
import os


url = 'https://www.xbiquge6.com/'
header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/76.0.3809.100 Safari/537.36",
          'Host': 'www.xbiquge6.com'}
local_url = 'http://192.168.1.9:8093/'
proxies = {
    "http": "http://113.116.58.38:9000",
    "https": "https://163.204.243.39:9999",
}


def index():
    pass


def get_proxies() -> dict:
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
    print("start time " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    res = requests.get(url, headers=header, timeout=5)
    if res.status_code in (200, 201):
        print('页面正在解析.....')
        jq = PyQuery(res.content)
        type_class_name = jq('div.box_con div.con_top a').eq(1).text()
        result_type = requests.post(local_url + 'polls/get_fiction/', data={'title': type_class_name})
        json_data = result_type.json()
        maininfo = jq('#maininfo')
        info = maininfo.find('#info')
        title = info.find('h1').text()
        all_tup = ()
        all_p = info.find('p')
        for p in all_p.items():
            all_tup += (p.text().split('：')[1],)
        author, status_data, last_update_time, latest_chapter = all_tup
        desc: str = info.siblings('div').find('p').eq(0).html()
        class_id = json_data['id']  # 将数据插入小说表
        fiction_json = requests.post(local_url + 'polls/post_fiction_create/', data={
            'author': author, 'status': status_data, 'last_update_time': last_update_time,
            'latest_chapter': latest_chapter, 'desc': desc, 'class_id': class_id, 'title': title
        }, timeout=3)
        fiction_json = fiction_json.json()
        fiction_id = fiction_json['id']
        box_con = jq('#list dl').find('dd')
        for k, vs in enumerate(box_con.items()):
            a = vs('a')
            request_url = url + '/' + a.attr('href').split('/')[-1]
            request_result = requests.get(request_url, headers=header, timeout=5)
            title_ = a.text()

            if request_result.status_code == 200:
                content = PyQuery(request_result.content)
                content_data = content('#content').html()
                data_fiction_chapter: dict = {
                    'fiction_id': fiction_id,
                    'title': title_,
                    'content': content_data
                }
                requests.post(local_url + 'polls/post_fiction_chapter/',
                              data=data_fiction_chapter, timeout=3)

            time.sleep(random.uniform(0.3, 2.1))

        print('正在写作中.....')
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


def func_forward(tup: tuple = ()):

    filename = str(tup[0]) + '.txt'
    back_tup = tup
    if os.path.exists(filename):
        open_file = open(filename, 'r+')
        read_line = open_file.readline()
        tup = tuple(eval(read_line))
        if tup.__len__() < 1:
            tup = back_tup
    else:
        open_file = open(filename, 'w')

    origin_vs = tup[0]
    vs = 10 + origin_vs

    for i in range(origin_vs, vs):
        for j in range(tup[1]):
            tup1 = (i, j + 1)
            print(tup1)
            request_post(tup1)
            open_file.write(','.join('%s' %id for id in tup1))
            open_file.close()
            open_file = open(filename, 'r+')
            time.sleep(random.uniform(0.5, 1.8))
    open_file.close()


if __name__ == '__main__':
    func_forward((0, 9))
    exit()
    ls: list = []
    suffix = 99
    min_num = 99999
    v = 10
    while suffix > 9:
        suffix = suffix - v
        ls.append((suffix, min_num))
        if suffix <= 9:
            ls.append((0, min_num))
    ls.sort()
    pool = Pool(processes=10)
    pool.map_async(func_forward, ls)
    pool.close()
    pool.join()
