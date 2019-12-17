import eventlet

eventlet.monkey_patch()

import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service

from pymsboot.api import service as api_service
from pymsboot import config

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def prepare_service(argv):
    _DEFAULT_LOG_LEVELS = [
        'eventlet.wsgi.server=WARN',
        'oslo_service.periodic_task=INFO',
        'oslo_service.loopingcall=INFO',
        'oslo_concurrency.lockutils=WARN',
        'urllib3.connectionpool=CRITICAL',
        'futurist.periodics=WARN',
        'flask=INFO',
        'werkzeug=INFO'
    ]
    default_log_levels = logging.get_default_log_levels()
    default_log_levels.extend(_DEFAULT_LOG_LEVELS)
    logging.set_defaults(default_log_levels=default_log_levels)

    logging.register_options(CONF)
    config.parse_args(args=argv)
    logging.setup(CONF, 'pymsboot_api')


def main():
    try:
        if sys.argv is None:
            argv = []
        else:
            argv = sys.argv[1:]
        prepare_service(argv)

        LOG.info('Start API Server')
        api_server = api_service.WSGIService()
        launcher = service.launch(CONF, api_server, workers=api_server.workers)
        launcher.wait()
    except RuntimeError as excp:
        sys.stderr.write("ERROR: %s\n" % excp)
        sys.exit(1)


if __name__ == '__main__':
    main()
