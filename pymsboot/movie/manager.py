import oslo_messaging as messaging
from oslo_log import log as logging

from pymsboot.rpc.manager import Manager
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

    def add_movie(self, ctx, movie_dict):
        LOG.info('Add movie {}'.format(movie_dict['id']))
        self.movie_handler.add(movie_dict)

    def delete_movie(self, ctx, movie_id):
        LOG.info('Delete movie {}'.format(movie_id))
        self.movie_handler.delete(movie_id)

    def update_movie(self, ctx, movie_id, url):
        LOG.info('Update movie {} from {}'.format(movie_id, url))
        self.movie_handler.update(movie_id, url)

    def get_movie(self, ctx, movie_id):
        LOG.info('Get movie {}'.format(movie_id))
        return self.movie_handler.get(movie_id)

    def get_all_movies(self, ctx):
        LOG.info('Get all movies')
        return self.movie_handler.get_all()
