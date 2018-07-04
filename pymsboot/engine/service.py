import cotyledon
import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging
from oslo_messaging.rpc import dispatcher

from pymsboot.services import periodics

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class EngineService(cotyledon.Service):
    def __init__(self, worker_id):
        super(EngineService, self).__init__(worker_id)
        self.server = None

    def run(self):
        topic = CONF.engine.topic
        server = CONF.engine.host
        transport = messaging.get_rpc_transport(CONF)
        target = messaging.Target(topic=topic, server=server, fanout=False)
        endpoint = []
        access_policy = dispatcher.DefaultRPCAccessPolicy
        self.server = messaging.get_rpc_server(
            transport,
            target,
            [endpoint],
            executor='threading',
            access_policy=access_policy
        )

        # Initial setup include databse, periodic tasks, etc
        LOG.info('Starting periodic tasks...')
        if cfg.CONF.api.enable_periodic_task_01:
            periodics.start_periodic_task_01_handler()

        if cfg.CONF.api.enable_periodic_task_02:
            periodics.start_periodic_task_02_handler()

        LOG.info('Starting engine...')
        self.server.start()

    def terminate(self):
        periodics.stop()

        if self.server:
            LOG.info('Stopping engine...')
            self.server.stop()
            self.server.wait()
