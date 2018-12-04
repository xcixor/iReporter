"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import RedFlagModel, RedFlagValidators, User

db = []

users = []

logged_in = []


class RedFlag(Resource):
    """Implements an RedFlag's endpoints."""

    def __init__(self):
        """Initialize db."""
        self.db = db

    def post(self):
        """Send redflag creation request."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By',
                            type=str, help='Created By is required',
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
        redflag = RedFlagModel(
            args['Created By'], args['Location'],
            args['Title'], args['Comment'])
        res = redflag.save(db)
        if res['status']:
            return {'status': 201, 'data': res['message']}, 201
        redflag_validation_errors = res['message']['errors'].copy()
        redflag.errors.clear()
        return {'status': 400, 'errors': redflag_validation_errors}, 400

    def get(self):
        """Return all created redflags."""
        if len(self.db) != 0:
            return {'status': 200, 'data': self.db}, 200
        else:
            return {'data': "There are no redflags at the moment",
                    'status': 404}, 404


class EditRedFlagComment(Resource):
    """Edit RedFlag comment."""

    def __init__(self):
        self.db = db

    def patch(self, redflag_id):
        """Edit an redflag."""
        parser = reqparse.RequestParser()
        parser.add_argument('Comment',
                            type=str,
                            help='Comment is required',
                            required=True)
        args = parser.parse_args()
        validate = RedFlagValidators()
        comment = args['Comment']
        if validate.validate_comment(args['Comment']):
            comment = args['Comment']
        else:
            return {'status': 400, 'error': validate.errors}, 400
        res = RedFlagModel.update_resource(redflag_id, self.db,
                                            Comment=comment)
        if res['status']:
            return {'status': 200, 'data': {'Id': res['message'],
                    'message': 'Updated red-flag record’s comment'}}, 200
        return {'status': 404, 'error': res['message']}, 404


class EditRedFlagLocation(Resource):
    """Edit RedFlag location."""

    def __init__(self):
        self.db = db

    def patch(self, redflag_id):
        """Edit an redflag location."""
        parser = reqparse.RequestParser()
        parser.add_argument('Location',
                            type=str,
                            help='Location is required',
                            required=True)
        args = parser.parse_args()
        validate = RedFlagValidators()
        location = args['Location']
        if validate.validate_location(args['Location']):
            location = args['Location']
        else:
            return {'status': 400, 'error': validate.errors}, 400

        res = RedFlagModel.update_resource(redflag_id, self.db,
                                            Location=location)
        if res['status']:
            return {'status': 200, 'data': {'Id': res['message'],
                                            'message': 'Updated redflag location'}}, 200
        return {'status': 404, 'error': res['message']}, 404


class RedFlagManipulation(Resource):
    """Manage redflags."""

    def __init__(self):
        """Initialize db."""
        self.db = db

    def get(self, redflag_id):
        """Get a specefic redflag."""
        redflag = RedFlagModel.find_redflag(redflag_id, self.db)
        if isinstance(redflag, dict):
            return {'status': 200, 'data': redflag}, 200
        else:
            return {'status': 404, 'error': 'That resource cannot be found'}, 404

    def delete(self, redflag_id):
        """Delete an redflag."""
        res = RedFlagModel.delete_redflag(redflag_id, self.db)
        if res:
            return {'status': 200,
                    'data': "redflag successfuly deleted"}, 200
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
        res = user.login(args['Email'], args['Password'], self.logged_in,
                         self.users)
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