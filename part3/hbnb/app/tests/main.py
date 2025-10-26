import unittest
from app.services import facade
from app import create_app
class TestUserEndpoints(unittest.TestCase):
    def fakeUser(self):
        """Creates fake user"""
        return self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
    def fakeAmenity(self):
        return self.client.post('/api/v1/amenities/', json={
            'name': 'Wi-Fi'
        })
    def fakePlace(self, user_id):
        return self.client.post('/api/v1/places/', json={
            "title": "string",
            "description": "string",
            "price": 0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": user_id
        })
    def fakeReview(self, user_id, place_id):
        return self.client.post('/api/v1/reviews/', json={
            "text": "string",
            "rating": 3,
            "user_id": user_id,
            "place_id": place_id
        })
    def setUp(self):
        facade.reset()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.fakeUser()
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_taken_email(self):
        self.fakeUser()
        response = self.fakeUser()
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        user_id = self.fakeUser().json['id']
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user_taken_email(self):
        self.fakeUser()
        user_id = self.client.post('/api/v1/users/', json={
            "first_name": "Hasanali",
            "last_name": "Qadirov",
            "email": "hasanali@example.com"
        }).json["id"]
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_id(self):
        response = self.client.put(f'/api/v1/users/123/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "hasanali@example.com"
        })
        self.assertEqual(response.status_code, 404)

    def test_get_user(self):
        user_id = self.fakeUser().json['id']
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_user_non_existing(self):
        response = self.client.get(f'/api/v1/users/some_id/')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        response = self.fakeAmenity()
        self.assertEqual(response.status_code, 201)

    def test_get_amenity(self):
        amenity_id = self.fakeAmenity().json["id"]
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_non_existing(self):
        response = self.client.get(f'/api/v1/amenities/123/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        amenity_id = self.fakeAmenity().json["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'Hi-Fi'
        })
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_non_existing(self):
        response = self.client.put('/api/v1/amenities/123', json={
            'name': 'Hi-Fi'
        })
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_invalid_data(self):
        amenity_id = self.fakeAmenity().json["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': ''
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place(self):
        user_id = self.fakeUser().json["id"]
        response = self.fakePlace(user_id)
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_values(self):
        user_id = self.fakeUser().json["id"]
        response = self.client.post('/api/v1/places/', json={
            "title": "string",
            "description": "string",
            "price": -15,
            "latitude": 500,
            "longitude": -500,
            "owner_id": user_id
        })
        self.assertEqual(response.status_code, 400)
    def test_create_place_non_existing_user(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "string",
            "description": "string",
            "price": 0,
            "latitude": 0,
            "longitude": 0,
            "owner_id": "123"
        })
        self.assertEqual(response.status_code, 400)
    def test_get_place(self):
        user_id = self.fakeUser().json["id"]
        place_id = self.fakePlace(user_id).json['id']
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_place_non_existing(self):
        response = self.client.get('/api/v1/places/123/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        user_id = self.fakeUser().json["id"]
        place_id = self.fakePlace(user_id).json['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': 'New Title',
            'description': '',
            'price': 400
        })
        self.assertEqual(response.status_code, 200)

    def test_update_place_non_existing(self):
        response = self.client.put('/api/v1/places/123', json={
            'title': 'New Title',
            'description': '',
            'price': 400
        })
        self.assertEqual(response.status_code, 404)

    def test_update_place_invalid_data(self):
        user_id = self.fakeUser().json["id"]
        place_id = self.fakePlace(user_id).json['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': '',
            'description': '',
            'price': -30
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        response = self.fakeReview(user_id, place_id)
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        response = self.fakeReview('123', '234')
        self.assertEqual(response.status_code, 400)

    def test_get_review(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        review = self.fakeReview(user_id, place_id)
        review_id = review.json['id']
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_non_existing(self):
        response = self.client.get('/api/v1/reviews/123/')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        self.fakeReview(user_id, place_id).json['id']
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_by_place_404(self):
        response = self.client.get(f'/api/v1/places/123/reviews')
        self.assertEqual(response.status_code, 404)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        review_id = self.fakeReview(user_id, place_id).json['id']
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_non_existing(self):
        response = self.client.delete('/api/v1/reviews/123')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        review_id = self.fakeReview(user_id, place_id).json['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Hello',
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review_non_existing(self):
        response = self.client.put('/api/v1/reviews/123', json={
            'text': 'Hello',
            'rating': 5
        })
        self.assertEqual(response.status_code, 404)

    def test_update_review_invalid_input(self):
        user_id = self.fakeUser().json['id']
        place_id = self.fakePlace(user_id).json['id']
        review_id = self.fakeReview(user_id, place_id).json['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Terrible',
            'rating': -1
        })
        self.assertEqual(response.status_code, 400)
