from datetime import datetime

from sqlalchemy.orm import relationship

from app.db import db


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
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

    def __repr__(self):
        return f"Collection {self.id}, {self.title}"
