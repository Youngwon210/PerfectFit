from domain.models.user import User
from utils import open_ai


class UserService:
    @staticmethod
    def get_users():
        try:
            users = User.query.all()  # 모든 사용자 데이터 가져오기
            print(f"Fetched users: {users}")  # 쿼리된 데이터 확인
            open_ai.get_dinner_recommendation()
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")  # 에러 발생 시 메시지 출력
            return []

