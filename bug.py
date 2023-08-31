import urllib
import requests
from bs4 import BeautifulSoup
import json
import pymysql
import time
import urllib as UrlUtils
import urllib.request as HttpUtils
import socket

base_url = "https://you.ctrip.com/place/tianjin"

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='wyj19735',
    db='travel_web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def write_in_datebase(title, num):
    curse = connection.cursor()
    sql = "insert into city(Cname,Cum_X) values(\"%s\",\"%s\");" % (title, num)
    connection.ping(reconnect=True)
    try:
        curse.execute(sql)
    except:
        print("数据库写入异常")
    connection.commit()
    connection.close()


def getPage(num):
    url = base_url + num + ".html"
    request = HttpUtils.Request(url)
    request.get_method = lambda: 'GET'
    response = HttpUtils.urlopen(request, timeout=10)
    print('====== Http request OK ======')
    return response.read().decode('utf-8')


def check_item(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(attrs={'class': 'destination-name-main'}).string.strip()
    print(title)
    return title


if __name__ == "__main__":
    for i in range(118, 4000):
        try:
            page = getPage(str(i))
            city = check_item(page)
        except socket.timeout as e:
            time.sleep(20)
            i = i-1
            continue
        except AttributeError as e:
            continue
        except urllib.error.URLError as e:
            time.sleep(20)
            i = i - 1
            continue
        if i % 50 == 0:
            time.sleep(20)
        write_in_datebase(city, i)
