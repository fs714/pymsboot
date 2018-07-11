import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot.rpc import rpc

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
        serializer = rpc.get_serializer()
        self._client = messaging.RPCClient(rpc.get_transport(), target, serializer=serializer)

    def create_movie(self, context, movie_obj):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'create_movie', movie_obj=movie_obj)

    def update_movie(self, context, movie_obj):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'update_movie', movie_obj=movie_obj)

    def delete_movie(self, context, movie_id):
        cctxt = self._client.prepare(version=self.version, fanout=False)
        cctxt.cast(context, 'delete_movie', movie_id=movie_id)

    # Versioned Objects indirection API
    def object_class_action(self, context, objname, objmethod, objver, args, kwargs):
        cctxt = self._client.prepare(version=self.version, namespace='indirection', fanout=False)
        return cctxt.call(context, 'object_class_action', objname=objname, objmethod=objmethod,
                          objver=objver, args=args, kwargs=kwargs)

    def object_action(self, context, objinst, objmethod, args, kwargs):
        cctxt = self._client.prepare(version=self.version, namespace='indirection', fanout=False)
        return cctxt.call(context, 'object_action', objinst=objinst, objmethod=objmethod, args=args, kwargs=kwargs)

    def object_backport(self, context, objinst, target_version):
        cctxt = self._client.prepare(version=self.version, namespace='indirection', fanout=False)
        return cctxt.call(context, 'object_backport', objinst=objinst, target_version=target_version)
