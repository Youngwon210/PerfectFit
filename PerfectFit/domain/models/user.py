from database.config import db


class User(db.Model):
    __tablename__ = 'user'  # 테이블 이름
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return f'<User {self.name}>'
