from .base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
    @property
    def rating(self):
        return self._rating
    @rating.setter
    def rating(self, value):
        if not (1 <= value <= 5):
            raise ValueError("Review.rating must be between 1 and 5 (inclusive)")
        self._rating = value
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        if len(value) == 0:
            raise ValueError("Review.text cannot be empty")
        self._text = value
