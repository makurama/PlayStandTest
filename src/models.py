from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True)
    password = Column(Text)
    role = Column(Text)

    def as_dict(self):
        account = {c.name: getattr(self, c.name)
                   for c in self.__table__.columns}
        account.pop('password')
        return account


class StatisticsModel(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    datetime = Column(Integer)
    action = Column(Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

