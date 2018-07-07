import sys

import cotyledon
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging

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

        workers = CONF.engine.engine_workers
        if workers is None or workers < 1:
            workers = processutils.get_worker_count()

        sm = cotyledon.ServiceManager()
        sm.add(
            engine_service.EngineService,
            workers=workers
        )
        sm.run()
    except RuntimeError as excp:
        sys.stderr.write("ERROR: %s\n" % excp)
        sys.exit(1)


if __name__ == '__main__':
    main()
