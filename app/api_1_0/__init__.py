"""Create api version one blueprint."""
from flask import Blueprint

from flask_restful import Api

version_one = Blueprint('v1', __name__, url_prefix='/api/v1')

API = Api(version_one)

from app.api_1_0 import routes
