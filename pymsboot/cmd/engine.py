import eventlet

eventlet.monkey_patch()

import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service

from pymsboot import config
from pymsboot.db.api import db_setup
from pymsboot.rpc import service as rpc_service

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def prepare_service(argv):
    _DEFAULT_LOG_LEVELS = [
        'eventlet.wsgi.server=WARN',
        'oslo_service.periodic_task=INFO',
        'oslo_service.loopingcall=INFO',
        'oslo_db=WARN',
        'oslo_concurrency.lockutils=WARN',
        'keystoneclient=INFO',
        'requests.packages.urllib3.connectionpool=CRITICAL',
        'urllib3.connectionpool=CRITICAL',
        'cotyledon=INFO',
        'futurist.periodics=WARN'
    ]
    default_log_levels = logging.get_default_log_levels()
    default_log_levels.extend(_DEFAULT_LOG_LEVELS)
    logging.set_defaults(default_log_levels=default_log_levels)

    logging.register_options(CONF)
    config.parse_args(args=argv)
    logging.setup(CONF, 'pymsboot')


def main():
    try:
        if sys.argv is None:
            argv = []
        else:
            argv = sys.argv[1:]
        prepare_service(argv)
        LOG.info('Start Engine Server')

        db_setup()

        engine_server = rpc_service.EngineService()
        launcher = service.launch(CONF, engine_server, workers=engine_server.workers)
        launcher.wait()
    except RuntimeError as excp:
        sys.stderr.write("ERROR: %s\n" % excp)
        sys.exit(1)


if __name__ == '__main__':
    main()
