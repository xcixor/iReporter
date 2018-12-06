"""Contains custom error messages."""


def bad_request(msg):
    """Request not processed by server due to client error.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 400}, 400


def no_content(msg):
    """Request successful but no content.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 204}, 204


def forbidden(msg):
    """Request does not have the necessary permissions.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 403}, 403


def unauthorized(msg):
    """Request lacks proper authorization.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 401}, 401


def not_found(msg):
    """Resource requested or url does not exist.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 404}, 404


def conflict(msg):
    """Conflict in the current state of the resource.

    args:
        msg(str): The error to display
    returns:
        error(dict): The error encounters and the status
        status code(int): The failure status code
    """
    return {'error': msg, 'status': 409}, 409
