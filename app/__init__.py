"""Initializes app."""

from flask import Flask, jsonify

from instance.config import CONFIG

from app.api_1_0 import version_one as v_1


def create_app(configuration):
    """Set up app.

    args:
        configuration(str): name of configuration to use for current instace
    returns:
        app(object): app instance
    """
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False

    # configure app
    app.config.from_object(CONFIG[configuration])
    CONFIG[configuration].init_app(app)

    # register blueprints
    app.register_blueprint(v_1)

    @app.errorhandler(404)
    def page_not_found(e):
        """Show custom error for inexisting resource."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def page_not_found(e):
        """Show custom error for inexisting resource."""
        return jsonify({"error": "Internal Server error"}), 500

    return app
