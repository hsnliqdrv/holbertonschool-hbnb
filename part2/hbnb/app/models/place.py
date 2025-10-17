from .base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description="", price, latitude, logitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.ownerId = ownerId
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        if len(value) == 0:
            raise ValueError("Place.title cannot be empty")

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        if (value < 0):
            raise ValueError("Place.price must be non-negative")
        self._price = value

    @property
    def latitude(self):
        return self._latitude
    @latitude.setter
    def latitude(self, value):
        if (abs(value) > 90):
            raise ValueError("Place.latitude must be -90<=l<=90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude
    @longitude.setter
    def longitude(self, value):
        if (abs(value) > 180):
            raise ValueError("Price longitude must be -180<=l<=180")
        self._latitude = value

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
