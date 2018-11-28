"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import IncidentModel

db = []


class Incident(Resource):
    """Implements an Incident's endpoints."""

    def __init__(self):
        """Initialize db."""
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
        incident.errors.clear()
        return {'status': 400, 'errors': incident_validation_errors}, 400

    def get(self):
        """Return all created incidents."""
        if len(self.db) != 0:
            return {'status': 200, 'data': self.db}, 200
        else:
            return {'data': "There are no incidences at the moment",
                    'status': 404}, 404


class IncidentManipulation(Resource):
    """Manage incidents."""

    def __init__(self):
        """Initialize db."""
        self.db = db

    def find_incident(self, incident_id):
        """Find and incident in db."""
        for value in self.db:
            for key, value in value.items():
                if str(key) == str(incident_id):
                    return value

    def get(self, incident_id):
        """Get a specefic incident."""
        incident = self.find_incident(incident_id)
        if isinstance(incident, dict):
            return {'status': 200, 'data': incident}, 200
        else:
            return {'status': 404, 'error': 'That resource cannot be found'}, 404

    def put(self, incident_id):
        """Edit an incidence."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By')
        parser.add_argument('Type')
        parser.add_argument('Location')
        parser.add_argument('Images', type=str)
        parser.add_argument('Video', type=str)
        parser.add_argument('Comment')
        args = parser.parse_args()
        new_incident = {}

        if args['Created By']:
            new_incident['Created By'] = int(args['Created By'])

        if args['Type']:
            new_incident['Type'] = args['Type']

        if args['Location']:
            new_incident['Location'] = args['Location']

        if args['Comment']:
            new_incident['Comment'] = args['Comment']

        incident = self.find_incident(incident_id)
        if isinstance(incident, dict):
            for value in self.db:
                for key, value in value.items():
                    if str(key) == str(incident_id):
                        value.update(new_incident)
                        return {'status': 201, 'data': value}, 201
        return {'status': 404, 'error': 'That resource cannot be found'}, 404
