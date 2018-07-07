import eventlet

eventlet.monkey_patch()

import sys

from oslo_config import cfg
from oslo_log import log as logging
from oslo_service import service

from pymsboot import config
from pymsboot.db.api import db_setup
from pymsboot.engine import service as engine_service

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
        LOG.info('Start Engine Server')

        db_setup()

        engine_server = engine_service.RPCService()
        launcher = service.launch(CONF, engine_server, workers=engine_server.workers)
        launcher.wait()
    except RuntimeError as excp:
        sys.stderr.write("ERROR: %s\n" % excp)
        sys.exit(1)


if __name__ == '__main__':
    main()
