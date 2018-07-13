from pecan import hooks

from pymsboot import context
from pymsboot.engine import rpcapi


class ContextHook(hooks.PecanHook):
    """Configures a request context and attaches it to the request."""

    def before(self, state):
        headers = state.request.headers
        auth_token = headers.get('X-Auth-Token')
        state.request.context = context.make_context(auth_token=auth_token)


class RPCHook(hooks.PecanHook):
    """Attach the rpcapi object to the request so controllers can get to it."""

    def before(self, state):
        state.request.rpcapi = rpcapi.get_engine_rpc_client()
