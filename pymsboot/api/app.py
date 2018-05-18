import pecan
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot.services import periodics

LOG = logging.getLogger(__name__)


def get_pecan_config():
    # Set up the pecan configuration.
    opts = cfg.CONF.pecan

    cfg_dict = {
        "app": {
            "root": opts.root,
            "modules": opts.modules,
            "debug": opts.debug,
            "auth_enable": opts.auth_enable
        }
    }

    return pecan.configuration.conf_from_dict(cfg_dict)


def setup_app(config=None):
    if not config:
        config = get_pecan_config()
    app_conf = dict(config.app)

    # Initial setup include databse, periodic tasks, etc
    LOG.info('Starting periodic tasks...')
    if cfg.CONF.api.enable_periodic_task_01:
        periodics.start_periodic_task_01_handler()

    if cfg.CONF.api.enable_periodic_task_02:
        periodics.start_periodic_task_02_handler()

    app = pecan.make_app(
        app_conf.pop('root'),
        hooks=[],
        logging=getattr(config, 'logging', {}),
        **app_conf
    )

    return app
