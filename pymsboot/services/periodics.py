import threading

from futurist import periodics
from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
_periodic_tasks = {}


@periodics.periodic(5)
def periodic_task_01(msg):
    LOG.info('Function periodic_task_01 running with {}'.format(msg))


@periodics.periodic(10)
def periodic_task_02(msg):
    LOG.info('Function periodic_task_02 running with {}'.format(msg))


def start_periodic_task_01_handler():
    worker = periodics.PeriodicWorker([])
    worker.add(
        periodic_task_01,
        msg='666'
    )
    _periodic_tasks['periodic_task_01'] = worker

    thread = threading.Thread(target=worker.start)
    thread.setDaemon(True)
    thread.start()

    LOG.info('Service periodic_task_01 started.')


def start_periodic_task_02_handler():
    worker = periodics.PeriodicWorker([])
    worker.add(
        periodic_task_02,
        msg='999'
    )
    _periodic_tasks['periodic_task_02'] = worker

    thread = threading.Thread(target=worker.start)
    thread.setDaemon(True)
    thread.start()

    LOG.info('Service periodic_task_02 started.')


def stop(task=None):
    if not task:
        for name, worker in _periodic_tasks.items():
            LOG.info('Stopping periodic task: %s', name)
            worker.stop()
            del _periodic_tasks[name]
    else:
        worker = _periodic_tasks.get(task)
        if worker:
            LOG.info('Stopping periodic task: %s', task)
            worker.stop()
            del _periodic_tasks[task]
