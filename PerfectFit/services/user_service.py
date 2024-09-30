from flask import flash

from domain.models.user import User
from utils import open_ai


class UserService:
    @staticmethod
    def get_users(page: int, count: int):
        try:
            paginate_user = User.query.paginate(page=page, per_page=count, error_out=False)

            open_ai.get_dinner_recommendation()
            return paginate_user
        except Exception as e:
            print(f"Error fetching users: {e}")  # 에러 발생 시 메시지 출력
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None

    @staticmethod
    def get_user(user_id: int) -> User | None:
        try:
            user = User.query.filter(User.id == user_id).first()

            if not user:
                return None

            return user
        except Exception as e:
            print(f"Error fetching user : {e}")
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None
