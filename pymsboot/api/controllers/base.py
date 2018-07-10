import datetime

import wsme
from wsme import types as wtypes


class APIBase(wtypes.Base):
    created_at = wsme.wsattr(datetime.datetime, readonly=True)
    """The time in UTC at which the object is created"""

    updated_at = wsme.wsattr(datetime.datetime, readonly=True)
    """The time in UTC at which the object is updated"""

    _wsme_attributes = []

    def as_dict(self):
        d = {}
        for attr in self._wsme_attributes:
            attr_val = getattr(self, attr.name)
            if not isinstance(attr_val, wtypes.UnsetType):
                d[attr.name] = attr_val
        return d
