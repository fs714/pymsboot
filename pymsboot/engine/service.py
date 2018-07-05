import cotyledon
import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import rpc
from pymsboot.movie.manager import MovieManager
from pymsboot.services import periodics

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class EngineService(cotyledon.Service):
    def __init__(self, worker_id):
        super(EngineService, self).__init__(worker_id)
        self.topic = CONF.engine.topic
        self.server = CONF.engine.host

        # Initial setup include databse, periodic tasks, etc
        LOG.info('Starting periodic tasks...')
        if cfg.CONF.api.enable_periodic_task_01:
            periodics.start_periodic_task_01_handler()

        if cfg.CONF.api.enable_periodic_task_02:
            periodics.start_periodic_task_02_handler()

    def run(self):
        transport = rpc.get_transport()
        target = messaging.Target(topic=self.topic, server=self.server)
        endpoint = [MovieManager()]
        self.server = messaging.get_rpc_server(
            transport,
            target,
            endpoint,
            executor='threading'
        )

        LOG.info('Starting engine...')
        self.server.start()

    def terminate(self):
        periodics.stop()

        if self.server:
            LOG.info('Stopping engine...')
            self.server.stop()
            self.server.wait()
