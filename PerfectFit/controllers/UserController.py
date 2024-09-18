from flask import Blueprint, jsonify
from services.UserService import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
def get_users():
    users = UserService.get_all_users()
    user_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(user_list)

