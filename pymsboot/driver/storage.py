import time

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class MovieHandler():
    def __init__(self):
        pass

    def download(self, uuid, url):
        LOG.info('Start download movie {} from {}'.format(uuid, url))
        time.sleep(5)
        LOG.info('Finished download movie {} from {}'.format(uuid, url))

    def remove(self, uuid):
        LOG.info('Delete movie {}'.format(uuid))
        time.sleep(2)
        LOG.info('Finished to delete movie {}'.format(uuid))
