import time

from oslo_log import log as logging

from pymsboot.db.api import get_connection
from pymsboot.db.models import Movie

LOG = logging.getLogger(__name__)


class MovieHandler():
    def __init__(self):
        self.db_conn = get_connection()

    def add(self, movie_dict):
        movie_id = movie_dict['id']
        LOG.info('Add movie {}'.format(movie_id))
        movie_dict['state'] = 'Downloading'
        movie = Movie(**movie_dict)
        self.db_conn.add_movie(movie)
        LOG.info('Start download movie {}'.format(movie_id))
        time.sleep(30)
        LOG.info('Finished download movie {}'.format(movie_id))
        self.db_conn.update_movie_state(movie_id, 'Downloaded')
        LOG.info('Finished to add movie {}'.format(movie_id))

    def delete(self, movie_id):
        LOG.info('Delete movie {}'.format(movie_id))
        time.sleep(10)
        self.db_conn.delete_movie_by_id(movie_id)
        LOG.info('Finished to delete movie {}'.format(movie_id))

    def update(self, movie_id, url):
        LOG.info('Update movie {}'.format(movie_id))
        LOG.info('Start download movie {} from {}'.format(movie_id, url))
        time.sleep(40)
        LOG.info('Finished download movie {} from {}'.format(movie_id, url))
        self.db_conn.update_movie_url(movie_id, url)
        LOG.info('Finished to update movie {}'.format(movie_id))

    def get(self, movie_id):
        LOG.info('Get movie {}'.format(movie_id))
        time.sleep(3)
        movie_dict = self.db_conn.get_movie_by_id(movie_id).to_dict()
        LOG.info('Finished to get info of movie {}'.format(movie_id))
        return movie_dict

    def get_all(self):
        LOG.info('Get all movies')
        time.sleep(5)
        all_movie_list = [m.to_dict() for m in self.db_conn.get_all_movies()]
        LOG.info('Finished to get all movies')
        return all_movie_list
