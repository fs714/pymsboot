import oslo_messaging as messaging
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service

from pymsboot import rpc
from pymsboot.movie.manager import MovieManager
from pymsboot.services import periodics

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class RPCService(service.Service):
    def __init__(self):
        super(RPCService, self).__init__()
        self.topic = CONF.engine.topic
        self.server = CONF.engine.host

        self.workers = CONF.api.api_workers
        if self.workers is None or self.workers < 1:
            self.workers = processutils.get_worker_count()

        # Initial setup include databse, periodic tasks, etc
        LOG.info('Starting periodic tasks...')
        if CONF.engine.enable_periodic_task_01:
            periodics.start_periodic_task_01_handler()

        if CONF.engine.enable_periodic_task_02:
            periodics.start_periodic_task_02_handler()

    def start(self):
        super(RPCService, self).start()
        transport = rpc.get_transport()
        target = messaging.Target(topic=self.topic, server=self.server)
        endpoint = [MovieManager()]
        self.server = messaging.get_rpc_server(
            transport,
            target,
            endpoint,
            executor='eventlet'
        )

        LOG.info('Starting engine...')
        self.server.start()

    def stop(self, graceful=True):
        periodics.stop()

        try:
            self.server.stop()
            self.server.wait()
        except Exception as e:
            LOG.exception('Service error occurred when stopping the RPC server. Error: %s', e)

        super(RPCService, self).stop(graceful=graceful)
        LOG.info('Stopped RPC server for service %(service)s on host %(host)s.',
                 {'service': self.topic, 'host': self.host})
