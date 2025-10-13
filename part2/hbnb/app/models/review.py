from .base import BaseModel

class Review(BaseModel):
    def __init__(self, placeId, userId, rating, comment):
        self.placeId = placeId
        self.userId = userId
        self.rating = rating
        self.comment = comment
    @staticmethod
    def listByPlace(reviewsRepo, placeId):
        return list(filter(lambda r: r.placeId == placeId, reviewsRepo.get_all()))
