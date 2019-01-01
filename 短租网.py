import requests
from bs4 import BeautifulSoup
import time

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110'
                  ' Safari/537.36'
}


# 判断性别函数
def judgement_sex(class_name):
    if class_name == ['member_icol']:
        return '女'
    else:
        return '男'


# 获取详细页url
def get_links(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        href = link.get("href")
        get_info(href)


# 获取网页信息
def get_info(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    tittles = soup.select('div.pho_info > h4')       # ????????????
    addresses = soup.select('span.pr5')
    for tittle, address in zip(tittles, addresses):
        data = {
            'tittle': tittle.get_text().strip(),
            'address': address.get_text().strip(),
        }
        print(data)


if __name__ == '__main__':
    urls = [
        'https://xa.xiaozhu.com/search-duanzufang-p1-0/'
    ]
    for single_url in urls:
        get_links(single_url)
        time.sleep(2)
'''
    #不返回结果？？？？？
'''