from dataclasses import asdict

from flask import Blueprint, jsonify

from dto.user.intro_user import IntroUserDto
from dto.user.user_dto import UserDto
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
def get_users():
    users = UserService.get_users()
    response: UserDto.Response.Users = UserDto.Response.Users([IntroUserDto(user.id, user.name) for user in users])

    return jsonify(asdict(response))
