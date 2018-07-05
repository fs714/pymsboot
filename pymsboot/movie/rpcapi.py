import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import rpc

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class MovieClient(object):
    def __init__(self):
        self.namespace = 'movie'
        self.version = '1.0'
        target = messaging.Target(topic=CONF.engine.topic, namespace=self.namespace, version=self.version)
        self._client = messaging.RPCClient(rpc.get_transport(), target)

    def add(self, ctxt, movie):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'add_movie', movie=movie)

    def delete(self, ctxt, movie):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'delete_movie', movie=movie)

    def put(self, ctxt, movie):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(ctxt, 'put_movie', movie=movie)

    def get(self, ctxt, movie):
        """
        Get operation doesn't need RPC, this is just an example.
        """
        cctxt = self._client.prepare(version=self.version, fanout=False)
        return cctxt.call(ctxt, 'get_movie', movie=movie)
