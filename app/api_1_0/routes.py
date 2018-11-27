"""Defines the routes of the api."""

from app.api_1_0 import api
from app.api_1_0 import views

api.add_resource(views.Incident, '/incidents')
