"""Defines the routes of the api."""

from app.api_1_0 import API as api
from app.api_1_0 import views

api.add_resource(views.RedFlag, '/redflags')
api.add_resource(views.RedFlagManipulation, '/redflags/<int:redflag_id>')
api.add_resource(views.EditRedFlagComment,
                 '/redflags/<int:redflag_id>/comments')
api.add_resource(views.EditRedFlagLocation,
                 '/redflags/<int:redflag_id>/location')
api.add_resource(views.Signup, '/auth/signup')
api.add_resource(views.Signin, '/auth/login')
api.add_resource(views.Signout, '/auth/logout/<user_id>')
