from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Manager():
    def __init__(self):
        self.additional_endpoints = []

    def init_host(self):
        """
        A hook point for services to execute tasks before the services are made
        available (i.e. showing up on RPC and starting to accept RPC calls) to
        other components. Child classes should override this method.
        """
        pass
