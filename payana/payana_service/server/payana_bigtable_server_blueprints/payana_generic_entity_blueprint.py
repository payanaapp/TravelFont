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
from payana.payana_service.controller.payana_bigtable_controller.payana_itinerary_objects_controller import payana_itinerary_objects_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_global_city_rating_itinerary_controller import payana_global_city_itinerary_rating_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_neighboring_cities_controller import payana_neighboring_cities_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_autocomplete_cities_controller import payana_autocomplete_cities_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_autocomplete_users_controller import payana_autocomplete_users_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_sign_up_mail_notification_controller import payana_mail_id_sign_up_notification_name_space
from payana.payana_service.controller.payana_gcs_controller.payana_signed_url_controller import payana_signed_url_name_space
from payana.payana_service.controller.payana_gcs_controller.payana_gcs_objects_read_write_edit_controller import payana_gcs_object_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_global_city_timestamp_itinerary_controller import payana_global_city_itinerary_timestamp_name_space
from payana.payana_service.controller.payana_bigtable_controller.payana_tables_controller import payana_tables_name_space

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
payana_entity_table_api.add_namespace(payana_global_city_itinerary_rating_name_space)
payana_entity_table_api.add_namespace(payana_global_city_itinerary_timestamp_name_space)
payana_entity_table_api.add_namespace(payana_neighboring_cities_name_space)
payana_entity_table_api.add_namespace(payana_autocomplete_users_name_space)
payana_entity_table_api.add_namespace(payana_autocomplete_cities_name_space)
payana_entity_table_api.add_namespace(payana_mail_id_sign_up_notification_name_space)
payana_entity_table_api.add_namespace(payana_signed_url_name_space)
payana_entity_table_api.add_namespace(payana_gcs_object_name_space)
payana_entity_table_api.add_namespace(payana_tables_name_space)
payana_entity_table_api.add_namespace(payana_itinerary_objects_name_space)
        
@payana_entity_table_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not service_settings.FLASK_DEBUG:
        return {'message': message}, 500
