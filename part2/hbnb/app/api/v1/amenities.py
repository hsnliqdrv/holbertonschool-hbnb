from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def amenity_repr(amenity):
    return {"id": amenity.id, "name": amenity.name}

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create an amenity"""
        amenity_data = api.payload
        data = facade.create_amenity(amenity_data)
        return amenity_repr(data), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        return list(map(amenity_repr, facade.get_all_amenities()))

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get an amenity"""
        data = facade.get_amenity(amenity_id)
        if not data:
            return {"error": "Amenity not found"}, 404
        return amenity_repr(data), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        if not facade.get_amenity(amenity_id):
            return {"error": "Amenity not found"}, 404
        data = api.payload
        facade.update_amenity(amenity_id, data)
        return {"message":"Amenity updated successfully"}, 200
