from sqlalchemy import create_engine, inspect
from pymsboot.db import models
from pymsboot.db.tables.movie import *

# CONN_STR = 'postgres://knight:8pPvp3HjoB3ePpKOBAdBssSUCUAuMPd8sSr6J3tRD14=@axesdn-db-dev.crtxlghyjpby.rds.cn-north-1.amazonaws.com.cn:5432/aosdb_dev'
CONN_STR = 'postgres://user:addr:5432/dbname'

engine = create_engine(CONN_STR)

def cleanup_tables():
    for tbl in reversed(models.Base.metadata.sorted_tables):
        engine.execute(tbl.delete())

def drop_all_tables():
    models.Base.metadata.drop_all(engine)

def list_tables():
    # check table exists
    ins = inspect(engine)
    for _t in ins.get_table_names():
        print(_t)


def main():
    cleanup_tables()
    drop_all_tables()
    list_tables()


if __name__ == '__main__':
    main()
