import oslo_messaging as messaging
from oslo_config import cfg

from pymsboot.context import RequestContext

_TRANSPORT = None


def get_transport():
    global _TRANSPORT

    if not _TRANSPORT:
        _TRANSPORT = messaging.get_rpc_transport(cfg.CONF)

    return _TRANSPORT


def get_serializer():
    serializer = PymsbootSerializer()
    return serializer


class PymsbootSerializer(messaging.Serializer):
    def __init__(self):
        pass

    def serialize_entity(self, context, entity):
        return entity

    def deserialize_entity(self, context, entity):
        return entity

    def serialize_context(self, context):
        return context.to_dict()

    def deserialize_context(self, context):
        return RequestContext.from_dict(context)
