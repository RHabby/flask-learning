from hashlib import md5
from random import choice

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db
from app.collection.models import Collections


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10))
    about_me = db.Column(db.String(160))
    location = db.Column(db.String(30))
    web_site = db.Column(db.String(100))
    followed = db.relationship("User", secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic"
    )

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

    def avatar(self, size):
        hash_email = md5(self.email.lower().encode("utf-8")).hexdigest()
        avatar_types = ["404", "mp", "identicon",
                        "monsterid", "wavatar", "retro", "robohash"]
        result = f"https://www.gravatar.com/avatar/{hash_email}?d=monsterid&s={size}"
        return result

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_bookmarks(self):
        collections = Collections.query.join(followers, (followers.c.followed_id == Collections.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Collections.created.desc())
        return collections

    def __repr__(self):
        return f"<User {self.username} with id: {self.id}>"
