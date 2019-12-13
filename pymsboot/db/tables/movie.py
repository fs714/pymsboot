import datetime
import uuid

from sqlalchemy import Integer, String, Column, DateTime, JSON

from pymsboot.db.models import Base


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(String(64), default=str(uuid.uuid1()))
    name = Column(String(64), nullable=False, unique=True)
    rank = Column(Integer)
    url = Column(String(255))
    state = Column(String(64))
    meta = Column(JSON)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    updated_time = Column(DateTime, onupdate=datetime.datetime.utcnow)