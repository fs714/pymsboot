import sys

import cotyledon
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import config
from pymsboot import rpc
from pymsboot.engine import service as engine_service

CONF = cfg.CONF


def main():
    try:
        if sys.argv is None:
            argv = []
        else:
            argv = sys.argv[1:]
        config.parse_args(args=argv)
        logging.setup(CONF, 'pymsboot')

        workers = CONF.engine.engine_workers
        if workers is None or workers < 1:
            workers = processutils.get_worker_count()

        rpc.get_transport()
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
