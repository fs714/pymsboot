from oslo_context import context


class RequestContext(context.RequestContext):
    pass


def make_context(*args, **kwargs):
    return RequestContext(*args, **kwargs)
