from marshmallow import ValidationError, fields, validates, validates_schema
from scheme.base_scheme import BaseSchema
from entities.news import NewsGet
import time

class NewsScheme(BaseSchema):
    """
    validates input data
    """
    __entity_class__ = NewsGet
    start_date = fields.String(missing=time.strftime("%Y-%m-%d", time.localtime(int(time.time()))).lower())
    finish_date = fields.String(missing=time.strftime("%Y-%m-%d", time.localtime(int(time.time()))).lower())
    key_word = fields.String(missing=None)
    counter_news = fields.Integer(missing=0)

    @validates('counter_news')
    def validate_page_size(self, counter_news):
        if counter_news < 0:
            raise ValidationError('Не кибербульте')


    @validates_schema
    def validate_counter_news(self, date, **kwargs):
        if date['finish_date'] == '' and date['start_date'] == '':
            date['finish_date'] = time.strftime("%Y-%m-%d", time.localtime(int(time.time()))).lower()
            date['start_date'] = time.strftime("%Y-%m-%d", time.localtime(int(time.time()))).lower()

        if date['finish_date'] < date['start_date']:
            raise ValidationError('Неверное действие с датами')

news_scheme = NewsScheme()