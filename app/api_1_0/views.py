"""Api endpoint implementation."""
from flask_restful import Resource, reqparse

from app.api_1_0.models import RedFlagModel, RedFlagValidators, User

from app.errors import bad_request, not_found, no_content


DB = []

USERS = []

LOGGED_IN = []


class RedFlag(Resource):
    """Implements an RedFlag's endpoints."""

    def post(self):
        """Send redflag creation request."""
        parser = reqparse.RequestParser()
        parser.add_argument('Created By',
                            type=int, help='Created By is required',
                            required=True)
        parser.add_argument('Location', type=str,
                            help='Location is required',
                            required=True)
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
        res = redflag.save(DB)
        if res['status']:
            return {'status': 201, 'data': res['message']}, 201
        redflag_validation_errors = res['message']['errors'].copy()
        redflag.errors.clear()
        return bad_request(redflag_validation_errors)

    def get(self):
        """Return all created redflags."""
        if DB:
            return {'status': 200, 'data': DB}, 200
        return no_content('There are no redflags at the moment')


class EditRedFlagComment(Resource):
    """Edit RedFlag comment."""

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
        res = RedFlagModel.update_resource(redflag_id, DB,
                                           Comment=comment)
        if res['status']:
            return {'status': 200,
                    'data': {'Id': res['message'],
                             'message': 'Updated red-flag {}'.
                                        format('record’s comment')}}, 200
        return not_found(res['message'])


class EditRedFlagLocation(Resource):
    """Edit RedFlag location."""

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

        res = RedFlagModel.update_resource(redflag_id, DB,
                                           Location=location)
        if res['status']:
            return {'status': 200,
                    'data': {'Id': res['message'],
                             'message': 'Updated redflag {}'.
                                        format('location')}}, 200
        return not_found(res['message'])


class RedFlagManipulation(Resource):
    """Manage redflags."""

    def get(self, redflag_id):
        """Get a specefic redflag."""
        redflag = RedFlagModel.find_redflag(redflag_id, DB)
        if isinstance(redflag, dict):
            return {'status': 200, 'data': redflag}, 200
        return not_found('That redflag cannot be found')

    def delete(self, redflag_id):
        """Delete an redflag."""
        res = RedFlagModel.delete_redflag(redflag_id, DB)
        if res:
            return {'status': 200,
                    'data': "redflag successfuly deleted"}, 200
        return not_found('That redflag cannot be found')


class Signup(Resource):
    """Register user."""

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
        res = user.sign_up(args['Confirm Password'], USERS)
        if res.get('status'):
            return {'data': {'message': res.get('message'),
                             'status': 201}}, 201
        return bad_request(user.errors)


class Signin(Resource):
    """Signup user."""

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
        res = user.login(args['Email'], args['Password'], LOGGED_IN,
                         USERS)
        if res.get('status'):
            return {'data': {'message': res.get('message'),
                             'status': 200}}, 200
        return bad_request(res['message'])


class Signout(Resource):
    """Signup user."""

    def post(self, user_id):
        """Create user."""
        res = User.logout(user_id, LOGGED_IN)
        if res['status']:
            return {'data': {'message': res['message'], 'status': 200}}, 200
        return bad_request(res['message'])
