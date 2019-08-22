import pymysql
import time


def connect_mysql() -> pymysql.Connection:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='xiaoshuo',
                                 charset='utf8mb4',
                                 port=3308,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def db_insert(table, filed, data):
    connection_mode = connect_mysql()
    sql = "insert into `fiction` " + filed + " values(%s,%s,%s,%s,%s,%s,%s)"
    with connection_mode.cursor() as cursor:

        cursor.execute(sql, ('比爱哦', 'fffw', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'fef', 'success', 'ffff', 'vvvvv'))
    connection_mode.commit()
    print(sql)


if __name__ == '__main__':
    db_insert(1, "(`title`, `author`, `last_update_time`, `desc`, `status`, `convert`, `latest_chapter`)", 3)
