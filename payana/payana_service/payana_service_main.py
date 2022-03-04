from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields
from payana.payana_service.server import service_settings
from payana.payana_service.server.payana_bigtable_server.payana_bigtable_server_init import payana_profile_table_api_blueprint

payana_flask_app = Flask(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = service_settings.FLASK_SERVER_NAME


def initialize_app(flask_app):
    configure_app(flask_app)
    # payana_service_app.init_app(payana_profile_table_api_blueprint)
    flask_app.register_blueprint(
        payana_profile_table_api_blueprint)


def main():
    initialize_app(payana_flask_app)
    payana_flask_app.run(debug=service_settings.FLASK_DEBUG)


def run():
    initialize_app(payana_flask_app)
    payana_flask_app.run(debug=service_settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
