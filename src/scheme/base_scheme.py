from marshmallow import Schema, post_load


class BaseSchema(Schema):
    """
    Базовая схема для наследования
    """
    __entity_class__ = None

    @post_load
    def make_object(self, data, **kwargs):
        return self.__entity_class__(**data)