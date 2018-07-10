from oslo_versionedobjects import base as object_base
from oslo_versionedobjects import fields as object_fields


class PymsbootObject(object_base.VersionedObject):
    """Base class and object factory.

    This forms the base of all objects that can be remoted or instantiated
    via RPC. Simply defining a class that inherits from this base class
    will make it remotely instantiatable. Objects should implement the
    necessary "get" classmethod routines as well as "save" object methods
    as appropriate.
    """

    OBJ_PROJECT_NAMESPACE = 'pymsboot'

    fields = {
        'created_at': object_fields.DateTimeField(nullable=True),
        'updated_at': object_fields.DateTimeField(nullable=True),
    }

    def as_dict(self):
        """Return the object represented as a dict.

        The returned object is JSON-serialisable.
        """

        def _attr_as_dict(field):
            """Return an attribute as a dict, handling nested objects."""
            attr = getattr(self, field)
            if isinstance(attr, PymsbootObject):
                attr = attr.as_dict()
            return attr

        return dict((k, _attr_as_dict(k)) for k in self.fields if self.obj_attr_is_set(k))

    def _set_from_db_object(self, db_object, fields=None):
        """Sets object fields.

        :param db_object: A DB entity of the object
        :param fields: list of fields to set on obj from db_object.
        """
        fields = fields or self.fields
        for field in fields:
            setattr(self, field, db_object[field])

    @staticmethod
    def _from_db_object(obj, db_object, fields=None):
        """Converts a database entity to a formal object.

        :param obj: An object of the class.
        :param db_object: A DB entity of the object
        :param fields: list of fields to set on obj from db_object.
        :return: The object of the class
        """
        obj._set_from_db_object(db_object, fields)

        # NOTE(rloo). We now have obj, a versioned object that corresponds to
        # its DB representation. A versioned object has an internal attribute
        # ._changed_fields; this is a list of changed fields -- used, e.g.,
        # when saving the object to the DB (only those changed fields are
        # saved to the DB). The obj.obj_reset_changes() clears this list
        # since we didn't actually make any modifications to the object that
        # we want saved later.
        obj.obj_reset_changes()

        return obj

    @classmethod
    def _from_db_object_list(cls, db_objects):
        """Returns objects corresponding to database entities.

        Returns a list of formal objects of this class that correspond to
        the list of database entities.

        :param cls: the VersionedObject class of the desired object
        :param db_objects: A  list of DB models of the object
        :returns: A list of objects corresponding to the database entities
        """
        return [cls._from_db_object(cls(), db_obj) for db_obj in db_objects]
