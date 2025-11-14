from app import db
import uuid
from .base import BaseModel  # Import BaseModel from its module

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)
