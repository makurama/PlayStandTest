from marshmallow import fields, validate
from entities.user import UserCreate, BaseUser
from scheme.base_scheme import BaseSchema


class UserCreateSchema(BaseSchema):
    """
    AuthSchema - class for validating registration data
    """
    __entity_class__ = UserCreate
    login = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


class GetUserCreateSchema(BaseSchema):
    """
    AuthSchema - class for validating getting user data
    """
    __entity_class__ = BaseUser
    login = fields.Email(required=True)


get_user_schema = GetUserCreateSchema()
user_schema = UserCreateSchema()
