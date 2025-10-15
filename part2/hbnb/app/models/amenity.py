from .base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        self.name = name
    @staticmethod
    def listByPlace(placesRepo, placeId):
        return placesRepo.get(placeId).amenities
