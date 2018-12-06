"""Contains the models for the data."""
import datetime
from app.api_1_0.validators import RedFlagValidators, UserValidators


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
