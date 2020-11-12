from models import UserModel
from sqlalchemy import func, and_, between
from datetime import datetime
from exception import ServiceError
from typing import List
import pars_newsru
import pars_chelru
import time


class NoNews(ServiceError):
    message = {"answer": "Новости закончились"}


class NewsService:
    """
    сlass implements business logic get methods
    """
    def __init__(self, session):
        """
        class constructor
        :param session: connect to db
        :param user_id: user id in session
        """
        self.session = session

    def get_news(self, news):
        """
        generates a report on the specified parameters
        :param report: data for search
        :return: dataclass report
        """
        # if тут убрать, т.к. все моменты из него я покрыл
        news_return = []
        if (news.start_date is not None and news.start_date != ''
                and news.finish_date is not None and news.start_date != ''):

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


        # else: # тут я пошел в понятный код, а не в минимальность кода
        #     print('tyt')
        #     # date_chelru_url = time.strftime("%d.%m.%Y", time.localtime(int(time.time()))).lower()
        #     # news_return.extend(pars_newsru.parse(''))
        #     # news_return.extend(pars_chelru.parse(f'?dateFrom={date_chelru_url}&dateTo={date_chelru_url}'))
        #     # news_return = (sorted(news_return, key=lambda x: x['datetime']))

        if news.key_word is not None and news.key_word != '':
            news_key_return = []
            for element in news_return:
                if news.key_word.lower() in element.get('title').lower().split(' '):
                    news_key_return.append(element)
            return news_key_return
        else:
            return news_return
