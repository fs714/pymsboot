import oslo_messaging as messaging
from oslo_log import log as logging

from pymsboot.db import api as db_api
from pymsboot.driver.storage import MovieHandler
from pymsboot.rpc.manager import Manager

LOG = logging.getLogger(__name__)


class EngineManager(Manager):
    RPC_API_NAMESPACE = 'engine'
    RPC_API_VERSION = '1.0'
    target = messaging.Target(namespace=RPC_API_NAMESPACE, version=RPC_API_VERSION)

    def __init__(self):
        super(EngineManager, self).__init__()
        self.db_api = db_api.DbApi()

    def get_movie(self, ctx, uuid):
        LOG.info('Get movie {}'.format(uuid))
        movie_db = self.db_api.get_movie_by_uuid(uuid)
        return movie_db.as_dict()

    def get_all_movie(self, ctx, **kwargs):
        LOG.info('Get all movie')
        movies_db = self.db_api.get_all_movies()
        return [m.as_dict() for m in movies_db]

    def create_movie(self, ctx, **kwargs):
        movie_dict = kwargs['content_json']

        LOG.info('Add movie {}'.format(movie_dict))
        movie_dict['state'] = 'downloading'
        self.db_api.create_movie(movie_dict)

        movie_handler = MovieHandler()
        movie_handler.download(movie_dict['uuid'], movie_dict['url'])
        self.db_api.update_movie(movie_dict['uuid'], {'state': 'ready'})

    def update_movie(self, ctx, uuid, **kwargs):
        movie_dict = kwargs['content_json']

        LOG.info('Update movie {}'.format(movie_dict))
        self.db_api.update_movie(uuid, movie_dict)

    def delete_movie(self, ctx, uuid):
        LOG.info('Delete movie {}'.format(uuid))

        movie_handler = MovieHandler()
        movie_handler.remove(uuid)
        self.db_api.delete_movie_by_uuid(uuid)
