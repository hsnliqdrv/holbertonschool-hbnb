from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.errors import *

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
review_model_output = api.model('Review', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
review_all_output = api.model('Review', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

error = api.model('Error', {
    'error': fields.String(required=True, description='Error description')
})
message = api.model('Message', {
    'message': fields.String(required=True, description='Message description')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created', review_model_output)
    @api.response(400, 'Referenced user not found', error)
    @api.response(400, 'Referenced place not found', error)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            new_data = facade.create_review(api.payload)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except UserNotFoundError:
            return {"error": "Referenced user not found"}, 400
        except PlaceNotFoundError:
            return {"error": "Referenced place not found"}, 400
        return api.marshal(new_data, review_model_output), 201

    @api.response(200, 'List of reviews retrieved successfully', [review_all_output])
    def get(self):
        """Retrieve a list of all reviews"""
        return [api.marshal(r, review_all_output) for r in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_model_output)
    @api.response(404, 'Review not found', error)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if (not review):
            return {"error": "Review not found"}, 404
        return api.marshal(review, review_model_output), 200

    @api.expect(review_model_update)
    @api.response(200, 'Review updated successfully', message)
    @api.response(404, 'Review not found', error)
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully', message)
    @api.response(404, 'Review not found', error)
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully', review_all_output)
    @api.response(404, 'Place not found', error)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except PlaceNotFoundError:
            return {"error": "Place not found"}, 404
        return [api.marshal(r, review_all_output) for r in reviews], 200
