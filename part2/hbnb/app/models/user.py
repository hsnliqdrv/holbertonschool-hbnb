from .base import BaseModel
import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

class User(BaseModel):
    def __init__(self, email, first_name, last_name, password="", isAdmin=False):
        super().__init__()
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        if len(value) == 0:
            raise ValueError("User.first_name cannot be empty")
        self._first_name = value
    @property
    def last_name(self):
        return self._last_name
    @last_name.setter
    def last_name(self, value):
        if len(value) == 0:
            raise ValueError("User.last_name cannot be empty")
        self._last_name = value
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        if len(value) == 0:
            raise ValueError("User.email cannot be empty")
        if not is_valid_email(value):
            raise ValueError("User.email should be valid email")
        self._email = value
    def addPlace(self, place):
        self.places.append(place.id)
        self.save()
    def addReview(self, review):
        self.reviews.append(review.id)
        self.save()
    def removePlace(self, place):
        self.places.remove(place.id)
        self.save()
    def removeReview(self, review):
        self.reviews.remove(review.id)
        self.save()
