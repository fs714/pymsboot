import pecan
from oslo_log import log as logging
from oslo_utils import uuidutils
from pecan import rest
from wsme import Unset
from wsme import types as wtypes

from pymsboot import objects
from pymsboot.api import expose
from pymsboot.api.controllers import base

LOG = logging.getLogger(__name__)


class Movie(base.APIBase):
    """An Movie."""

    id = wtypes.text
    "The movie identifier."

    name = wtypes.text
    "The movie name."

    rank = int
    "The movie rank in system."

    url = wtypes.text
    "The movie download url."

    state = wtypes.text
    "The movie state."


class MoviesController(rest.RestController):
    @expose.expose([Movie])
    def get(self):
        LOG.info('Get all movies.')
        movie_objs = objects.Movie.get_all(context=pecan.request.context)
        return [Movie(**m.as_dict()) for m in movie_objs]

    @expose.expose(wtypes.text, body=Movie, status_code=201)
    def post(self, movie):
        LOG.info('Add a movie')
        if movie.id == Unset:
            movie.id = uuidutils.generate_uuid()
        if movie.state == Unset:
            movie.state = None
        movie_obj = objects.Movie(**movie.as_dict())
        pecan.request.rpcapi.create_movie(context=pecan.request.context, movie_obj=movie_obj)
        return 'Download In Progress'

    @pecan.expose()
    def _lookup(self, movie_id, *remainder):
        return MovieController(movie_id), remainder


class MovieController(rest.RestController):
    def __init__(self, movie_id):
        self.movie_id = movie_id

    @expose.expose(Movie)
    def get(self):
        LOG.info('Get movie {}.'.format(self.movie_id))
        movie_obj = objects.Movie.get_by_id(context=pecan.request.context, id=self.movie_id)
        if movie_obj:
            return Movie(**movie_obj.as_dict())
        else:
            return None

    @expose.expose(wtypes.text, body=Movie)
    def put(self, movie):
        LOG.info('Update movie {}.'.format(self.movie_id))
        movie_obj = objects.Movie.get_by_id(context=pecan.request.context, id=self.movie_id)
        # Update only the fields that have changed
        for field in objects.Movie.fields:
            if getattr(movie, field) == wtypes.Unset:
                continue
            if getattr(movie, field) != movie_obj[field]:
                movie_obj[field] = getattr(movie, field)
        pecan.request.rpcapi.update_movie(context=pecan.request.context, movie_obj=movie_obj)
        return 'Update In Progress'

    @expose.expose(wtypes.text)
    def delete(self):
        LOG.info('Deleting movie {}.'.format(self.movie_id))
        pecan.request.rpcapi.delete_movie(context=pecan.request.context, movie_id=self.movie_id)
        return 'Delete In Progress'
