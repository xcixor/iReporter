"""Contains the models for the data."""
import datetime
from app.utils import is_email, is_empty, is_valid_password
from app.utils import has_special_characters


class RedFlagValidators():
    """Validates a RedFlag object data."""

    def __init__(self):
        """Initialize validator with empty errors list."""
        self.errors = []

    def validate_creator(self, creator):
        """Verify and set created_by."""
        if creator:
            created_by = creator
            if isinstance(created_by, int):
                return True
            self.errors.append("Created by should be an Integer")
            return False
        self.errors.append("redflag owner should not be blank")
        return False

    def validate_title(self, title):
        """Validate Title."""
        if not is_empty(title):
            if not has_special_characters(title):
                return True
            self.errors.append(("Title cannot contain special characters"))
        self.errors.append("Title cannot be empty")
        return False

    def validate_location(self, location):
        """Validate location."""
        if not is_empty(location):
            coordinates = [x.strip() for x in location.split(',')]
            if len(coordinates) == 2:
                longitude = ''
                lat = ''
                try:
                    longitude = float(coordinates[0])
                    lat = float(coordinates[1])
                except:
                    longitude = None
                    lat = None
                if longitude is not None and lat is not None:
                    return True
                self.errors.append(
                    "Coordinates should be floating point values")
                return False
            self.errors.append("Two coordinates required")
            return False
        self.errors.append("Location should not be empty")
        return False

    def validate_comment(self, comment):
        """Validate comment."""
        if not is_empty(comment):
            if not has_special_characters(comment):
                return True
            self.errors.append("Comments cannot contain {}".
                               format("special characters"))
            return False
        self.errors.append("Comments cannot be empty")
        return False


class RedFlagModel(RedFlagValidators):
    """This class models an RedFlag."""

    def __init__(self, created_by, location, title, comment):
        """Initialize an redflag object.

        args:
            created_by(str): redflag owner
            location(str): longituted, latitude coordinates
            status(str): draft, under investigation, resolved or rejected
            comment(str): A description of the redflag
        """
        super().__init__()
        self.incident_id = ''
        self.created_by = created_by
        self.created_on = datetime.datetime.now()
        self.location = location
        self.title = title
        self.comment = comment

    def save(self, incident_list):
        """Save redflag to db.

        args:
            db(list): The list into which to save the redflag.
        """
        if self.validate_creator(self.created_by) and \
           self.validate_location(self.location) and \
           self.validate_comment(self.comment) and \
           self.validate_title(self.title):
            self.incident_id = len(incident_list) + 1
            incident_list.append({self.incident_id: self.describe_redflag()})
            return {'status': True,
                    'message': {"Id": self.incident_id,
                                "message": "Successfuly created redflag"}}
        return {'status': False, 'message': {'errors': self.errors}}

    @classmethod
    def find_redflag(cls, redflag_id, redflag_list):
        """Retrieve an redflag."""
        comp = [incident for incident in redflag_list if next(iter(incident)) == redflag_id]
        if comp:
            return comp[0]
        return None

    @classmethod
    def update_resource(cls, redflag_id, redflag_list, **kwargs):
        """Update an redflag location."""
        redflag = cls.find_redflag(redflag_id, redflag_list)
        if redflag:
            update_redflag = cls.get_dict_values(redflag)
            update_redflag.update(kwargs)
            return {'status': True, 'message': update_redflag['Id']}
        else:
            return {'status': False, 'message': 'That redflag cannot be found'}

    @staticmethod
    def get_dict_values(dict_value):
        for key, value in dict_value.items():
            return value

    @classmethod
    def delete_redflag(cls, redflag_id, redflag_list):
        """Delete an redflag."""
        incident = RedFlagModel.find_redflag(redflag_id, redflag_list)
        print(incident)
        if incident:
            redflag_list.remove(incident)
            return True
        return False

    def describe_redflag(self):
        """Return the object description.

        returns:
            dict: redflag properties

        """
        return {
            'Id': self.incident_id,
            'Created By': int(self.created_by),
            'Date Created': str(self.created_on),
            'Location': self.location,
            'Comment': self.comment,
            'Title': self.title
        }


class UserValidators():
    """Validate user fields."""

    def __init__(self):
        """Initialize validator with empty errors list."""
        self.errors = []

    def validate_email(self, email):
        """Validate email."""
        if not is_empty(email):
            if is_email(email):
                return True
            self.errors.append('Invalid Email Address')
            return False
        self.errors.append("Email should not be blank")
        return False

    def validate_password(self, password):
        """Validate password."""
        if not is_empty(password):
            if is_valid_password(password):
                return True
            self.errors.append("Password should be atleast eight characters")
            return False
        self.errors.append("Password should not be blank")
        return False

    def match_password(self, password, confirm_passowrd):
        """Match passwords."""
        if password == confirm_passowrd:
            return True
        self.errors.append("Passwords should match")
        return False


class User(UserValidators):
    """Models a user."""

    def __init__(self, email, password):
        """Initialize a user.

        args:
            email: user email id
            password: secret characters
            confirm_passowrd: confirmation password
        """
        super().__init__()
        self.email = email
        self.password = password
        self.user_id = ''

    def sign_up(self, confirm_passowrd, users):
        """Register user.

        args:
            users: list to save the user
        """
        if self.validate_email(self.email) and \
           self.validate_password(self.password) and \
           self.validate_password(confirm_passowrd):
            if self.match_password(confirm_passowrd, self.password):
                if not self.find_user(self.email, users):
                    self.user_id = len(users) + 1
                    users.append({self.email: self.describe_user()})
                    return {'status': True,
                            'message': {"Id": self.email,
                                        "message":
                                        "You have successfuly signed up"}}
                return {'status': False,
                        'message': self.errors.
                                   append("That email is already taken")}
            return {'status': False, 'message': {'errors': self.errors}}
        return {'status': False, 'message': {'errors': self.errors}}

    def describe_user(self):
        """Return object representation of user."""
        return {
            "Email": self.email,
            "Password": self.password,
            "Id": self.user_id
        }

    @classmethod
    def find_user(cls, email, users):
        """Retrieve user."""
        for user in users:
            for key, value in user.items():
                if key == email:
                    return value
                return None

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
