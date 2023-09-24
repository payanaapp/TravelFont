from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields
from payana.payana_service.server import service_settings
from payana.payana_service.server.payana_bigtable_server_blueprints.payana_profile_page_blueprint import payana_profile_table_api_blueprint
from payana.payana_service.server.payana_bigtable_server_blueprints.payana_home_blueprint import payana_home_api_blueprint
from payana.payana_service.server.payana_bigtable_server_blueprints.payana_generic_entity_blueprint import payana_entity_api_blueprint
from payana.payana_service.server.payana_bigtable_gunicorn_server_init import gunicorn_init_app

import multiprocessing

payana_flask_app = Flask(__name__)

def number_of_gunicorn_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = service_settings.FLASK_SERVER_NAME


def register_payana_blueprints(flask_app):
    flask_app.register_blueprint(
        payana_profile_table_api_blueprint)
    
    flask_app.register_blueprint(
        payana_home_api_blueprint)
    
    flask_app.register_blueprint(
        payana_entity_api_blueprint)
    

def initialize_app():
    configure_app(payana_flask_app)
    register_payana_blueprints(payana_flask_app)
    payana_flask_app.run(debug=service_settings.FLASK_DEBUG)
    
def gunicorn_initialize_app():
    configure_app(payana_flask_app)
    register_payana_blueprints(payana_flask_app)
    
    workers = number_of_gunicorn_workers()
    port = '8888'
    
    gunicorn_payana_app = gunicorn_init_app(port, workers, payana_flask_app)
    gunicorn_payana_app.run()


def main():
    register_payana_blueprints(payana_flask_app)


if __name__ == "__main__":
    main()
