from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20))
    email = db.Column(db.String(length=50),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(length=180),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    address = db.Column(db.String(length=190), nullable=True)
    orders = db.relationship("Order", back_populates="user")
    # is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
