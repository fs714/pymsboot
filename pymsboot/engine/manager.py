import oslo_messaging as messaging
from oslo_log import log as logging

from pymsboot.driver.storage import MovieHandler
from pymsboot.rpc.manager import Manager

LOG = logging.getLogger(__name__)


class EngineManager(Manager):
    RPC_API_NAMESPACE = 'engine'
    RPC_API_VERSION = '1.0'
    target = messaging.Target(namespace=RPC_API_NAMESPACE, version=RPC_API_VERSION)

    def __init__(self):
        super(EngineManager, self).__init__()
        self.movie_handler = MovieHandler()

    def get_movie(self, ctx, **kwargs):
        LOG.info('Get movie {}'.format(kwargs.get("uuid")))

    def get_all_movie(self, ctx, **kwargs):
        LOG.info('Get all movie')
        return {'key': 'value'}

    def create_movie(self, ctx, movie_obj):
        LOG.info('Add movie {}'.format(movie_obj.id))
        # movie_obj.state = 'Downloading'
        # movie_obj.create(ctx)
        # self.movie_handler.download(movie_obj.id, movie_obj.url)
        # movie_obj.state = 'Downloaded'
        # movie_obj.update(ctx)

    def update_movie(self, ctx, movie_obj):
        LOG.info('Update movie {}'.format(movie_obj.id))
        # movie_obj.state = 'Downloading'
        # movie_obj.update(ctx)
        # self.movie_handler.remove(movie_obj.id)
        # self.movie_handler.download(movie_obj.id, movie_obj.url)
        # movie_obj.state = 'Downloaded'
        # movie_obj.update(ctx)

    def delete_movie(self, ctx, movie_id):
        LOG.info('Delete movie {}'.format(movie_id))
        # movie_obj = objects.Movie.get_by_id(ctx, movie_id)
        # self.movie_handler.remove(movie_id)
        # movie_obj.delete(ctx, movie_id)
