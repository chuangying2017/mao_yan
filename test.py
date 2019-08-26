# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# # browser = webdriver.PhantomJS()
# #
# # browser.get('https://www.baidu.com')
# #
# # print(browser.current_url)
#
#
# chrome_options = Options()
#
# chrome_options.add_argument('--headless')
#
# chrome_options.add_argument('--disable-gpu')
#
# driver = webdriver.Chrome(chrome_options=chrome_options)
#
# driver.get("https://www.qidian.com/")
#
# res = driver.find_element('class', 'rank-wrap box-center mb20')
#
# print(res)
import os
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException
import json
from pyquery import PyQuery
import time
from multiprocessing import Pool
import random
import platform



url = 'https://www.xbiquge6.com/'
headers = {
    'Host': 'www.xbiquge6.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def fetch_fiction(tup: tuple = (0, 2)):
    global url, headers
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    page_code = str(tup[0]) + '_' + str(tup[1])
    new_url = url + page_code + '/'
    try:
        browser.get(new_url)
        id_list = browser.find_element_by_id('list')
        maininfo = browser.find_element_by_id('maininfo')
        box_con = browser.find_elements(By.CSS_SELECTOR, '.box_con .con_top a')[1]
        maininfo_p = maininfo.find_elements(By.TAG_NAME, 'p')
        top_for = maininfo_p[:-2]
        fiction = {
            'class_name': box_con.text,  # 文章分类
            'title': maininfo.find_element_by_tag_name('h1').text,  # 小说标题
            'desc': maininfo_p[-2].text
        }
        ls_fiction_info = []
        for p in top_for:
            ls_fiction_info.append(p.text.split('：')[1])
        fiction['author'] = ls_fiction_info[0]
        fiction['status'] = ls_fiction_info[1]
        fiction['last_update_time'] = ls_fiction_info[2]
        fiction['latest_chapter'] = ls_fiction_info[3]
        dt: list = []
        dd = id_list.find_elements(By.TAG_NAME, 'dd')
        content_script = "return document.getElementById('content').innerHTML"

        storage_ls: list = []

        for l in dd:
            storage_ls.append((l.find_element(By.TAG_NAME, 'a').get_attribute('href'), l.text))
        print('准备制作....' + fiction['title'] + '快开始了加油~~~!' + page_code)
        for k, d in enumerate(storage_ls):
            print('制作文章中...' + d[1] + ' ---' + page_code)
            fiction_chapter: dict = {
                'title': d[1]
            }
            browser.get(d[0])
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located((By.ID, 'content')))
            content = browser.execute_script(content_script)
            fiction_chapter['content'] = content
            dt.append(fiction_chapter)
            print('完成小部分.....' + str(k+1))
        try:
            print('准备插入数据...')
            fiction['data'] = dt
            path = set_path('xiaoshuo')
            print(path)
            if bool(1-os.path.exists(path)):
                print('创建了文件夹  ', path)
                os.mkdir('xiaoshuo')
            os.chdir(path)  # 这里有问题会递归创建文件夹 紧急处理
            filename = str(fiction['title']) + '.txt'
            f = open(filename, 'w+')
            f.write(json.dumps(fiction))
            f.close()
            print('插入完成....')
            # batch_data(filename, path)
        except Exception as e:
            print('异常001', e.__str__())
    except TimeoutException:
        print('request page Time Out') # 这里需要做一些重复请求工作
    except NoSuchElementException:
        print('网页元素没找到')
    finally:
        browser.close()
    print('文章制作完成...')


def set_path(filename: str) -> str:
    path: str = os.getcwd()
    if platform.system() == 'Windows':
        path += '\\' + filename
    elif platform.system() == 'Linux':
        path += '/' + filename
    else:
        path += '/' + filename
    return path


def func_forward(tup: tuple = (0, 1, 9, 99999)):
    new_num = 1
    filename = set_path(str(tup[0]) + '.txt')
    if os.path.exists(filename):
        open_file = open(filename, 'r+')
        read_line = open_file.readline()
        if len(read_line) > 1:
            tup = tuple(eval(read_line))
        new_num = tup[1]
    else:
        open_file = open(filename, 'w+')

    origin_vs = tup[0]

    vs = tup[2]

    for i in range(origin_vs, vs):
        for j in range(new_num, tup[3]):
            tup1 = (i, j, tup[2], tup[3])
            open_file.seek(0)
            open_file.truncate()
            open_file.write(','.join('%s' % id for id in tup1))
            open_file.close()
            open_file = open(filename, 'r+')
            print(tup1)
            try:
                fetch_fiction(tup1)
            except Exception:
                print('数据库插入异常')
            finally:
                print('继续前进....' + str(i) + '_' + str(tup1[1]))
            # time.sleep(random.uniform(0.5, 1.8))
        print('结束这一次...' + str(i) + '_' + str(tup1[1]))
        open_file.close()
        terminal = i + 1
        if i == vs:
            break
        else:
            filename = set_path(str(terminal) + '.txt')
            open_file = open(filename, 'w+')
    open_file.close()


def t_request():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    try:
        browser.get('https://www.xbiquge6.com/0_1/')

        # print(browser.page_source)
    except TimeoutException:
        print('Time out')
    try:
        id_list = browser.find_element_by_id('list')
        dt: list = []
        for dd in id_list.find_elements(By.TAG_NAME, 'dd'):
            dt.append((dd.find_element(By.TAG_NAME, 'a').get_attribute('href'), dd.text))
        # print(dt.__len__())
        remainder = dt[1000:]
        for i, dd in enumerate(remainder):
            print('文章制作中....' + str(i))
            browser.get(dd[0])
            content = browser.find_element_by_id('content')
            requests.post('http://192.168.1.9:8093/polls/post_fiction_chapter/', data={
                'fiction_id': 1,
                'title': dd[1],
                'content': content.text
            })
        print('执行完成....!')
    except NoSuchElementException:
        print('element not found')
    finally:
        browser.close()


def batch_data(filename: str, path):

    try:

        # if ~data.__len__():
        #     dl = []
        #     for i in range(100):
        #         dl.append({'status': 'success', 'msg': 'operation mode ok'})
        #     data['data'] = dl
        os.chdir(path)
        file = open(filename, 'r')
        ls_ = file.read()
        data = json.loads(ls_)

        res = requests.post('http://192.168.1.9:8093/polls/post_batch_create_data/', json=data, headers={
            'Host': '192.168.1.9:8093',
            'Accept': 'application/json'
        })
    except InterruptedError:
        print('500内部出错')
    else:
        print(res.json())


def xiaoshuo():
    if os.path.exists('0.txt'):
        file = open('0.txt')
        print(tuple(eval(file.read())))
        file.close()
    else:
        print('is not exists')


if __name__ == '__main__':
    func_forward((89, 374))
    exit()
    ls: list = []
    suffix = 99
    min_num = 99999
    v = 10
    while suffix > 9:
        suffix = suffix - v
        ls.append((suffix, 1, suffix + v, min_num))
        if suffix <= 9:
            ls.append((0, 1, 9, min_num))
    ls.sort()
    pool = Pool(processes=10)
    pool.map(func_forward, ls)
    pool.close()
    pool.join()

