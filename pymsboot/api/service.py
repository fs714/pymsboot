from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service
from oslo_service import wsgi

from pymsboot.api import app

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class WSGIService(service.ServiceBase):
    """Provides ability to launch API from wsgi app."""

    def __init__(self):
        self.app = app.setup_app()

        self.workers = CONF.api.api_workers
        if self.workers is not None and self.workers < 1:
            LOG.warning(
                "Value of config option api_workers must be integer "
                "greater than 1.  Input value ignored."
            )
            self.workers = None
        self.workers = self.workers or processutils.get_worker_count()

        self.server = wsgi.Server(
            cfg.CONF,
            "pymsboot_api",
            self.app,
            host=cfg.CONF.api.host,
            port=cfg.CONF.api.port,
            use_ssl=False
        )

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def wait(self):
        self.server.wait()

    def reset(self):
        self.server.reset()
