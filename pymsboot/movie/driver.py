import time

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class MovieHandler():
    def __init__(self):
        pass

    def download(self, movie_id, url):
        LOG.info('Start download movie {} from {}'.format(movie_id, url))
        time.sleep(15)
        LOG.info('Finished download movie {} from {}'.format(movie_id, url))

    def remove(self, movie_id):
        LOG.info('Delete movie {}'.format(movie_id))
        time.sleep(5)
        LOG.info('Finished to delete movie {}'.format(movie_id))
