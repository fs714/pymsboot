from flask import Blueprint, jsonify

bp_movie = Blueprint('movie', __name__)


@bp_movie.route('/movie', methods=['GET'])
def get_all_movies():
    return jsonify({'message': 'All Movies'}), 200
