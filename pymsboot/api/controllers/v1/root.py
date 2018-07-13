import pecan
from wsme import types as wtypes

from pymsboot.api import expose
from pymsboot.api.controllers.v1 import movie as v1_movie


class RootResource(wtypes.Base):
    """Root resource for API version 1.

    It references all other resources belonging to the API.
    """
    url = wtypes.text


class Controller(object):
    """API root controller for version 1."""
    movies = v1_movie.MoviesController()

    @expose.expose(RootResource)
    def index(self):
        return RootResource(url='%s/%s' % (pecan.request.host_url, 'v1'))
