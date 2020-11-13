from models import StatisticsModel
from sqlalchemy import and_, between
from exception import ServiceError
import time


class IncorrectData(ServiceError):
    message = {"answer": "Выберите временной промежуток"}


class StatisticService:
    def __init__(self, session):
        self.session = session

    def save_event(self, events, user_id):
        for event in (events.get('event')):
            unix_date = (int(time.mktime(time.strptime(event.get('datetime'), '%d-%m-%Y %H:%M:%S'))))
            old_event = (self.session.query(StatisticsModel)
                         .filter(and_(StatisticsModel.user_id == user_id,
                                      StatisticsModel.datetime == unix_date,
                                      StatisticsModel.action == event.get('action'))).first())

            if old_event is None:
                new_event = StatisticsModel(user_id=user_id, datetime=unix_date, action=event.get('action'))
                self.session.add(new_event)
                self.session.commit()

    def get_event(self, statistic):
        if statistic.start_date is None and statistic.finish_date is None and statistic.ready_date is None:
            raise IncorrectData()

        HOURS = 3600
        DAY = 86400

        if statistic.ready_date == 'this_day':
            start_date = int(time.time()) - DAY
            finish_date = int(time.time())
        elif statistic.ready_date == 'this_hours':
            start_date = int(time.time()) - HOURS
            finish_date = int(time.time())
        else:
            start_date = int(time.mktime(time.strptime(statistic.start_date, '%Y-%m-%d')))
            finish_date = int(time.mktime(time.strptime(statistic.finish_date, '%Y-%m-%d')))

        query = (
            self.session.query(StatisticsModel)
            .filter(between(StatisticsModel.datetime, start_date, finish_date)).all()
        )
        return_event = []
        for event in query:
            return_event.append(event.as_dict())

        for item in return_event:
            item.update({'datetime': time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(item.get('datetime')))})

        return return_event
