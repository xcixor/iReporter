"""Defines the routes of the api."""

from app.api_1_0 import api
from app.api_1_0 import views

api.add_resource(views.Incident, '/incidents')
api.add_resource(views.IncidentManipulation, '/incidents/<incident_id>')
api.add_resource(views.EditIncidentComment,
                 '/incidents/<incident_id>/comments')
api.add_resource(views.EditIncidentLocation,
                 '/incidents/<incident_id>/location')
api.add_resource(views.Signup, '/auth/signup')
