import pecan
from oslo_log import log as logging
from pecan import rest
from wsme import types as wtypes

from pymsboot.api import expose

LOG = logging.getLogger(__name__)

MOVIES_DB = [
    {
        'id': 'e00cbfb3-ae3a-469d-955d-eea64c27c7af',
        'name': 'Titanic',
        'director': 'James Cameron',
        'actors': [
            'Leonardo DiCaprio',
            'Kate Winslet'
        ]
    },
    {
        'id': 'c840f0b6-0d28-4c0c-abaa-f96dca76c057',
        'name': 'Your Name',
        'director': 'Makoto Shinkai',
        'actors': [
            'Taki Tachibana',
            'Mitsuha Miyamizu'
        ]
    }
]


class Movie(wtypes.Base):
    """An Movie."""

    id = wtypes.text
    "The movie identifier."

    name = wtypes.text
    "The movie name."

    director = wtypes.text
    "The movie director."

    actors = [wtypes.text]
    "The movie actors."

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'actors': self.actors
        }


class MovieController(rest.RestController):
    def __init__(self, movie_id):
        self.movie_id = movie_id

    @expose.expose(Movie)
    def get(self):
        LOG.info('Getting movie {}.'.format(self.movie_id))
        for m in MOVIES_DB:
            if m['id'] == self.movie_id:
                return Movie(**m)
        return None

    @expose.expose(wtypes.text, body=Movie)
    def put(self, movie):
        LOG.info('Updating movie {}.'.format(self.movie_id))
        for m in MOVIES_DB:
            if m['id'] == self.movie_id:
                m['name'] = movie.name
                m['director'] = movie.director
                m['actors'] = movie.actors
        return 'Update Success'

    @expose.expose(wtypes.text)
    def delete(self):
        LOG.info('Deleting movie {}.'.format(self.movie_id))
        global MOVIES_DB
        MOVIES_DB = [m for m in MOVIES_DB if m['id'] != self.movie_id]
        return 'Delete Success'


class MoviesController(rest.RestController):
    @expose.expose([Movie])
    def get(self):
        LOG.info('Getting movies.')
        return [Movie(**m) for m in MOVIES_DB]

    @expose.expose(None, body=Movie, status_code=201)
    def post(self, movie):
        LOG.info('Adding a new movie')
        MOVIES_DB.append(movie.to_dict())

    @pecan.expose()
    def _lookup(self, movie_id, *remainder):
        return MovieController(movie_id), remainder
