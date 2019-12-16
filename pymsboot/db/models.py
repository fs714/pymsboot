from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PymsbootBase(Base):
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d
