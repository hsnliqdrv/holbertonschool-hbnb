from .base import BaseModel

class User(BaseModel):
    def __init__(self, email="", password="", isAdmin=False, first_name="", last_name=""):
        super().__init__()
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
    def addPlace(self, place):
        if (place.id not in self.places):
            self.places.append(place.id)
            self.save()
    def addReview(self, review):
        if (review.id not in self.reviews):
            self.reviews.append(review.id)
            self.save()
    def removePlace(self, place):
        if (place.id in self.places):
            self.places.remove(place.id)
            self.save()
    def removeReview(self, review):
        if (review.id in self.reviews):
            self.reviews.remove(review.id)
            self.save()
