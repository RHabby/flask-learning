import unittest
from datetime import datetime, timedelta

from app import config, create_app, db
from app.collection.models import Collections
from app.user.models import User
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="bob")
        u.set_password("bob")
        self.assertFalse(u.check_password("john"))
        self.assertTrue(u.check_password("bob"))

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        self.assertEqual(u.avatar(
            128), ("https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=monsterid&s=128"))

    def test_follow(self):
        u1 = User(username="bob", email="bob@example.com")
        u2 = User(username="joseph", email="joseph@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [u2])
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "joseph")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "bob")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_bookmarks(self):
        # create usesrs
        u1 = User(username="paul", email="paul@example.com")
        u2 = User(username="john", email="john@example.com")
        u3 = User(username="ringo", email="ringo@example.com")
        u4 = User(username="george", email="george@example.com")

        # create bookmarks
        now = datetime.utcnow()
        bm1 = Collections(title="Example 01 bookmark", url="example.com/01example",
                          base_url="example.com", created=now + timedelta(seconds=1), user_id=1)
        bm2 = Collections(title="Example 02 bookmark", url="example.com/02example",
                          base_url="example.com", created=now + timedelta(seconds=1), user_id=4)
        bm3 = Collections(title="Example 03 bookmark", url="example.com/03example",
                          base_url="example.com", created=now + timedelta(seconds=2), user_id=3)
        bm4 = Collections(title="Example 04 bookmark", url="example.com/04example",
                          base_url="example.com", created=now + timedelta(seconds=2), user_id=2)
        db.session.add_all([bm1, bm2, bm3, bm4])
        db.session.commit()

        # TODO: sqlalchemy.orm.exc.DetachedInstanceError: 
        # Parent instance <User at 0x7f0ecc4fcba8> is not bound to a Session, 
        # and no contextual session is established; lazy load operation of 
        # attribute 'followed' cannot proceed (Background on this error at: 
        # http://sqlalche.me/e/bhk3)
        
        u1.follow(u2)   # paul follows john
        u1.follow(u4)   # paul follows george
        u2.follow(u3)   # john follows ringo
        u3.follow(u4)   # ringo follows george
        db.session.commit()

        fb1 = u1.followed_bookmarks.all()
        fb2 = u1.followed_bookmarks.all()
        fb3 = u1.followed_bookmarks.all()
        fb4 = u1.followed_bookmarks.all()

        self.assertEqual(fb1, [bm2, bm4])
        self.assertEqual(fb2, [bm3])
        self.assertEqual(fb3, [bm4])
        self.assertEqual(fb4, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
