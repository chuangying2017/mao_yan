import requests
from pyquery import PyQuery
import lxml
import csv

url = 'https://www.hongxiu.com/'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/76.0.3809.100 Safari/537.36",
           'Host': 'www.hongxiu.com'
           }


def get_index():
    global url, headers

    res = requests.get(url, headers=headers)
    text_content = res.content
    d = PyQuery(text_content)
    new_book_list = d('#new-book-list')
    ul_list = new_book_list.find('ul')
    all_li = ul_list.find('li')
    list_store = []
    for v in all_li.items():
        children = v.children()
        # print(children('.book-info h4 a').html());break
        children_author = children('.book-info .cf')
        dict_new = {
            'convert': children('.book-img img').attr('src'),  # 封面图片
            'title': children('.book-info h4 a').html(),   # 小说标题
            'url': children('.book-img a').attr('href'),  # 小说地址
            'description': children('.book-info p').html(),
            'author': children_author.find('i').html(),
            'class': children_author.find('a').text()
        }
        list_store.append(dict_new)
    write_to_csvRows(list_store, ['convert', 'title', 'url', 'description', 'author', 'class'])


def write_to_csvField(fieldnames):
    '''写入csv文件字段'''
    with open("author_fiction.csv", 'a', encoding='utf-8', newline='') as f:
        # 将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 调用writeheader方法写入字段名
        writer.writeheader()


def write_to_csvRows(content, fieldnames):
    """写入csv文件内容"""
    with open("author_fiction.csv", 'a', encoding='utf-8', newline='') as f:
        # 将字段名传给Dictwriter来初始化一个字典写入对象
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 调用writeheader方法写入字段名
        # writer.writeheader()            ###这里写入字段的话会造成在抓取多个时重复.
        writer.writerows(content)
        f.close()


def read_csv_data():
    with open('author_fiction.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        tup = ()
        for line in reader:
            if i <= 0:
                i += 1
                continue
            i += 1



if __name__ == '__main__':
    read_csv_data()
