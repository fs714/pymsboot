# python start_api.py --config-file=./conf/pymsboot.conf

import os
import subprocess
import sys

from oslo_config import cfg

from pymsboot import config

CONF = cfg.CONF


def start_uwsgi(argv):
    # uwsgi --http 0.0.0.0:9666 --wsgi-file ./ancc/cmd/api.py --callable application --processes 4 --threads 2 --stats 127.0.0.1:9191
    cmd = []
    cmd.append('uwsgi')
    cmd.append('--http')
    cmd.append(CONF.api.host + ':' + str(CONF.api.port))
    cmd.append('--wsgi-file')
    cmd.append('./pymsboot/cmd/api.py')
    cmd.append('--callable')
    cmd.append('application')
    cmd.append('--processes')
    if CONF.api.api_workers <= 1:
        p_num = os.cpu_count()
    else:
        p_num = CONF.api.api_workers
    cmd.append(str(p_num))
    cmd.append('--threads')
    cmd.append('2')
    cmd.append('--stats')
    cmd.append('0.0.0.0:9667')
    cmd.append('--pyargv')
    cmd.append(' '.join(argv))

    print(' '.join(cmd))
    subprocess.call(cmd)


if __name__ == '__main__':
    if sys.argv is None:
        argv = []
    else:
        argv = sys.argv[1:]
    config.parse_args(args=argv)
    start_uwsgi(argv)
