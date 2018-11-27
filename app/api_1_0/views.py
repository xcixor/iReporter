"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import IncidentModel

db = []


class Incident(Resource):
    """Implements an Incident's endpoints."""

    def __init__(self):
        """Initialize the parameters of an incident."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Created By')
        self.parser.add_argument('Type')
        self.parser.add_argument('Location')
        self.parser.add_argument('Images', type=str)
        self.parser.add_argument('Video', type=str)
        self.parser.add_argument('Comment')
        self.args = self.parser.parse_args()
        self.db = db
        self.incident = IncidentModel(
            self.args['Created By'], self.args['Type'], self.args['Location'],
            self.args['Comment'])

    def post(self):
        """Send incident creation request."""
        res = self.incident.save(db)
        if res['status']:
            return {'status': 201, 'data': res['message']}, 201
        incident_validation_errors = res['message']['errors'].copy()
        self.incident.errors.clear()
        return {'status': 400, 'errors': incident_validation_errors}, 400

    def get(self):
        """Return all created incidents."""
        return {'status': 201, 'data': self.db}, 201
