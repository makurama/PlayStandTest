from marshmallow import ValidationError, fields, validates, validates_schema
from scheme.base_scheme import BaseSchema
from entities.statistic import Statistic


class StatisticScheme(BaseSchema):
    """
    validates input data
    """
    __entity_class__ = Statistic
    start_date = fields.String(missing=None)
    finish_date = fields.String(missing=None)
    page = fields.Integer(required=True)
    ready_date = fields.String(missing=None)

    @validates('ready_date')
    def validate_ready_date(self, ready_date):
        access_date = ('this_day', 'this_hours')
        if ready_date is not None:
            if ready_date not in access_date:
                raise ValidationError(f'Доступные периоды: {access_date}')

    @validates('page')
    def validate_page(self, page):
        if page < 0:
            raise ValidationError('page должно быть положительным числом')

    @validates_schema
    def validate_date(self, data, **kwargs):
        if data['finish_date'] == '' and data['start_date'] == '':
            data['finish_date'] = None
            data['start_date'] = None

        if data['start_date'] is not None and data['finish_date'] is not None:

            if data['start_date'] > data['finish_date']:
                raise ValidationError('start_date не должен быть больше '
                                      'finish_date')


statistic_scheme = StatisticScheme()
