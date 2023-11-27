from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler

payana_gke_health_readiness_name_space = Namespace(
    'ready', description='GKE readiness probe')

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code

payana_readiness_probe_success_message = payana_service_constants.payana_readiness_probe_success_message

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500


@payana_gke_health_readiness_name_space.route("/")
class PayanaGKEReadinessEndPoint(Resource):

    @payana_gke_health_readiness_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        return {
            status: payana_200_response,
            message: payana_readiness_probe_success_message,
            status_code: payana_200
        }, payana_200
