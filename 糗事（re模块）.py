import requests
import re


# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110'
                  ' Safari/537.36'
}


# 初始化列表以装入爬虫信息
info_lists = []


def judgement_sex(class_name):
    if class_name == "womenIcon":
        return 'woman'
    else:
        return 'man'


def get_info(url):
    res = requests.get(url)
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.text, re.S)
    sexs = re.findall('<div class="articleGender (.*?)">', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    comments = re.findall('<i class="number">(\d+)</i> 评论', res.text, re.S)
    for id, level, sex, content, comment in zip(ids, levels, sexs, contents, comments):
        info = {
            'id': id,
            'level': level,
            'sex': judgement_sex(sex),
            'content': content,
            'comment': comment
        }
        info_lists.append(info)


if __name__ == '__main__':
    urls = ["https://www.qiushibaike.com/text/page/2/"]
    for url in urls:
        get_info(url)
    for info_list in info_lists:
        f = open('C:/Users/Xue/Desktop/a.txt', 'a+')
        try:
            f.write(info_list['id']+'\n')
            f.write(info_list['level'] + '\n')
            f.write(info_list['sex'] + '\n')
            f.write(info_list['content'] + '\n')
            f.write(info_list['comment'] + '\n\n')
            f.close()
        except UnicodeEncodeError:
            pass
