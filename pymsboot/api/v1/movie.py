from flask import Blueprint, jsonify, g, request
from oslo_log import log as logging
from oslo_utils import uuidutils

from pymsboot.engine.rpcapi import get_engine_rpc_client

LOG = logging.getLogger(__name__)

bp_movie = Blueprint('movie', __name__)


@bp_movie.route('/movie', methods=['GET'])
def get_all_movie():
    movies = get_engine_rpc_client().get_all_movie(g.req_ctx)
    LOG.info(movies)
    return jsonify({'message': movies}), 200


@bp_movie.route('/movie/<uuid>', methods=['GET'])
def get_movie(uuid):
    movie = get_engine_rpc_client().get_movie(g.req_ctx, uuid)
    LOG.info(movie)
    return jsonify(movie), 200


@bp_movie.route('/movie', methods=['POST'])
def create_movie():
    content = request.json
    LOG.info(content)
    content['uuid'] = uuidutils.generate_uuid()
    get_engine_rpc_client().create_movie(g.req_ctx, content_json=content)
    return jsonify({'msg': 'finished'}), 200
