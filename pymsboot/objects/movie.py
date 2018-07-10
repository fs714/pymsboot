from oslo_log import log as logging
from oslo_versionedobjects import fields as object_fields

from pymsboot.db.api import get_connection
from pymsboot.objects.base import PymsbootObject

LOG = logging.getLogger(__name__)


class Movie(PymsbootObject):
    dbapi = get_connection()

    fields = {
        'id': object_fields.UUIDField(nullable=False),
        'name': object_fields.StringField(nullable=True),
        'rank': object_fields.IntegerField(nullable=True),
        'url': object_fields.StringField(nullable=True),
        'state': object_fields.StringField(nullable=True),
    }

    @classmethod
    def get_by_id(cls, id):
        """Find a movie based on its uuid and return a movie object."""

        LOG.info('Getting movie {}.'.format(id))
        movie_db = cls.dbapi.get_movie_by_id(id)
        movie_obj = cls._from_db_object(cls(), movie_db)
        return movie_obj

    @classmethod
    def get_all(cls):
        """Find a movie based on its uuid and return a movie object."""

        LOG.info('Getting movies.')
        movies_db = cls.dbapi.get_all_movies()
        movies_obj = cls._from_db_object_list(movies_db)
        return movies_obj

    @classmethod
    def create(cls, movie_dict):
        """Create a Movie record in the DB."""
        LOG.info('Create movie from {}.'.format(movie_dict))
        movie = Movie(**movie_dict)
        cls.dbapi.add_movie(movie)

    @classmethod
    def update_state(cls, id, state):
        """Update state for a Movie record in the DB."""
        LOG.info('Update movie {} state to {}'.format(id, state))
        cls.dbapi.update_movie_state(id, state)

    @classmethod
    def update_url(cls, id, url):
        """Update url for a Movie record in the DB."""
        LOG.info('Update movie {} url to {}'.format(id, url))
        cls.dbapi.update_movie_url(id, url)

    @classmethod
    def delete(cls, id):
        """Delete a Movie record in the DB."""
        LOG.info('Delete movie {}'.format(id))
        cls.dbapi.delete_movie_by_id(id)
