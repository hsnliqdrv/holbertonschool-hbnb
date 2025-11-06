from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.errors import *
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

amenity_model_input = api.model('Amenity Create Input', {
    'name': fields.String(required=True, description='Name of the amenity')
})
amenity_model_output = api.model('Amenity Create Output', {
    'id': fields.String(required=True, description='ID of amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})
error = api.model('Error', {
    'error': fields.String(required=True, description='Error description')
})
message = api.model('Message', {
    'message': fields.String(required=True, description='Message description')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model_input, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_model_output)
    @api.response(403, 'Unauthorized action', error)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def post(self):
        """Create an amenity"""
        jwt_payload = get_jwt()
        if not jwt_payload.get('is_admin'):
            return {"error": "Only admin can create amenities"}, 403
        amenity_data = api.payload
        try:
            data = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': 'Invalid input data: ' + str(e)}, 400
        return api.marshal(data, amenity_model_output), 201

    @api.response(200, 'List of amenities retrieved successfully', [amenity_model_output])
    def get(self):
        """Get all amenities"""
        return [api.marshal(a, amenity_model_output) for a in facade.get_all_amenities()]

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', amenity_model_output)
    @api.response(404, 'Amenity not found', error)
    def get(self, amenity_id):
        """Get an amenity"""
        data = facade.get_amenity(amenity_id)
        if not data:
            return {"error": "Amenity not found"}, 404
        return api.marshal(data, amenity_model_output), 200

    @api.expect(amenity_model_input, validate=True)
    @api.response(200, 'Amenity updated successfully', message)
    @api.response(404, 'Amenity not found', error)
    @api.response(403, 'Unauthorized action', error)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        if not jwt_payload.get('is_admin'):
            return {"error": "Only admin can update amenities"}, 403
        data = api.payload
        try:
            facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {'error': 'Invalid input data: ' + str(e)}, 400
        except AmenityNotFoundError:
            return {"error": "Amenity not found"}, 404
        return {"message":"Amenity updated successfully"}, 200
