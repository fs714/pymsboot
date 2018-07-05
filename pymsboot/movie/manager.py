import oslo_messaging as messaging
from oslo_log import log as logging

from pymsboot.manager import Manager
from pymsboot.movie.driver import MovieHandler

LOG = logging.getLogger(__name__)


class MovieManager(Manager):
    RPC_API_NAMESPACE = 'movie'
    RPC_API_VERSION = '1.0'
    target = messaging.Target(namespace=RPC_API_NAMESPACE, version=RPC_API_VERSION)

    def __init__(self):
        super(MovieManager, self).__init__()
        self.movie_handler = MovieHandler()

    def init_host(self):
        LOG.info('Invoke init_host')

    def add_movie(self, movie):
        LOG.info('Add movie {}'.format(movie))
        self.movie_handler.add(movie)

    def delete_movie(self, movie):
        LOG.info('Delete movie {}'.format(movie))
        self.movie_handler.delete(movie)

    def update_movie(self, movie):
        LOG.info('Update movie {}'.format(movie))
        self.movie_handler.update(movie)

    def get_movie(self, movie):
        LOG.info('Get movie {}'.format(movie))
        return self.movie_handler.get(movie)
