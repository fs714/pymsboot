from sqlalchemy.ext.declarative import declarative_base


class PymsbootBase(object):
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
        return d


Base = declarative_base(cls=PymsbootBase)
