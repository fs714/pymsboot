import pecan
from oslo_log import log as logging
from wsme import types as wtypes

from pymsboot.api import expose
from pymsboot.api.controllers.v1 import root as v1_root

LOG = logging.getLogger(__name__)

API_STATUS = wtypes.Enum(str, 'SUPPORTED', 'CURRENT', 'DEPRECATED')


class APIVersion(wtypes.Base):
    """An API Version."""

    id = wtypes.text
    "The version identifier."

    status = API_STATUS
    "The status of the API (SUPPORTED, CURRENT or DEPRECATED)."

    links = [wtypes.text]
    "The link to the versioned API."

    @classmethod
    def sample(cls):
        return cls(
            id='v1.0',
            status='CURRENT',
            links='http://example.com:7070/v1'
        )


class RootController(object):
    v1 = v1_root.Controller()

    @expose.expose([APIVersion])
    def index(self):
        LOG.info("Fetching API versions.")

        host_url_v1 = '%s/%s' % (pecan.request.host_url, 'v1')
        api_v1 = APIVersion(
            id='v1.0',
            status='CURRENT',
            links=[host_url_v1]
        )

        return [api_v1]
