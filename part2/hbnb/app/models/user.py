import base 

class User(base.BaseModel):
    def __init__(self, email, password, isAdmin, firstName="", lastName=""):
        super().__init__()
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.firstName = firstName
        self.lastName = lastName
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
