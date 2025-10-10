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
    def updateProfile(self, firstName=self.firstName, lastName=self.lastName):
        self.update({"firstName": firstName, "lastName": lastName})
    def addPlace(self, place):
        self.places.append(place.id)
        self.save()
    def addReview(self, review):
        self.reviews.append(review.id)
        self.save()
