import requests
from bs4 import BeautifulSoup


def get_html(url, header, params=None):
    r = requests.get(url, params=params, headers=header)
    return r


def get_count_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all(name='button', class_='NFa13')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    h = soup.find_all(name='h2', class_='NBbt')
    p = soup.find_all(name='p', class_='NBaa1')
    time = soup.find_all(name='time', class_='NLlj')

    times = []
    for item in time:
        times.append(item['datetime'])

    paragraph = []
    for item in p:
        paragraph.append(
            item.find('a', class_=None)['title']
        )

    news = []
    counter = 0
    for item in h:
        news.append({
            'siteName': '74.ru',
            'title': item.find('a', class_=None)['title'],
            'description': paragraph[counter],
            'datetime': times[counter],
            'urlNews': 'https://74.ru' + item.find('a', class_=None)['href']
        })
        counter += 1
    return news


def parse(url):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310', 'accept': '*/*'}
    host = 'https://74.ru/text/'
    url = host + url
    html = get_html(url, HEADERS)
    if html.status_code == 200:
        pages_count = get_count_pages(html.text)

        news = []
        for page in range(1, pages_count+1):
            html = get_html(url+f'&page={page}', header=HEADERS)
            news.extend(get_content(html.text))
        return news
