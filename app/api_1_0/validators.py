"""This module validates the data models."""
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
