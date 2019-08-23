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




ls:list = []

for i in range(100):
    ls.append({'name': 'zahng', 'age': '23'})



res = requests.post('http://192.168.1.9:8093/polls/post_fiction_chapter/', data=[{'name': 'zahng', 'age': '23'}, {'name': 'zahng', 'age': '23'}, {'name': 'zahng', 'age': '23'},{'name': 'zahng', 'age': '23'}])

print(res)



