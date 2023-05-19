from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from payana.payana_service.server import service_settings
from payana.payana_service.controller.payana_bigtable_controller.payana_profile_page_controller import profile_table_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_profile_page_itineraries_controller import profile_page_itineraries_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_profile_page_travel_footprint_controller import profile_page_travelfont_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_likes_controller import payana_likes_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_travel_buddy_requests_controller import profile_travel_buddy_name_space

payana_profile_table_api_blueprint = Blueprint(
    'payana_profile_table_api_blueprint', __name__, url_prefix='/profile')

payana_profile_table_api = Api(payana_profile_table_api_blueprint, version="1.0",
                               title="Payana Profile Page BigTable APIs",
                               description="Manage endpoints of payana profile page bigtable APIs")

payana_profile_table_api.add_namespace(profile_table_name_space)
payana_profile_table_api.add_namespace(profile_page_itineraries_name_space)
payana_profile_table_api.add_namespace(profile_page_travelfont_name_space)
payana_profile_table_api.add_namespace(profile_travel_buddy_name_space)

@payana_profile_table_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not service_settings.FLASK_DEBUG:
        return {'message': message}, 500
