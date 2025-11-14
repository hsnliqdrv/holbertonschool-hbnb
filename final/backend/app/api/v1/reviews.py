from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.errors import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review Model Create', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})
review_model_output = api.model('Review Model Create Output', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
review_all_output = api.model('Review Model Get All', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

review_model_update = api.model('Review Model Update', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

error = api.model('Error', {
    'error': fields.String(required=True, description='Error description')
})
message = api.model('Message', {
    'message': fields.String(required=True, description='Message description')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created', review_model_output)
    @api.response(400, 'Invalid input data', error)
    @api.response(401, 'Invalid credentials', error)
    @jwt_required()
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()
        review_data = api.payload
        review_data["user_id"] = user_id
        try:
            new_data = facade.create_review(api.payload)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except UserNotFoundError:
            return {"error": "Referenced user not found"}, 400
        except PlaceNotFoundError:
            return {"error": "Referenced place not found"}, 400
        except CannotReviewOwnPlaceError:
            return {"error": "Cannot review own place"}, 400
        except AlreadyReviewedError:
            return {"error": "Place is already reviewed"}, 400
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

    @api.expect(review_model_update, validate=True)
    @api.response(200, 'Review updated successfully', message)
    @api.response(404, 'Review not found', error)
    @api.response(403, 'Unauthorized action', error)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin')
        try:
            facade.update_review(user_id, review_id, api.payload, is_admin)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        except DoesNotOwnReviewError:
            return {"error": "User does not own the review"}, 403
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully', message)
    @api.response(404, 'Review not found', error)
    @api.response(403, 'Unauthorized action', error)
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin')
        try:
            facade.delete_review(user_id, review_id, is_admin)
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        except DoesNotOwnReviewError:
            return {"error": "User does not own the review"}, 403
        return {"message": "Review deleted successfully"}, 200
