from flask import Blueprint, jsonify, g
from oslo_log import log as logging

from pymsboot.engine.rpcapi import get_engine_rpc_client

LOG = logging.getLogger(__name__)

bp_movie = Blueprint('movie', __name__)


@bp_movie.route('/movie', methods=['GET'])
def get_all_movie():
    movies = get_engine_rpc_client().get_all_movie(g.req_ctx)
    LOG.info(movies)
    return jsonify({'message': movies}), 200
