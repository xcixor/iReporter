"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import IncidentModel

db = []


class Incident(Resource):
    """Implements an Incident's endpoints."""

    def __init__(self):
        """Initialize the parameters of an incident."""
        self.db = db

    def post(self):
        """Send incident creation request."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By')
        parser.add_argument('Type')
        parser.add_argument('Location')
        parser.add_argument('Images', type=str)
        parser.add_argument('Video', type=str)
        parser.add_argument('Comment')
        args = parser.parse_args()
        incident = IncidentModel(
            args['Created By'], args['Type'], args['Location'],
            args['Comment'])
        res = incident.save(db)
        if res['status']:
            return {'status': 201, 'data': res['message']}, 201
        incident_validation_errors = res['message']['errors'].copy()
        self.incident.errors.clear()
        return {'status': 400, 'errors': incident_validation_errors}, 400

    def get(self):
        """Return all created incidents."""
        return {'status': 201, 'data': self.db}, 201
