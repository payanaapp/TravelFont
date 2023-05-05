from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from payana.payana_service.server import service_settings
from payana.payana_service.controller.payana_bigtable_controller.payana_likes_controller import payana_likes_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_comments_controller import payana_comments_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_checkin_objects_controller import payana_checkin_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_city_influencers_controller import payana_city_influencer_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_country_cities_controller import payana_country_cities_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_excursion_checkin_objects_permission_controller import payana_excursion_checkin_objects_permission_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_excursion_objects_controller import payana_excursion_objects_name_space

payana_entity_api_blueprint = Blueprint(
    'payana_entity_api_blueprint', __name__, url_prefix='/entity')

payana_entity_table_api = Api(payana_entity_api_blueprint, version="1.0",
                               title="Payana Likes BigTable EndPoint APIs",
                               description="Manage endpoints of payana likes bigtable APIs")

payana_entity_table_api.add_namespace(payana_likes_name_space)
payana_entity_table_api.add_namespace(payana_comments_name_space)
payana_entity_table_api.add_namespace(payana_checkin_name_space)
payana_entity_table_api.add_namespace(payana_city_influencer_name_space)
payana_entity_table_api.add_namespace(payana_country_cities_name_space)
payana_entity_table_api.add_namespace(payana_excursion_checkin_objects_permission_name_space)
payana_entity_table_api.add_namespace(payana_excursion_objects_name_space)

@payana_entity_table_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not service_settings.FLASK_DEBUG:
        return {'message': message}, 500
