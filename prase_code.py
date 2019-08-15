# 抓取猫眼电影TOP100榜
import csv
import json
import re
from multiprocessing import Pool

import pymysql
import pymysql.cursors
import requests
from requests.exceptions import RequestException


def get_one_page(url):
    '''获取单页源码'''
    try:
        headers = {
            "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,"
                          "likeGecko)Chrome/68.0.3440.106Safari/537.36 "
        }
        res = requests.get(url, headers=headers)
        # 判断响应是否成功,若成功打印响应内容,否则返回None
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''解析单页源码'''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime'
                         + '.*?>(.*?)</p>.*?score.*?integer">(.*?)</i>.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # 采用遍历的方式提取信息
    for item in items:
        yield {
            'rank': item[0],
            'title': item[1],
            'actor': item[2].strip()[3:] if len(item[2]) > 3 else '',  # 判断是否大于3个字符
            'time': item[3].strip()[5:] if len(item[3]) > 5 else '',
            'score': item[4] + item[5]
        }


def write_to_textfile(content):
    '''写入text文件'''
    with open("MovieResult.text", 'a', encoding='utf-8') as f:
        # 利用json.dumps()方法将字典序列化,并将ensure_ascii参数设置为False,保证结果是中文而不是Unicode码.
        f.write(json.dumps(content, ensure_ascii=False) + "\n")
        f.close()


def write_to_csvField(fieldnames):
    '''写入csv文件字段'''
    with open("MovieResult.csv", 'a', encoding='utf-8', newline='') as f:
        # 将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 调用writeheader方法写入字段名
        writer.writeheader()


def write_to_csvRows(content, fieldnames):
    """写入csv文件内容"""
    with open("MovieResult.csv", 'a', encoding='utf-8', newline='') as f:
        # 将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 调用writeheader方法写入字段名
        # writer.writeheader()            ###这里写入字段的话会造成在抓取多个时重复.
        writer.writerows(content)
        f.close()


def main(offset):
    fieldnames = ["rank", "title", "actor", "time", "score"]
    url = "http://maoyan.com/board/4?offset={0}".format(offset)
    html = get_one_page(url)
    rows = []
    for item in parse_one_page(html):
        # write_to_textfile(item)
        rows.append(item)

    save_data(rows)


def save_data(list):
    ls = []
    for dist_v in list:
        ls.append(tuple(dist_v.values()))
    # Connect to the database

    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='123456',
                                 db='erp',
                                 charset='utf8mb4',
                                 port=3308,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `maoyan` (`rank`, `title`, `actor`, `time`, `score`) VALUES (%s, %s, %s, %s, %s)"
            for v in ls:
                cursor.execute(sql, v)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        print('success')
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `rank`, `title`, `actor`, `time`, `score` FROM `maoyan` WHERE `title`=%s"
        #     cursor.execute(sql, (v[1],))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()


if __name__ == '__main__':
    # 将字段名传入列表
    #fieldnames = ["rank", "title", "actor", "time", "score"]
    #write_to_csvField(fieldnames)
    # #通过遍历写入TOP100信息
    # for i in range(10):
    #     main(offset=i * 10,fieldnames=fieldnames)
    #     time.sleep(1)
    pool = Pool()
    # map方法会把每个元素当做函数的参数,创建一个个进程,在进程池中运行.
    pool.map(main, [i * 10 for i in range(10)])

