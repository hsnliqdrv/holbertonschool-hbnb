from .base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        if len(value) == 0:
            raise ValueError("Review.text cannot be empty")
        return self._text
