from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import relationship
from app import db

# Association table for many-to-many relationship
place_amenity = db.Table('place_amenity',
    Column('place_id', Integer, db.ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', Integer, db.ForeignKey('amenities.id'), primary_key=True)
)
