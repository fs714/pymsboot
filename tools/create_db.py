import sys
sys.path.append('../')

from sqlalchemy import create_engine, inspect

from pymsboot.db import models
from pymsboot.db.tables.movie import *

CONN_STR = 'postgres://pymsboot:pymsboot@127.0.0.1:5432/pymsboot'


def main():
    engine = create_engine(CONN_STR)
    models.Base.metadata.create_all(engine)

    # check table exists
    ins = inspect(engine)
    for _t in ins.get_table_names():
        print(_t)


if __name__ == '__main__':
    main()
