from oslo_versionedobjects import base as ovoo_base
from oslo_versionedobjects import fields as ovoo_fields

remotable_classmethod = ovoo_base.remotable_classmethod
remotable = ovoo_base.remotable


class PymsbootObjectRegistry(ovoo_base.VersionedObjectRegistry):
    pass


class PymsbootObject(ovoo_base.VersionedObject):
    """Base class and object factory.

    This forms the base of all objects that can be remoted or instantiated
    via RPC. Simply defining a class that inherits from this base class
    will make it remotely instantiatable. Objects should implement the
    necessary "get" classmethod routines as well as "save" object methods
    as appropriate.
    """

    OBJ_SERIAL_NAMESPACE = 'pymsboot_object'
    OBJ_PROJECT_NAMESPACE = 'pymsboot'

    def as_dict(self):
        return {k: getattr(self, k)
                for k in self.fields
                if self.obj_attr_is_set(k)}


class PymsbootObjectDictCompat(ovoo_base.VersionedObjectDictCompat):
    pass


class PymsbootPersistentObject():
    """Mixin class for Persistent objects.

    This adds the fields that we use in common for all persistent objects.
    """
    fields = {
        'created_at': ovoo_fields.DateTimeField(nullable=True),
        'updated_at': ovoo_fields.DateTimeField(nullable=True),
    }


class PymsbootObjectIndirectionAPI(ovoo_base.VersionedObjectIndirectionAPI):
    def __init__(self):
        super(PymsbootObjectIndirectionAPI, self).__init__()
        from pymsboot.engine import rpcapi as engine_rpcapi
        self._engineer = engine_rpcapi.get_engine_rpc_client()

    def object_action(self, context, objinst, objmethod, args, kwargs):
        return self._engineer.object_action(context, objinst, objmethod, args, kwargs)

    def object_class_action(self, context, objname, objmethod, objver, args, kwargs):
        return self._engineer.object_class_action(context, objname, objmethod, objver, args, kwargs)

    def object_backport(self, context, objinst, target_version):
        return self._engineer.object_backport(context, objinst, target_version)


class PymsbootObjectSerializer(ovoo_base.VersionedObjectSerializer):
    # Base class to use for object hydration
    OBJ_BASE_CLASS = PymsbootObject
