from datetime import datetime
from exception import ServiceError
import pars_newsru
import pars_chelru
import time
import re

class NoNews(ServiceError):
    message = {"answer": "Новости закончились"}


class NewsService:
    def __init__(self, session):
        self.session = session

    def get_news(self, news):
        news_return = []

        result_date = str(datetime.strptime(news.finish_date, '%Y-%m-%d') -
                          datetime.strptime(news.start_date, '%Y-%m-%d'))

        try:
            result_date = int(result_date[:result_date.find('d')])
        except ValueError:
            result_date = 0

        if news.counter_news > result_date:
            raise NoNews

        # через unixtime т.к. dateutil в этой версии помер.
        unix_time = int((news.counter_news * 86400) + time.mktime(time.strptime(news.start_date, '%Y-%m-%d')))

        date_newsru_url = time.strftime("%d%b%Y", time.localtime(unix_time)).lower()
        date_chelru_url = time.strftime("%d.%m.%Y", time.localtime(unix_time)).lower()

        news_return.extend(pars_newsru.parse(date_newsru_url))
        news_return.extend(pars_chelru.parse(f'?dateFrom={date_chelru_url}&dateTo={date_chelru_url}'))
        news_return = (sorted(news_return, key=lambda x: x['datetime']))

        if news.key_word is not None and news.key_word != '':
            news_key_return = []
            for element in news_return:
                news_str = re.sub(r'[!"#?:.,*]', "", element.get('title').lower())

                if news.key_word.lower() in news_str.split(' '):
                    news_key_return.append(element)
            return news_key_return
        else:
            return news_return
