import oslo_messaging as messaging
from oslo_config import cfg

from pymsboot import context as pymsboot_context
from pymsboot.objects import base

_TRANSPORT = None


def get_transport():
    global _TRANSPORT

    if not _TRANSPORT:
        _TRANSPORT = messaging.get_rpc_transport(cfg.CONF)

    return _TRANSPORT


def get_serializer():
    serializer = RequestContextSerializer(base.PymsbootObjectSerializer())
    return serializer


class RequestContextSerializer(messaging.Serializer):

    def __init__(self, base):
        self._base = base

    def serialize_entity(self, context, entity):
        if not self._base:
            return entity
        return self._base.serialize_entity(context, entity)

    def deserialize_entity(self, context, entity):
        if not self._base:
            return entity
        return self._base.deserialize_entity(context, entity)

    def serialize_context(self, context):
        return context.to_dict()

    def deserialize_context(self, context):
        return pymsboot_context.RequestContext.from_dict(context)
