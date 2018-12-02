"""repeated stuff."""

import re


def is_empty(value):
    """Check if string is empty or whitespace.

    args:
        value(str): string to check for whitespace or none
    """
    if value.isspace() or value == "":
        return True


def has_special_characters(value):
    """Check if string has special characters.

    args:
        value(str): String to check for special characters
    """
    if not re.match("^[a-zA-Z0-9 _]*$", value):
        return True


def is_email(email):
    """Check if string is a valid email.

    args:
        email(str): value to check
    """
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                email):
        return True

def is_valid_password(password):
        """Check if password meets specifications.

        args:
            password(str): string to validate
        """
        if len(password) >= 8:
            return True
