import requests
from bs4 import BeautifulSoup
from re import sub
from datetime import datetime

def get_html(url, header, params=None):
    r = requests.get(url, params=params, headers=header)
    return r


def transformDate(strDate, url):
    dateString = url[url.rfind('/')+1:]
    findMiddle = strDate.find(':')

    dateString = dateString[:2] + ' ' + dateString[2:5] + ' ' + dateString[5:] + ' ' + strDate[findMiddle-2:findMiddle+3]

    return str(datetime.strptime(dateString, '%d %b %Y %H:%M'))


def get_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(name='div', class_='index-news-content')

    news = []
    for item in items:
        news.append({
            'siteName': 'newsru.com',
            'title': sub('[\\t\\n]', '', item.find('a', class_='index-news-title').get_text()),
            'description': sub('[\\t\\n]', '', item.find('a', class_='index-news-text').get_text()),
            'datetime': transformDate(sub('[\\t\\n]', '', item.find('span', class_='index-news-date').get_text()), url),
            'urlNews': 'https://www.newsru.com' + item.find('a', class_='index-news-title')['href']
        })

    return news


def parse(url):
    HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310', 'accept': '*/*'}

    host = 'https://www.newsru.com/allnews/'
    url = host + url
    html = get_html(url, HEADER)
    if html.status_code == 200:
        return get_content(html.text, url)