from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from payana.payana_service.server import service_settings
from payana.payana_service.controller.payana_gke_controller.payana_gke_readiness_probe_controller import payana_gke_health_readiness_name_space
from payana.payana_service.controller.payana_gke_controller.payana_gke_liveness_probe_controller import payana_gke_health_liveness_name_space

payana_health_api_blueprint = Blueprint(
    'payana_health_api_blueprint', __name__, url_prefix='/health')

payana_health_api = Api(payana_health_api_blueprint, version="1.0",
                      title="Payana BigTable APIs",
                      description="Manage health endpoints of payana service APIs")

payana_health_api.add_namespace(payana_gke_health_readiness_name_space)
payana_health_api.add_namespace(payana_gke_health_liveness_name_space)


@payana_health_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not service_settings.FLASK_DEBUG:
        return {'message': message}, 500
