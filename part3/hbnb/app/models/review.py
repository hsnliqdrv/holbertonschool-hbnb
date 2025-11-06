from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    @validates("text")
    def validate_text(self, key, value):
        if len(value) == 0:
            raise ValueError("text cannot be empty")
        return value
    @validates("rating")
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value
