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

base_url = "https://you.ctrip.com/place/tianjin"

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='wyj19735',
    db='travel_web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def write_in_datebase(name, city, score, popularity, message, address, time, introduce, pic_url, sIntroduce):
    curse = connection.cursor()
    sql = "insert into scenic_zone(SZ_name,SZ_city,SZ_score,SZ_popularity,SZ_message,SZ_address,SZ_time,SZ_introduce," \
          "SZ_pic_url,SZ_sIntroduce) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");" % (
              name, city, score, popularity, message, address, time, introduce, pic_url, sIntroduce)
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
    pic_url = ['', '', '', '', '', '']
    pic_name = ['', '', '', '', '', '']
    pic_score = [0, 0, 0, 0, 0, 0]
    pic_popularity = [0, 0, 0, 0, 0, 0]
    pic_SI = ['', '', '', '', '', '']
    SZ_address = ['', '', '', '', '', '']
    SZ_time = ['', '', '', '', '', '']
    SZ_Introduce = ['', '', '', '', '', '']
    SZ_message = [0, 0, 0, 0, 0, 0]
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(attrs={'class': 'destination-name-main'}).string.strip()
    elements = soup.select('.guide-main-item-top[style*="background-image"]')
    i = 0
    for element in elements:
        pic_url[i] = element['style'].split('url(')[1].split(')')[0]
        i = i + 1
    elements = soup.select('.title')
    i = 0
    for element in elements:
        pic_name[i] = element.text
        i = i + 1
    elements = soup.select('.tag')
    i = 0
    for element in elements:
        try:
            x = element.select_one('span:first-child').text
            try:
                x = float(re.sub(r'[\u4e00-\u9fa5]+', '', x))
            except ValueError as e:
                x = float('0')
            pic_score[i] = x
            s = element.select_one('span:last-child').text
            s = re.sub(r'[\u4e00-\u9fa5]+', '', s)
            if 'w' in s:
                # 将字符串中的字母'w'替换为空字符串，并将数字乘以10000
                s = re.sub(r'w', '', s)
                s = int(re.search(r'\d+', s).group(0)) * 10000
            else:
                # 如果字符串中不包含字母'w'，直接提取其中的数字并转换为整数类型
                s = int(re.search(r'\d+', s).group(0))
            pic_popularity[i] = s
        except:
            pic_popularity[i] = 0
            pic_score[i] = 0
        i = i + 1
    elements = soup.select('.txt')
    i = 0
    for element in elements:
        pic_SI[i] = element.text
        i = i + 1

    elements = soup.select('.guide-main-item')
    i = 0
    for element in elements:
        request = HttpUtils.Request(element.get('href'))
        request.get_method = lambda: 'GET'
        response = HttpUtils.urlopen(request, timeout=60)
        match = re.search(r'/(\d+)\.html', element.get('href'))
        if match:
            SZ_message[i] = int(match.group(1))
        soup2 = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')
        try:
            SZ_address[i] = soup2.find(attrs={'class': 'baseInfoText'}).string.strip()
        except AttributeError as e:
            SZ_address[i] = ''
        try:
            SZ_time[i] = soup2.find('p', {'class': 'baseInfoText cursor openTimeText'}).get_text().strip()
        except AttributeError as e:
            SZ_time[i] = ''
        inset_p_list = soup2.find_all('p', {'class': 'inset-p'})
        p = 0
        for inset_p in inset_p_list:
            if p >= 2:
                break
            SZ_Introduce[i] += inset_p.get_text(strip=True)
            SZ_Introduce[i] += '\n'
            p = p + 1
        i = i + 1
    for i in range(6):
        write_in_datebase(pic_name[i], city, pic_score[i], pic_popularity[i], SZ_message[i], SZ_address[i], SZ_time[i],
                          SZ_Introduce[i], pic_url[i], pic_SI[i])
        print(pic_name[i])


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
    for i in range(2043, 2691):  # 2691
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

    # page = getPage('1')
    # city = check_item(page)
    # for i in range(118, 4000):
    #     try:
    #         page = getPage(str(i))
    #         city = check_item(page)
    #     except socket.timeout as e:
    #         time.sleep(20)
    #         i = i-1
    #         continue
    #     except AttributeError as e:
    #         continue
    #     except urllib.error.URLError as e:
    #         time.sleep(20)
    #         i = i - 1
    #         continue
    #     if i % 50 == 0:
    #         time.sleep(20)
    #     write_in_datebase(city, i)
