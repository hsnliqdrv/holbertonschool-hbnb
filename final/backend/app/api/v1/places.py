from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.errors import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'user': fields.Nested(user_model, description='Owner of the review')
})

# Define the place model for input validation and documentation
place_model_details = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), required=True, description="List of amenities"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})
place_model_create = api.model('Place Creation Input', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
})
place_model_create_output = api.model('Place Model Creation Output', {
    'id': fields.String(required=True, description='ID of the place'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
})
get_all_model = api.model('Get all places model', {
    'id': fields.String(required=True, description='ID of the place'),
    'title': fields.String(required=True, description='Title of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'price': fields.Float(required=True, description='Price')
})
place_model_update = api.model('Place Model Update Input', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
})
review_all_output = api.model('Review Model Get All', {
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
class PlaceList(Resource):
    @api.expect(place_model_create, validate=True)
    @api.response(201, 'Place successfully created', place_model_create_output)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def post(self):
        """Register a new place"""
        user_id = get_jwt_identity()
        place_data = api.payload
        place_data["owner_id"] = user_id
        try:
            place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except UserNotFoundError:
            return {"error": "Referenced user not found"}, 400
        return api.marshal(place, place_model_create_output), 201

    @api.response(200, 'List of places retrieved successfully', [get_all_model])
    def get(self):
        """Retrieve a list of all places"""
        return [api.marshal(p, get_all_model) for p in facade.get_all_places()]

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_model_details)
    @api.response(404, 'Place not found', error)
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return api.marshal(place, place_model_details), 200

    @api.expect(place_model_update, validate=True)
    @api.response(200, 'Place updated successfully', message)
    @api.response(404, 'Place not found', error)
    @api.response(403, 'Unauthorized action', error)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin')
        try:
            facade.update_place(user_id, place_id, api.payload, is_admin)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except PlaceNotFoundError:
            return {"error": "Place not found"}, 404
        except DoesNotOwnPlaceError:
            return {"error": "User does not own the place"}, 403
        return {"message":"Place updated successfully"}, 200

@api.route('/<place_id>/reviews')
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

