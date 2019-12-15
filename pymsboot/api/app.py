from flask import Flask, g
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot.api.v1.movie import bp_movie
from pymsboot.context import make_context

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

app = Flask(__name__)


def setup_app():
    LOG.info('setup api wsgi app')
    app.config.update(
        DEBUG=True,
        SECRET_KEY=b'\x87T4a\x00\x8e\x12\xf8\xaa\x90\xe2\x98\xcf6Td\xaa\xf6\x8e\xf2\n\xae\x12'
    )

    app.register_blueprint(bp_movie, url_prefix='/api/v1/')

    return app


@app.before_request
def before_req():
    g.req_ctx = make_context()
