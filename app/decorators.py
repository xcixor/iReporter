"""Defines the decorators for the errors."""
from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def resource_not_found(e):
    """Show custom error for inexisting resource."""
    return jsonify({"error": "Resource not found"}), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    """Show custom error for inexisting resource."""
    return jsonify({"error": "Internal Server error"}), 500
