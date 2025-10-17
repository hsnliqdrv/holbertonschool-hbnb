from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.errors import *

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        if (self.get_user_by_email(user_data["email"])):
            raise EmailTakenError
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        if (not self.get_user(user_id)):
            raise UserNotFoundError
        if (self.get_user_by_email(user_data["email"])):
            raise EmailTakenError
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        if not self.get_amenity(amenity_id):
            raise AmenityNotFoundError
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    def create_place(self, place_data):
        owner = self.get_user(place_data["owner_id"])
        if (not owner):
            raise UserNotFoundError
        place = Place(**place_data)
        owner.addPlace(place)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        if not self.get_place(place_id):
            raise PlaceNotFoundError
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if (not user):
            raise UserNotFoundError
        if (not place):
            raise PlaceNotFoundError
        review = Review(**review_data)
        user.addReview(review)
        place.addReview(place)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise PlaceNotFoundError
        return [self.get_review(review_id) for review_id in place.reviews]

    def update_review(self, review_id, review_data):
        if not self.get_review(review_id):
            return ReviewNotFoundError
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return ReviewNotFoundError
        place = self.get_place(review.place_id)
        user = self.get_user(review.user_id)
        user.removeReview(review)
        place.removeReview(review)
        self.review_repo.delete(review_id)
