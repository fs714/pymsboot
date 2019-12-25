import sys

from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import config
from pymsboot.sync.scheduler import scheduler

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def main():
    if sys.argv is None:
        argv = []
    else:
        argv = sys.argv[1:]

    logging.register_options(CONF)
    logging.set_defaults(default_log_levels=logging.get_default_log_levels())

    config.parse_args(args=argv)

    logging.setup(CONF, 'pymsboot_sync')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
