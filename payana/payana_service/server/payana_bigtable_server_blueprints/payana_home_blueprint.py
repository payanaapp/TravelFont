from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from payana.payana_service.server import service_settings
from payana.payana_service.controller.payana_bigtable_controller.payana_profile_page_controller import profile_table_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_global_influencers_feed_search_itinerary_cache_controller import payana_global_city_influencers_feed_search_itinerary_cache_name_space

payana_home_api_blueprint = Blueprint(
    'payana_home_api_blueprint', __name__, url_prefix='/home')

payana_home_api = Api(payana_home_api_blueprint, version="1.0",
                      title="Payana BigTable APIs",
                      description="Manage endpoints of payana bigtable APIs")

payana_home_api.add_namespace(profile_table_name_space)
payana_home_api.add_namespace(payana_global_city_influencers_feed_search_itinerary_cache_name_space)


@payana_home_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not service_settings.FLASK_DEBUG:
        return {'message': message}, 500
