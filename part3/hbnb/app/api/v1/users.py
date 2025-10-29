from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.errors import *
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('users', description='User operations')

error = api.model('Error', {
    'error': fields.String(required=True, description='Error description')
})

create_user_input = api.model('Create User Input',{
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
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
    @api.response(400, 'Invalid input data', error)
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": "Invalid input data: " + str(e)}, 400
        except EmailTakenError:
            return {"error": "Email already registered"}, 400
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
    @api.response(403, 'Unauthorized action', error)
    @api.response(400, 'Email is taken', error)
    @api.response(400, 'Invalid input data', error)
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        requester_id = get_jwt_identity()
        user_data = api.payload
        try:
            new_data = facade.update_user(requester_id, user_id, user_data)
        except ValueError as e:
            return {'error': 'Invalid input data: ' + str(e)}, 400
        except UserNotFoundError:
            return {"error": "User not found"}, 404
        except EmailTakenError:
            return {"error": "Email is taken"}, 400
        except CannotUpdateOthersError:
            return {"error": "Cannot edit other users"}, 403
        return api.marshal(new_data, create_user_output), 200
