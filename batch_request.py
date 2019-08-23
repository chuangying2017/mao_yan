# _*_coding=utf-8_*_
import multiprocessing
import time
from collections import OrderedDict
import hashlib
import linecache
import os
import requests
import json


def formatUrlAndHeader(des, singer, songName):
    # 生成url和header的逻辑
    return url, h


# 每个进程都去读各自的文件,然后以写文件的方式保存当前的执行记录,为了预防断电或者其他程序异常终止情况
def worker(fileName):
    descr = ["播放", "搜索", "搜", "听", "我要听", "我想听", "来一首", "来一个", "来一段", "来一曲", "来首", "来个", "来段", "来曲"]
    Logprefix = os.path.split(fileName)[1].replace(".txt", "")
    resultLogPath = os.path.join(os.getcwd(), "log", Logprefix + ".log")
    logbreakPoint = os.path.join(os.getcwd(), "log", Logprefix + ".txt")
    with open(logbreakPoint, "r") as b:
        startLine = int(b.read())
        b.close()
    with open(resultLogPath, "a+", encoding="utf-8") as logF:
        with open(fileName, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
            LineNum = startLine
            for j in range(len(lines) - startLine + 1):
                LineContent = linecache.getline(fileName, LineNum)
                for i in descr:
                    line = LineContent.split("\t")
                    singer = line[0]
                    song = line[1].replace("\n", "")
                    uAndH = formatUrlAndHeader(i, singer, song)
                    try:
                        r = requests.get(url=uAndH[0], headers=uAndH[1])
                        with open(logbreakPoint, "w") as w:
                            w.write(str(LineNum))
                        print("searching:%s, line: %d\n" % (fileName, LineNum))
                        result = json.loads(r.text)
                        resultSinger = result["data"]["sounds"][0]["singer"]
                        resultSong = result["data"]["sounds"][0]["title"]
                        if not (resultSinger == singer and resultSong == song):
                            logF.write("Error: search des: %s, singer:%s, song:%s;return: %s\n" % (
                            i, singer, song, r.text.encode('latin-1').decode('unicode_escape')))
                    except Exception as e:
                        logF.write("Error: search des: %s, singer:%s, song:%s;return: %s\n" % (
                        i, singer, song, str(e).encode('latin-1').decode('unicode_escape')))
                LineNum += 1
        logF.close()


if __name__ == '__main__':
    orgPath = os.path.join(os.getcwd(), "data")
    files = os.listdir(orgPath)
    for i in files:
        f = os.path.join(orgPath, i)
        if os.path.isfile(f):
            p = multiprocessing.Process(target=worker, args=(f,))
            p.start()
