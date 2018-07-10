from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative

Base = declarative.declarative_base()


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(String(255), primary_key=True, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    rank = Column(Integer)
    url = Column(String(255))
    state = Column(String(64))

    def as_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
