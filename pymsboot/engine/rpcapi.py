import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot.rpc import rpc

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

_ENGINE_RPC_CLIENT = None


def get_engine_rpc_client():
    global _ENGINE_RPC_CLIENT
    if _ENGINE_RPC_CLIENT is not None:
        return _ENGINE_RPC_CLIENT

    _ENGINE_RPC_CLIENT = EngineClient()
    return _ENGINE_RPC_CLIENT


class EngineClient(object):
    def __init__(self):
        self.namespace = 'engine'
        self.version = '1.0'
        target = messaging.Target(topic=CONF.engine.topic, namespace=self.namespace, version=self.version)
        self._client = messaging.RPCClient(rpc.get_transport(), target, serializer=rpc.get_serializer())

    def get_movie(self, context, **kwargs):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        LOG.info(context)
        cctxt.call(context, 'get_movie', kwargs)

    def get_all_movie(self, context, **kwargs):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        return cctxt.call(context, 'get_all_movie', **kwargs)

    def create_movie(self, context, **kwargs):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'create_movie', kwargs)

    def update_movie(self, context, **kwargs):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'update_movie', kwargs)

    def delete_movie(self, context, movie_uuid):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'delete_movie', movie_uuid=movie_uuid)
