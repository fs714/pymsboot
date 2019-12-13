from flask import Flask
from oslo_config import cfg
from oslo_log import log as logging

from pymsboot.api.v1.movie import bp_movie

LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def setup_app():
    app = Flask(__name__)

    app.config.update(
        DEBUG=True,
        SECRET_KEY=b'\x87T4a\x00\x8e\x12\xf8\xaa\x90\xe2\x98\xcf6Td\xaa\xf6\x8e\xf2\n\xae\x12'
    )

    app.register_blueprint(bp_movie, url_prefix='/api/v1/')

    return app
