from oslo_config import cfg
from oslo_db import api as db_api
from oslo_db.sqlalchemy import session as db_session
from oslo_log import log as logging
from sqlalchemy.orm import exc

from pymsboot.db.tables.movie import *

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

_BACKEND_MAPPING = {'sqlalchemy': 'pymsboot.db.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING, lazy=True)


def get_instance():
    return IMPL


_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = db_session.enginefacade.get_legacy_facade()
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


def get_backend():
    return Connection()


def model_query(model, *args, **kwargs):
    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


class Connection(object):

    def __init__(self):
        pass

    def get_movie_by_id(self, id):
        session = get_session()
        query = session.query(Movie).filter_by(id=id)
        try:
            movie_db = query.one()
        except exc.NoResultFound:
            # TODO: process this situation
            return None
        return movie_db

    def get_all_movies(self):
        session = get_session()
        query = session.query(Movie)
        movies_db = query.all()
        return movies_db

    def create_movie(self, values):
        session = get_session()
        movie_db = Movie(**values)
        session.add(movie_db)
        session.commit()

    def update_movie(self, id, values):
        session = get_session()
        movie_db_query = session.query(Movie).filter_by(id=id)
        movie_db_query.update(values)
        movie_db = movie_db_query.one()
        session.commit()
        return movie_db

    def delete_movie_by_id(self, id):
        session = get_session()
        session.query(Movie).filter_by(id=id).delete()
        session.commit()
