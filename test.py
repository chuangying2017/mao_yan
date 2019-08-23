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







tup = (0, 1)

filename = str(tup[0]) + '.txt'
if os.path.exists(filename):
    res = open(filename, 'r+')
    read_line = res.readline()
    res.close()
    tup1 = tuple(eval(read_line))
    print(eval(read_line))
else:
    res = open(filename, 'w')
    res.write(','.join('%d' %d for d in tup))
    res.close()



