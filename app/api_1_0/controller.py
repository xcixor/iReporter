"""Facilitate communication between views and models"""
from app.api_1_0.validators import UserValidators


class Controller(UserValidators):
    """Manipulate model functionality."""

    def __init__(self):
        """Initialize validators."""
        super().__init__()

    def login(self, email, password, login_list, users):
        """Signin user.

        args:
            email: user email
            password: user_password
            login_list: list to save logged in user
        """
        if self.validate_email(email) and self.validate_password(password):
            user = self.find_user(email, users)
            if isinstance(user, dict):
                if self.match_password(password, user['Password']):
                    login_list.append({'Email': email, 'Id': user['Id']})
                    return {'status': True, 'message': login_list}
                return {'status': False,
                        'message': 'Invalid password/email combination'}
            return {'status': False,
                    'message': 'User not found in our database'}
        return {'status': False, 'message': self.errors}

    @classmethod
    def logout(cls, user_id, logged_in):
        """Log user out."""
        if logged_in:
            for user in logged_in:
                for key, value in user.items():
                    if str(user['Id']) == str(user_id):
                        logged_in.remove(user)
                        return {'status': True,
                                'message': 'Successfuly logged out'}
                return {'status': False,
                        'message': 'That user is not logged in'}
        return {'status': False, 'message': 'That user is not logged in'}

    @classmethod
    def find_user(cls, email, users):
        """Retrieve user."""
        for user in users:
            for key, value in user.items():
                if key == email:
                    return value
                return None
