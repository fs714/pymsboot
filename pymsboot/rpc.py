import oslo_messaging as messaging
from oslo_config import cfg

_TRANSPORT = None
_ENGINE_CLIENT = None


def get_transport():
    global _TRANSPORT

    if not _TRANSPORT:
        _TRANSPORT = messaging.get_rpc_transport(cfg.CONF)

    return _TRANSPORT
