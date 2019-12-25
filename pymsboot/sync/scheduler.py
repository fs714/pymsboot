import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def task_one(a, b, c):
    time.sleep(1)
    LOG.info('task_one a = {}, b = {}, c = {}'.format(a, b, c))
    return a + b + c


def periodic_task_one():
    print('periodic_task_one on {}'.format(datetime.now()))
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_dict = {}
        for i in range(0, 20):
            future = executor.submit(task_one, i, i * 10, i * 100)
            future_dict[future] = i

        for f in as_completed(future_dict):
            LOG.info('Index: {}, result: {}'.format(str(future_dict[f]), str(f.result())))


def periodic_task_two():
    LOG.info('periodic_task_two on {}'.format(datetime.now()))


def periodic_task_three():
    LOG.info('periodic_task_three on {}'.format(datetime.now()))


executors = {
    'default': ProcessPoolExecutor(max_workers=3)
}
scheduler = BlockingScheduler()
scheduler.configure(executors=executors)

scheduler.add_job(periodic_task_one, 'interval', seconds=2)
scheduler.add_job(periodic_task_two, 'interval', seconds=5)
scheduler.add_job(periodic_task_three, 'interval', seconds=10)
