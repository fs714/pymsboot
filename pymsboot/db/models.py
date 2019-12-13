from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base


class PymsbootBase(models.ModelBase):
    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

    def save(self, session=None):
        import pymsboot.db.api as db_api

        if session is None:
            session = db_api.get_session()

        super(PymsbootBase, self).save(session)


Base = declarative_base(cls=PymsbootBase)
