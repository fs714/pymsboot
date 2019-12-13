from sqlalchemy import create_engine, inspect
from pymsboot.db import models
from pymsboot.db.tables.movie import *

# CONN_STR = 'postgres://knight:8pPvp3HjoB3ePpKOBAdBssSUCUAuMPd8sSr6J3tRD14=@axesdn-db-dev.crtxlghyjpby.rds.cn-north-1.amazonaws.com.cn:5432/aosdb_dev'
CONN_STR = 'postgres://user:addr:5432/dbname'


def main():
    engine = create_engine(CONN_STR)
    models.Base.metadata.create_all(engine)

    # check table exists
    ins = inspect(engine)
    for _t in ins.get_table_names():
        print(_t)


if __name__ == '__main__':
    main()
