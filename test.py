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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException



url = 'https://www.xbiquge6.com'
headers = {
    'Host': 'www.xbiquge6.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


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
                'content': content
            })
        print('执行完成....!')
    except NoSuchElementException:
        print('element not found')
    finally:
        browser.close()


if __name__ == '__main__':
    t_request()