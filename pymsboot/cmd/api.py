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


def main():
    try:
        if sys.argv is None:
            argv = []
        else:
            argv = sys.argv[1:]
        config.parse_args(args=argv)
        logging.setup(CONF, 'pymsboot')
        LOG.info('Start API Server')

        api_server = api_service.WSGIService()
        launcher = service.launch(CONF, api_server, workers=api_server.workers)
        launcher.wait()
    except RuntimeError as excp:
        sys.stderr.write("ERROR: %s\n" % excp)
        sys.exit(1)


if __name__ == '__main__':
    main()
