"""Defines the decorators for the errors."""
from flask import Blueprint, make_response, jsonify

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def resource_not_found(e):
    """Show custom error for inexisting resource."""
    return jsonify({"error": "Resource not found"}), 404

@errors.errorhandler(500)
def internal_server_error(e):
    """Show custom error for inexisting resource."""
    return jsonify({"error": "Internal Server error"}), 500


@errors.errorhandler(405)
def method_not_allowed(e):
    """Show custom error for inexisting resource."""
    return jsonify({"error": "Internal Server error"}), 405
