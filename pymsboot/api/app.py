import sys
from datetime import datetime

from flask import Flask, g
from flask.json import JSONEncoder
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot import config
from pymsboot.api.v1.movie import bp_movie
from pymsboot.context import make_context
from pymsboot.db.api import db_init, DbApi

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

app = Flask(__name__)


def prepare_service(argv):
    _DEFAULT_LOG_LEVELS = [
        'eventlet.wsgi.server=WARN',
        'oslo_service.periodic_task=INFO',
        'oslo_service.loopingcall=INFO',
        'oslo_concurrency.lockutils=WARN',
        'urllib3.connectionpool=CRITICAL',
        'futurist.periodics=WARN',
        'flask=INFO',
        'sqlalchemy=WARN',
        'werkzeug=INFO'
    ]
    extra_log_level_defaults = [
        'flask=INFO'
    ]
    default_log_levels = logging.get_default_log_levels()
    default_log_levels.extend(_DEFAULT_LOG_LEVELS)
    logging.register_options(CONF)
    logging.set_defaults(default_log_levels=default_log_levels + extra_log_level_defaults)

    config.parse_args(args=argv)

    logging.setup(CONF, 'pymsboot_api')


def create_app():
    if sys.argv is None:
        argv = []
    else:
        argv = sys.argv[1:]
    prepare_service(argv)

    db_init()

    LOG.info('setup api wsgi app')
    app.config.update(
        DEBUG=True,
        SECRET_KEY=b'\x87T4a\x00\x8e\x12\xf8\xaa\x90\xe2\x98\xcf6Td\xaa\xf6\x8e\xf2\n\xae\x12'
    )

    app.json_encoder = CustomJSONEncoder
    app.wsgi_app = OsloLogMiddleware(app.wsgi_app)

    app.register_blueprint(bp_movie, url_prefix='/api/v1/')

    return app


@app.before_request
def before_req():
    g.dbapi = DbApi()
    g.req_ctx = make_context()


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class OsloLogMiddleware(object):
    format = ('%(REMOTE_ADDR)s %(REMOTE_USER)s %(REMOTE_STATUS)s '
              '"%(REQUEST_METHOD)s %(REQUEST_URI)s" status: %(status)s'
              ' len: %(bytes)s')

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        LOG.info('Starting request: %s "%s %s"' %
                 (environ['REMOTE_ADDR'], environ['REQUEST_METHOD'],
                  self._get_uri(environ)))

        if LOG.isEnabledFor(logging.INFO):
            return self._log_app(environ, start_response)
        else:
            return self.application(environ, start_response)

    @staticmethod
    def _get_uri(environ):
        req_uri = (environ.get('SCRIPT_NAME', '')
                   + environ.get('PATH_INFO', ''))
        if environ.get('QUERY_STRING'):
            req_uri += '?' + environ['QUERY_STRING']
        return req_uri

    def _log_app(self, environ, start_response):
        req_uri = self._get_uri(environ)

        def replacement_start_response(status, headers, exc_info=None):
            """We need to gaze at the content-length, if set, to
            write log info.
            """
            size = None
            for name, value in headers:
                if name.lower() == 'content-length':
                    size = value
            self.write_log(environ, req_uri, status, size)
            return start_response(status, headers, exc_info)

        return self.application(environ, replacement_start_response)

    def write_log(self, environ, req_uri, status, size):
        """Write the log info out in a formatted form to ``LOG.info``.
        """
        if size is None:
            size = '-'
        log_format = {
            'REMOTE_ADDR': environ.get('REMOTE_ADDR') or '-',
            'REMOTE_USER': environ.get('HTTP_X_USER_ID', '-'),
            'REMOTE_STATUS': environ.get('HTTP_X_IDENTITY_STATUS', '-'),
            'REQUEST_METHOD': environ['REQUEST_METHOD'],
            'REQUEST_URI': req_uri,
            'status': status.split(None, 1)[0],
            'bytes': size,
        }
        # We don't need to worry about trying to avoid the cost of
        # interpolation here because we only reach this code if INFO
        # is enabled.
        message = self.format % log_format
        LOG.info(message)
