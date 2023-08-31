import urllib
import requests
from bs4 import BeautifulSoup
import json
import pymysql
import re
import time
import urllib as UrlUtils
from itertools import chain
import urllib.request as HttpUtils
import socket

base_url = "https://you.ctrip.com/restaurant/beijing"

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='wyj19735',
    db='travel_web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def write_in_datebase(name, city, introduce, pic_url):
    curse = connection.cursor()
    sql = "insert into snack(S_name,S_city,S_introduce,S_pic_url) values(\"%s\",\"%s\",\"%s\",\"%s\");" % (
        name, city, introduce, pic_url)
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
    response = HttpUtils.urlopen(request, timeout=60)
    print('====== Http request OK ======')
    return response.read().decode('utf-8')


def check_item(html, city):
    SN_url = ['', '', '', '', '', '']
    SN_name = ['', '', '', '', '', '']
    SN_Introduce = ['', '', '', '', '', '']
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('li[data-imgurl]')
    i = 0
    for element in elements:
        SN_url[i] = element['data-imgurl']
        i = i + 1

    dt_tags = soup.select('.card_list.fs_card dt')
    SN_name = [tag.text.strip() for tag in dt_tags]
    elements = soup.select('.card_list.fs_card .all_link')
    i = 0
    n = 0
    for element in elements:
        if i % 2 == 0:
            i = i + 1
            continue
        url2 = 'https://you.ctrip.com' + element.get('href')
        request = HttpUtils.Request(url2)
        request.get_method = lambda: 'GET'
        response = HttpUtils.urlopen(request, timeout=60)
        match = re.search(r'/(\d+)\.html', element.get('href'))
        soup2 = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')
        try:
            m = soup2.find('li', class_='infotext').string.strip()
            SN_Introduce[n] = m
        except AttributeError as e:
            SN_Introduce[n] = ''
        i = i + 1
        n = n + 1
    for i in range(n):
        write_in_datebase(SN_name[i], city, SN_Introduce[i], SN_url[i])
        print(SN_name[i])


if __name__ == "__main__":
    curse = connection.cursor()
    sql = "SELECT * from city;"
    connection.ping(reconnect=True)
    try:
        curse.execute(sql)
        x = curse.fetchall()
    except:
        print("数据库写入异常")
    connection.commit()
    connection.close()
    # print(x)
    for i in range(4,2691):  # 2691
        Cum = str(x[i]['Cum_X'])
        city = x[i]['Cname']
        try:
            page = getPage(Cum)
            check_item(page, city)
            print(city)
        except socket.timeout as e:
            time.sleep(20)
            i = i - 1
            continue
        except AttributeError as e:
            continue
        except urllib.error.URLError as e:
            time.sleep(20)
            i = i - 1
            continue
        if i % 50 == 0:
            time.sleep(20)
