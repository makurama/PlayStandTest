from marshmallow import fields, validate
from scheme.base_scheme import BaseSchema
from entities.auth import Auth


class AuthSchema(BaseSchema):
    __entity_class__ = Auth
    login = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


auth_schema = AuthSchema()
