from flask import Flask
from database.config import Config, db  # Config와 db를 import
from controllers.user_controller import user_bp

app = Flask(__name__)
app.config.from_object(Config)  # config.py의 Config 클래스를 사용

# 데이터베이스 초기화
db.init_app(app)

# UserController의 Blueprint 등록
app.register_blueprint(user_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
