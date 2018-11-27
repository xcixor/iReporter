"""Create api version one blueprint."""
from flask import Blueprint

from flask_restful import Api

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

api = Api(v1)

from app.api_1_0 import routes