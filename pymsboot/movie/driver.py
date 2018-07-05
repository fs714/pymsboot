import time

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class MovieHandler():
    def __init__(self):
        self.db = None

    def add(self, movie):
        LOG.info('Add new movie {}'.format(movie))
        LOG.info('Download new movie {}'.format(movie))
        time.sleep(10)
        LOG.info('Update DB for new movie {}'.format(movie))
        LOG.info('Finished to add new movie {}'.format(movie))

    def delete(self, movie):
        LOG.info('Delete movie {}'.format(movie))
        time.sleep(2)
        LOG.info('Update DB for deleting movie {}'.format(movie))
        LOG.info('Finished to delete movie {}'.format(movie))

    def update(self, movie):
        LOG.info('Update movie {}'.format(movie))
        time.sleep(5)
        LOG.info('Update DB for update movie {}'.format(movie))
        LOG.info('Finished to update movie {}'.format(movie))

    def get(self, movie):
        LOG.info('Get movie {}'.format(movie))
        LOG.info('Get info from DB for movie {}'.format(movie))
        LOG.info('Finished to get info of movie {}'.format(movie))
        return movie
