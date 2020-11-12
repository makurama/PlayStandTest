from dataclasses import dataclass


@dataclass
class BaseUser:
    """
    parent class to inherit
    """
    login: str


@dataclass
class UserCreate(BaseUser):
    """
    class for converting insert data
    """
    password: str
