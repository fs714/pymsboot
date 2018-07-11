from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Manager():
    def __init__(self):
        self.additional_endpoints = []
