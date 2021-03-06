from flask import Blueprint, jsonify, g, request
from oslo_log import log as logging
from oslo_utils import uuidutils

from pymsboot.engine.rpcapi import get_engine_rpc_client

LOG = logging.getLogger(__name__)

bp_movie = Blueprint('movie', __name__)


@bp_movie.route('/movie', methods=['GET'])
def get_all_movie():
    LOG.info('Get all movie')
    movies = g.dbapi.get_all_movies()
    LOG.info(movies)
    return jsonify({
        'msg': 'success',
        'data': [m.as_dict() for m in movies]
    }), 200


@bp_movie.route('/movie/<uuid>', methods=['GET'])
def get_movie(uuid):
    LOG.info('Get movie {}'.format(uuid))
    movie = g.dbapi.get_movie_by_uuid(uuid)
    LOG.info(movie)
    return jsonify({
        'msg': 'success',
        'data': movie.as_dict()
    }), 200


@bp_movie.route('/movie', methods=['POST'])
def create_movie():
    content = request.json
    LOG.info('create movie with ', content)
    content['uuid'] = uuidutils.generate_uuid()
    get_engine_rpc_client().create_movie(g.req_ctx, content_json=content)

    return jsonify({
        'msg': 'async',
        'data': ''
    }), 200


@bp_movie.route('/movie/<uuid>', methods=['PUT'])
def update_movie(uuid):
    content = request.json
    LOG.info('update movie {} with {}'.format(uuid, content))
    get_engine_rpc_client().update_movie(g.req_ctx, uuid=uuid, content_json=content)

    return jsonify({
        'msg': 'async',
        'data': ''
    }), 200


@bp_movie.route('/movie/<uuid>', methods=['DELETE'])
def delete_movie(uuid):
    LOG.info('delete movie {}'.format(uuid))
    get_engine_rpc_client().delete_movie(g.req_ctx, uuid=uuid)
    return jsonify({
        'msg': 'async',
        'data': ''
    }), 200
