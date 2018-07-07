import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import rpc

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

_MOVIE_RPC_CLIENT = None


def get_movie_rpc_client():
    global _MOVIE_RPC_CLIENT
    if _MOVIE_RPC_CLIENT is not None:
        return _MOVIE_RPC_CLIENT

    _MOVIE_RPC_CLIENT = MovieClient()
    return _MOVIE_RPC_CLIENT


class MovieClient(object):
    def __init__(self):
        self.namespace = 'movie'
        self.version = '1.0'
        target = messaging.Target(topic=CONF.engine.topic, namespace=self.namespace, version=self.version)
        self._client = messaging.RPCClient(rpc.get_transport(), target)

    def add(self, ctxt, movie_dict):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'add_movie', movie_dict=movie_dict)

    def delete(self, ctxt, movie_id):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'delete_movie', movie_id=movie_id)

    def put(self, ctxt, movie_id, url):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'update_movie', movie_id=movie_id, url=url)

    def get(self, ctxt, movie_id):
        """
        Get operation doesn't need RPC, this is just an example.
        """
        cctxt = self._client.prepare(version=self.version, fanout=False)
        return cctxt.call(ctxt, 'get_movie', movie_id=movie_id)

    def get_all(self, ctxt):
        """
        Get all operation doesn't need RPC, this is just an example.
        """
        cctxt = self._client.prepare(version=self.version, fanout=False)
        return cctxt.call(ctxt, 'get_all_movies')
