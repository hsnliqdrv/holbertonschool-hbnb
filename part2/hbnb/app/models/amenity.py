import base

class Amenity(base.BaseModel):
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
    @staticmethod
    def listByPlace(placesRepo, placeId):
        return placesRepo.get(placeId).amenities
