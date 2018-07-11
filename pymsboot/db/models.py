from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class PymsbootBase():

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


Base = declarative_base(cls=PymsbootBase)


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(String(255), primary_key=True, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    rank = Column(Integer)
    url = Column(String(255))
    state = Column(String(64))
