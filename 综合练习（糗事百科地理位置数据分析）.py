import requests
from bs4 import BeautifulSoup
import re
import json
import xlwt
import time


url_pri = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i)) for i in range(1, 11)]


headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110'
                  ' Safari/537.36'
}

places = []
geo_datas = []


def get_info(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    user_urls = soup.select('a.recmd-user')
    data = []
    # 将每个用户的详细页连接保存
    for user_url in user_urls:
        user_url = 'https://www.qiushibaike.com' + user_url.get('href')
        data.append(user_url)
    # 访问每个用户的详细页，爬取地理信息
    for user_url in data:
        user_data = requests.get(user_url, headers=headers)
        user_place = re.findall('<li><span>故乡:</span>(.*?)</li>', user_data.text, re.S)
        places.append(user_place)


def print_xls():
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet1')
    # 写入表头
    sheet.write(0, 0, 'address')
    sheet.write(0, 1, 'longitude')
    sheet.write(0, 2, 'latitude')
    # 写入数据
    i = 1
    for item in geo_datas:
        sheet.write(i, 0, item[0])
        sheet.write(i, 1, item[1])
        sheet.write(i, 2, item[2])
        i += 1
    book.save('result.xls')


def api_change():
    url = 'http://restapi.amap.com/v3/geocode/geo'
    for item in places:
        if item == []:
            continue
        if item[0:1] == '国外':
            continue
        par = {'address': item, 'key': 'cb649a25c1f81c1451adbeca73623251'}
        res = requests.get(url, par)
        json_data = json.loads(res.text)
        try:
            geo = json_data['geocodes'][0]['location']
            longitude = geo.split(',')[0]
            latitude = geo.split(',')[1]
            geo_data = [item, longitude, latitude]
            geo_datas.append(geo_data)
        except:
            pass


if __name__ == '__main__':
    for url in url_pri:
        get_info(url)
    api_change()
    print_xls()