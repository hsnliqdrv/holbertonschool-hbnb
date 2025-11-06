from app import db, bcrypt
import uuid
from .base import BaseModel  # Import BaseModel from its module
from sqlalchemy.orm import validates

def is_valid_email(email):
    """Check if email has valid pattern"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

class User(BaseModel):
     __tablename__ = 'users'

     first_name = db.Column(db.String(50), nullable=False)
     last_name = db.Column(db.String(50), nullable=False)
     email = db.Column(db.String(120), nullable=False, unique=True)
     password = db.Column(db.String(128), nullable=False)
     is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @validates("first_name")
    def validate_first_name(self, key, value):
        if len(value) == 0:
            raise ValueError("first_name cannot be empty")
        return value

    @validates("last_name")
    def validate_first_name(self, key, value):
        if len(value) == 0:
            raise ValueError("last_name cannot be empty")
        return value

    @validates("email")
    def validate_first_name(self, key, value):
        if not is_valid_email(value):
            raise ValueError("invalid email")
        return value
