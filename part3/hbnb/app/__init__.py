from flask_cors import CORS

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_jwt_extended import JWTManager
jwt = JWTManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask import Flask
from flask_restx import Api
from werkzeug.exceptions import BadRequest
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    CORS(app, origins=["http://127.0.0.1:8000", "http://127.0.0.1:8000"])
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    return app
