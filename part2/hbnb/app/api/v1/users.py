from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

error = api.model('Error', {
    'error': fields.String(required=True, description='Error description')
})

create_user_input = api.model('Create User Input',{
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})
create_user_output = api.model('Create User Output',{
    'id': fields.String(required=True, description='ID of the user'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})
update_user_input = api.model('Update User Input', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(create_user_input, validate=True)
    @api.response(201, 'User successfully created', create_user_output)
    @api.response(400, 'Email already registered', error)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}
        return api.marshal(new_user, create_user_output), 201
    @api.response(200, 'User list retrieved successfully', [create_user_output])
    def get(self):
        """Retrieve the list of users"""
        return [api.marshal(u, create_user_output) for u in facade.get_all_users()], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', create_user_output)
    @api.response(404, 'User not found', error)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return api.marshal(user, create_user_output), 200

    @api.expect(update_user_input, validate=True)
    @api.response(200, 'User successfully updated', create_user_output)
    @api.response(404, 'User not found', error)
    @api.response(400, 'Email is taken', error)
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user"""
        user_data = api.payload
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404
        if "email" in user_data and facade.get_user_by_email(user_data["email"]):
            return {'error': 'Email is taken'}, 400
        try:
            new_data = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {'error': 'Invalid input data: ' + str(e)}
        return api.marshal(new_data, create_user_output), 200
