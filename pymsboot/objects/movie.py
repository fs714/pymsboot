from oslo_log import log as logging
from oslo_versionedobjects import fields as object_fields

from pymsboot.db.api import get_connection
from pymsboot.objects import base

LOG = logging.getLogger(__name__)


@base.PymsbootObjectRegistry.register
class Movie(base.PymsbootObject, base.PymsbootPersistentObject, base.PymsbootObjectDictCompat):
    VERSION = '1.0'
    dbapi = get_connection()

    fields = {
        'id': object_fields.StringField(nullable=False),
        'name': object_fields.StringField(nullable=True),
        'rank': object_fields.IntegerField(nullable=True),
        'url': object_fields.StringField(nullable=True),
        'state': object_fields.StringField(nullable=True),
    }

    @staticmethod
    def _from_db_object(movie_obj, movie_db):
        """Converts a database entity to a formal object."""
        for field in movie_obj.fields:
            try:
                value = getattr(movie_db, field)
            except AttributeError:
                continue
            except ValueError:
                value = None
            movie_obj[field] = value

        movie_obj.obj_reset_changes()
        return movie_obj

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Movie._from_db_object(cls(context), obj) for obj in db_objects]

    @base.remotable_classmethod
    def get_by_id(cls, context, id):
        """Find a movie based on its uuid and return a movie object."""
        LOG.info('Getting movie {} {}.'.format(id, context))
        movie_db = cls.dbapi.get_movie_by_id(id)
        if movie_db:
            movie_obj = Movie._from_db_object(cls(context), movie_db)
            return movie_obj
        else:
            return None

    @base.remotable_classmethod
    def get_all(cls, context):
        """Find a movie based on its uuid and return a movie object."""
        LOG.info('Getting movies.')
        movies_db = cls.dbapi.get_all_movies()
        movies_obj = Movie._from_db_object_list(movies_db, cls, context)
        return movies_obj

    @base.remotable
    def create(self, context):
        """Create a Movie record in the DB."""
        LOG.info('Create movie {} {}.'.format(self.id, context))
        values = self.obj_get_changes()
        db_cluster = self.dbapi.create_movie(values)
        movie_obj = self._from_db_object(self, db_cluster)
        return movie_obj

    @base.remotable
    def update(self, context):
        """Update Movie record in the DB."""
        LOG.info('Update movie {} {}.'.format(self.id, context))
        updates = self.obj_get_changes()
        self.dbapi.update_movie(self.id, updates)
        self.obj_reset_changes()

    @base.remotable_classmethod
    def delete(cls, context, id):
        """Delete a Movie record in the DB."""
        LOG.info('Delete movie {} {}'.format(id, context))
        cls.dbapi.delete_movie_by_id(id)
