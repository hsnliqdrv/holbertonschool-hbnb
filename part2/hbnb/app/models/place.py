from .base import BaseModel

class Place(BaseModel):
    def __init__(self, title="", description="", price, latitude, logitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.ownerId = owner.id
        self.reviews = []
        self.amenities = []
    @staticmethod
    def listByOwner(placesRepo, ownerId):
        return list(filter(lambda p: p.ownerId == ownerId, placesRepo.get_all()))
    def addAmenity(self, amenity):
        if (amenity.id not in self.amenities):
            self.places.append(amenity.id)
            self.save()
    def addReview(self, review):
        if (review.id not in self.reviews):
            self.reviews.append(review.id)
            self.save()
    def removeAmenity(self, amenity):
        if (amenity.id in self.amenities):
            self.amenities.remove(amenity.id)
            self.save()
    def removeReview(self, review):
        if (review.id in self.reviews):
            self.reviews.remove(review.id)
            self.save()
