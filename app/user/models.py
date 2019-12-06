from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def user_name(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username} with id: {self.id}>"
