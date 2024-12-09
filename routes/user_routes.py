from flask import Blueprint, request, jsonify
import controllers
from lib.authenticate import token_required

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user', methods=['POST'])
def create_user_route():
    return controllers.create_user(request.json)


@user_bp.route('/users', methods=['GET'])
@token_required
def read_users_route():
    return controllers.read_users()


@user_bp.route('/user/<id>', methods=['PUT'])
@token_required
def update_user_route(id):
    return controllers.update_user(id, request.json)


@user_bp.route('/user/delete', methods=['DELETE'])
@token_required
def delete_user_route():
    return controllers.delete_user(request.json)
