from .base import BaseModel
import re
from app import bcrypt
def is_valid_email(email):
    """Check if email has valid pattern"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

class User(BaseModel):
    """Represents a user object"""
    def __init__(self, email, first_name, last_name, password):
        """User initializer"""
        super().__init__()
        self.email = email
        self.hash_password(password)
        self.is_admin = False
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
    @property
    def first_name(self):
        """Get first name"""
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        """Set first name"""
        if len(value) == 0:
            raise ValueError("User.first_name cannot be empty")
        self._first_name = value
    @property
    def last_name(self):
        """Get last name"""
        return self._last_name
    @last_name.setter
    def last_name(self, value):
        """Set last name"""
        if len(value) == 0:
            raise ValueError("User.last_name cannot be empty")
        self._last_name = value
    @property
    def email(self):
        """Get email"""
        return self._email
    @email.setter
    def email(self, value):
        """Set email"""
        if len(value) == 0:
            raise ValueError("User.email cannot be empty")
        if not is_valid_email(value):
            raise ValueError("User.email should be valid email")
        self._email = value
    def addPlace(self, place):
        """Add a place to list"""
        self.places.append(place.id)
        self.save()
    def addReview(self, review):
        """Add a review to list"""
        self.reviews.append(review.id)
        self.save()
    def removePlace(self, place):
        """Remove a place from list"""
        self.places.remove(place.id)
        self.save()
    def removeReview(self, review):
        """Remove a review from list"""
        self.reviews.remove(review.id)
        self.save()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
