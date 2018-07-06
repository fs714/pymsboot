import pecan
from oslo_log import log as logging
from pecan import rest
from wsme import types as wtypes

from pymsboot.api import expose
from pymsboot.movie.rpcapi import get_movie_rpc_client

LOG = logging.getLogger(__name__)


class Movie(wtypes.Base):
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rank': self.rank,
            'url': self.url,
            'state': self.state,
        }


class MoviesController(rest.RestController):
    @expose.expose([Movie])
    def get(self):
        LOG.info('Getting movies.')
        movies = get_movie_rpc_client().get_all(ctxt={})
        return [Movie(**m) for m in movies]

    @expose.expose(wtypes.text, body=Movie, status_code=201)
    def post(self, movie):
        LOG.info('Adding a new movie')
        get_movie_rpc_client().add(ctxt={}, movie_dict=movie.to_dict)
        return 'Download In Progress'

    @pecan.expose()
    def _lookup(self, movie_id, *remainder):
        return MovieController(movie_id), remainder


class MovieController(rest.RestController):
    def __init__(self, movie_id):
        self.movie_id = movie_id

    @expose.expose(Movie)
    def get(self):
        LOG.info('Getting movie {}.'.format(self.movie_id))
        movie = get_movie_rpc_client().get(ctxt={}, movie_id=self.movie_id)
        return movie

    @expose.expose(wtypes.text, body=Movie)
    def put(self, movie):
        LOG.info('Updating movie {}.'.format(self.movie_id))
        get_movie_rpc_client().put(ctxt={}, movie_id=self.movie_id, url=movie.url)
        return 'Update In Progress'

    @expose.expose(wtypes.text)
    def delete(self):
        LOG.info('Deleting movie {}.'.format(self.movie_id))
        get_movie_rpc_client().delete(ctxt={}, movie_id=self.movie_id)
        return 'Delete In Progress'
