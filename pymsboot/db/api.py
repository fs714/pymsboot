from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy import create_engine
from sqlalchemy.orm import exc
from sqlalchemy.orm import sessionmaker

from pymsboot.db import models as db_models

EXIST_MOVIES_DB = [
    {
        'id': 'e00cbfb3-ae3a-469d-955d-eea64c27c7af',
        'name': 'Titanic',
        'rank': 1,
        'url': 'http://www.baidu.com',
        'state': 'Downloaded',
    },
    {
        'id': 'c840f0b6-0d28-4c0c-abaa-f96dca76c057',
        'name': 'Your Name',
        'rank': 2,
        'url': 'http://www.baidu.com',
        'state': 'Downloaded',
    }
]

_ENGINE = None
_SESSION_MAKER = None
_CONNECTION = None

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def db_setup():
    LOG.info('Setup DB')
    _ENGINE = create_engine(CONF.db_engine)
    db_models.Base.metadata.drop_all(_ENGINE)
    db_models.Base.metadata.create_all(_ENGINE)

    LOG.info('Init DB Data')
    for m in EXIST_MOVIES_DB:
        get_connection().add_movie(db_models.Movie(**m))


def get_engine():
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    LOG.info('Init DB Engine')
    _ENGINE = create_engine(CONF.db_engine)
    return _ENGINE


def get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER

    LOG.info('Init DB Session Maker')
    _SESSION_MAKER = sessionmaker(bind=engine)
    return _SESSION_MAKER


def get_session():
    engine = get_engine()
    maker = get_session_maker(engine)
    session = maker()

    return session


def get_connection():
    global _CONNECTION
    if _CONNECTION is not None:
        return _CONNECTION

    LOG.info('Init DB API')
    _CONNECTION = Connection()
    return _CONNECTION


class Connection(object):

    def __init__(self):
        pass

    def get_movie_by_id(self, id):
        session = get_session()
        query = session.query(db_models.Movie).filter_by(id=id)
        try:
            movie = query.one()
        except exc.NoResultFound:
            # TODO: process this situation
            return None

        return movie

    def get_all_movies(self):
        session = get_session()
        query = session.query(db_models.Movie)
        movies = query.all()

        return movies

    def add_movie(self, movie):
        session = get_session()
        session.add(movie)
        session.commit()

    def update_movie_state(self, id, state):
        session = get_session()
        session.query(db_models.Movie).filter_by(id=id).update({'state': state})
        session.commit()

    def update_movie_url(self, id, url):
        session = get_session()
        session.query(db_models.Movie).filter_by(id=id).update({'url': url})
        session.commit()

    def delete_movie_by_id(self, id):
        session = get_session()
        session.query(db_models.Movie).filter_by(id=id).delete()
        session.commit()
