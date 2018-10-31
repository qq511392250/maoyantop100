import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

from bs4 import  BeautifulSoup
import random

User_Agents ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}



def get_one_page(url):
    try:
        response  = requests.get(
            url, headers=User_Agents)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]

        }



def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8')as  f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n',)
        f.close()


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
