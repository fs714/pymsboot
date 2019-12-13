import oslo_messaging as messaging
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service

from pymsboot.engine.manager import EngineManager
from pymsboot.rpc import rpc
from pymsboot.services import periodics

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class EngineService(service.Service):
    def __init__(self):
        super(EngineService, self).__init__()
        self.topic = CONF.engine.topic
        self.server = CONF.engine.host

        self.workers = CONF.engine.engine_workers
        if self.workers is None or self.workers < 1:
            self.workers = processutils.get_worker_count()

        # Initial setup include databse, periodic tasks, etc
        LOG.info('Starting periodic tasks...')
        if CONF.engine.enable_periodic_task_01:
            periodics.start_periodic_task_01_handler()

        if CONF.engine.enable_periodic_task_02:
            periodics.start_periodic_task_02_handler()

    def start(self):
        super(EngineService, self).start()
        transport = rpc.get_transport()
        target = messaging.Target(topic=self.topic, server=self.server)
        endpoint = [EngineManager()]
        self.server = messaging.get_rpc_server(
            transport,
            target,
            endpoint,
            executor='eventlet'
        )

        LOG.info('Starting engine...')
        self.server.start()

    def stop(self, graceful=False):
        periodics.stop()

        if self.server:
            self.server.stop()
            self.server.wait()
        super(EngineService, self).stop(graceful)
