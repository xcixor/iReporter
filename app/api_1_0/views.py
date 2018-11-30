"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import IncidentModel, IncidentValidators, User

db = []

users = []

logged_in = []


class Incident(Resource):
    """Implements an Incident's endpoints."""

    def __init__(self):
        """Initialize db."""
        self.db = db

    def post(self):
        """Send incident creation request."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By',
                            type=str, help='Created By is required',
                            required=True)
        parser.add_argument('Type',
                            type=str, help='Type is required',
                            required=True)
        parser.add_argument('Location', type=str,
                            help='Location is required',
                            required=True)
        parser.add_argument('Images', type=str)
        parser.add_argument('Video', type=str)
        parser.add_argument('Comment', type=str,
                            help='Comment is required',
                            required=True)
        parser.add_argument('Title', type=str,
                            help='Title is required',
                            required=True)
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


class EditIncidentComment(Resource):
    """Edit incident comment."""

    def __init__(self):
        self.db = db

    def patch(self, incident_id):
        """Edit an incidence."""
        parser = reqparse.RequestParser()
        parser.add_argument('Comment',
                            type=str,
                            help='Comment is required',
                            required=True)
        args = parser.parse_args()
        validate = IncidentValidators()
        comment = args['Comment']
        if validate.validate_comment(args['Comment']):
            comment = args['Comment']
        else:
            return {'status': 400, 'error': validate.errors}, 400
        res = IncidentModel.update_comment(incident_id, self.db, comment)
        if res['status']:
            return {'status': 200, 'data': {'Id': res['message'], 'message': 'Updated red-flag record’s comment'}}, 200
        return {'status': 404, 'error': res['message']}, 404


class EditIncidentLocation(Resource):
    """Edit Incident location."""

    def __init__(self):
        self.db = db

    def patch(self, incident_id):
        """Edit an incidence location."""
        parser = reqparse.RequestParser()
        parser.add_argument('Location',
                            type=str,
                            help='Location is required',
                            required=True)
        args = parser.parse_args()
        validate = IncidentValidators()
        location = args['Location']
        if validate.validate_location(args['Location']):
            location = args['Location']
        else:
            return {'status': 400, 'error': validate.errors}, 400

        res = IncidentModel.update_location(incident_id, self.db, location)
        if res['status']:
            return {'status': 200, 'data': {'Id': res['message'], 'message': 'Updated incident location'}}, 200
        return {'status': 404, 'error': res['message']}, 404


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

    def delete(self, incident_id):
        """Delete an incident."""
        res = IncidentModel.delete_incident(incident_id, self.db)
        if res:
            return {'status': 200,
                    'data': "Incident successfuly deleted"}, 200
        return {'status': 404, 'error':
                'That resource cannot be found'}, 404


class Signup(Resource):
    """Register user."""

    def __init__(self):
        """Initialize users list."""
        self.users = users

    def post(self):
        """Create user."""
        parser = reqparse.RequestParser()
        parser.add_argument('Email',
                            type=str,
                            help='Email is required',
                            required=True)
        parser.add_argument('Password',
                            type=str,
                            help='Password is required',
                            required=True)
        parser.add_argument('Confirm Password',
                            type=str,
                            help='Confirm Password is required',
                            required=True)
        args = parser.parse_args()

        user = User(args['Email'], args['Password'])
        res = user.sign_up(args['Confirm Password'], self.users)
        if res.get('status'):
            return {'data': {'message': res.get('message'), 'status': 201}}, 201
        return {'status': 400, 'errors': user.errors}, 400


class Signin(Resource):
    """Signup user."""

    def __init__(self):
        """Initialize login list."""
        self.logged_in = logged_in
        self.users = users

    def post(self):
        """Create user."""
        parser = reqparse.RequestParser()
        parser.add_argument('Email',
                            type=str,
                            help='Email is required',
                            required=True)
        parser.add_argument('Password',
                            type=str,
                            help='Password is required',
                            required=True)
        args = parser.parse_args()

        user = User(args['Email'], args['Password'])
        res = user.login(args['Email'], args['Password'], self.logged_in, self.users)
        if res.get('status'):
            return {'data': {'message': res.get('message'), 'status': 200}}, 200
        return {'status': 400, 'errors': res['message']}, 400


class Signout(Resource):
    """Signup user."""

    def __init__(self):
        """Initialize login list."""
        self.logged_in = logged_in

    def post(self, user_id):
        """Create user."""
        res = User.logout(user_id, self.logged_in)
        if res['status']:
            return {'data': {'message': res['message'], 'status': 200}}, 200
        return {'status': 400, 'errors': res['message']}, 400
