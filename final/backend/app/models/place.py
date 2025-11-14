from app import db
from app.models.secondary import place_amenity
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=True, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery',
                             backref=db.backref('places', lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates("title")
    def validate_title(self, key, value):
        if len(value) == 0:
            raise ValueError("title cannot be empty")
        return value
    @validates("description")
    def validate_desc(self, key, value):
        if len(value) == 0:
            raise ValueError("description cannot be empty")
        return value
    @validates("price")
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("price must not be negative")
        return value
    @validates("latitude")
    def validate_lat(self, key, value):
        if abs(value) > 90:
            raise ValueError("latitude must be between -90 and 90")
        return value
    @validates("longitude")
    def validate_lon(self, key, value):
        if abs(value) > 180:
            raise ValueError("latitude must be between -180 and 180")
        return value
