from oslo_config import cfg
from oslo_log import log as logging
from sqlalchemy import create_engine
from sqlalchemy.orm import exc, scoped_session, sessionmaker

from pymsboot.db.tables.movie import *

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def db_init():
    engine = create_engine(CONF.db_connection)
    session_factory = sessionmaker(bind=engine)
    global Session
    Session = scoped_session(session_factory)


class DbApi(object):
    def __init__(self):
        self.session = Session()

    def get_movie_by_uuid(self, uuid):
        query = self.session.query(Movie).filter_by(uuid=uuid)
        try:
            movie_db = query.one()
        except exc.NoResultFound:
            # TODO: process this situation
            return None
        return movie_db

    def get_all_movies(self):
        query = self.session.query(Movie)
        movies_db = query.all()
        return movies_db

    def create_movie(self, movie_dict):
        movie_db = Movie(**movie_dict)
        self.session.add(movie_db)
        self.session.commit()
        movie_db = self.session.query(Movie).filter_by(uuid=movie_dict['uuid']).one()
        return movie_db

    def update_movie(self, uuid, values):
        movie_db_query = self.session.query(Movie).filter_by(uuid=uuid)
        movie_db_query.update(values)
        self.session.commit()
        movie_db = movie_db_query.one()
        return movie_db

    def delete_movie_by_uuid(self, uuid):
        self.session.query(Movie).filter_by(uuid=uuid).delete()
        self.session.commit()
