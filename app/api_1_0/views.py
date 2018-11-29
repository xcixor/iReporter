"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import IncidentModel, IncidentValidators

db = []


class Incident(Resource):
    """Implements an Incident's endpoints."""

    def __init__(self):
        """Initialize db."""
        self.db = db
        # self.incident = None

    def post(self):
        """Send incident creation request."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By')
        parser.add_argument('Type')
        parser.add_argument('Location')
        parser.add_argument('Images', type=str)
        parser.add_argument('Video', type=str)
        parser.add_argument('Comment')
        parser.add_argument('Title')
        args = parser.parse_args()
        incident = IncidentModel(
            args['Created By'], args['Type'], args['Location'],
            args['Title'], args['Comment'])
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

    def get(self, incident_id):
        """Get a specefic incident."""
        incident = IncidentModel.find_incident(incident_id, self.db)
        if isinstance(incident, dict):
            return {'status': 200, 'data': incident}, 200
        else:
            return {'status': 404, 'error': 'That resource cannot be found'}, 404

    def put(self, incident_id):
        """Edit an incidence."""
        parser = reqparse.RequestParser()
        parser.add_argument('Type')
        parser.add_argument('Title')
        args = parser.parse_args()
        new_incident = {}
        validate = IncidentValidators()
        if args['Type']:
            if validate.validate_incident_type(args['Type']):
                new_incident['Type'] = args['Type']
            else:
                return {'status': 400, 'error': validate.errors}
        if args['Title']:
            if validate.validate_title(args['Title']):
                new_incident['Title'] = args['Title']
            else:
                return {'status': 400, 'error': validate.errors}
        res = IncidentModel.update_incident(incident_id, self.db, new_incident)
        if res['status']:
            return {'status': 201, 'data': res['message']}, 201
        return {'status': 404, 'error': res['message']}, 404

    def delete(self, incident_id):
        """Delete an incident."""
        res = IncidentModel.delete_incident(incident_id, self.db)
        if res:
            return {'status': 200,
                    'data': "Incident successfuly deleted"}, 200
        return {'status': 404, 'error':
                'That resource cannot be found'}, 404
