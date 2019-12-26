from datetime import datetime

from sqlalchemy.orm import relationship

from app.db import db


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    base_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    content_type = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        index=True
    )

    user = relationship("User", backref="collections")

    def comments_count(self):
        return CollectionsComment.query.filter(CollectionsComment.collections_id == self.id).count()

    def __repr__(self):
        return f"Collection {self.id}, {self.title}"


class CollectionsComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    collections_id = db.Column(
        db.Integer,
        db.ForeignKey("collections.id", ondelete="CASCADE"),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        index=True
    )

    collections = relationship("Collections", backref="comments")
    user = relationship("User", backref="comments")

    def __repr__(self):
        return f"Comment {self.id}"
