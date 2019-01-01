import requests
from bs4 import BeautifulSoup
import time
import xlwt


headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110'
                  ' Safari/537.36'
}


all_data = []


def get_data(url):
    data_pri = requests.get(url, headers=headers)
    soup = BeautifulSoup(data_pri.text, 'html.parser')
    names = soup.select('div.book-mid-info > h4 > a')
    writers = soup.select('p.author > a.name')
    discribles = soup.select('p.intro')
    for name, writer, discrible in zip(names, writers, discribles):
        name = name.getText(),
        writer = writer.getText(),
        discrible = discrible.getText()
        data = [name, writer, discrible]
        all_data.append(data)

    time.sleep(1)


if __name__ == '__main__':
    url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1'
    get_data(url)
    header = ['title', 'writer', 'discrible']

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    i = 1
    for data in all_data:
        j = 0
        for item in data:
            sheet.write(i, j, item)
            j += 1
        i += 1
    book.save('xiaoshuo.xls')