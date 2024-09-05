#!/usr/bin/env python

"""Contains functions for parsers
"""

from flask_restx import reqparse
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler

payana_profile_id_header = payana_service_constants.payana_profile_id_header
payana_activity_id_header = payana_service_constants.payana_activity_id_header
payana_mail_id_header = payana_service_constants.payana_mail_id_header
payana_entity_id_header = payana_service_constants.payana_entity_id_header
payana_city_header = payana_service_constants.payana_city_header
payana_user_header = payana_service_constants.payana_autocomplete_users_header
payana_country_header = payana_service_constants.payana_country_header
payana_comment_id_header = payana_service_constants.payana_comment_id_header
payana_check_in_id_header = payana_service_constants.payana_check_in_id_header
payana_excursion_id_header = payana_service_constants.payana_excursion_id_header
payana_itinerary_id_header = payana_service_constants.payana_itinerary_id_header
payana_itinerary_name_header = payana_service_constants.payana_itinerary_name_header
payana_friend_id_header = payana_service_constants.payana_friend_id_header
payana_signed_url_storage_bucket_header = payana_service_constants.payana_signed_url_storage_bucket_header
payana_signed_url_storage_object_header = payana_service_constants.payana_signed_url_storage_object_header
payana_autocomplete_header = payana_service_constants.payana_autocomplete_header
payana_signed_url_content_type = payana_service_constants.payana_signed_url_content_type


@payana_service_generic_exception_handler
def payana_profile_id_header_parser():

    profile_id_parser = reqparse.RequestParser()
    profile_id_parser.add_argument(
        payana_profile_id_header, location='headers')

    args = profile_id_parser.parse_args()
    profile_id = args[payana_profile_id_header]

    return profile_id


@payana_service_generic_exception_handler
def get_profile_id_header(request):

    profile_id = request.headers.get(payana_profile_id_header)

    return None if profile_id is None else profile_id.strip()

@payana_service_generic_exception_handler
def get_activity_id_header(request):

    activity_id = request.headers.get(payana_activity_id_header)

    return None if activity_id is None else activity_id.strip()

@payana_service_generic_exception_handler
def get_mail_id_header(request):

    mail_id = request.headers.get(payana_mail_id_header)

    return None if mail_id is None else mail_id.strip()

@payana_service_generic_exception_handler
def get_friend_id_header(request):

    friend_id = request.headers.get(payana_friend_id_header)

    return None if friend_id is None else friend_id.strip()

@payana_service_generic_exception_handler
def get_city_header(request):

    city = request.headers.get(payana_city_header)

    return None if city is None else city.strip()

@payana_service_generic_exception_handler
def get_autocomplete_header(request):

    autocomplete = request.headers.get(payana_autocomplete_header)

    return None if autocomplete is None else autocomplete.strip()

@payana_service_generic_exception_handler
def get_user_header(request):

    user = request.headers.get(payana_user_header)

    return None if user is None else user.strip()


@payana_service_generic_exception_handler
def get_country_header(request):

    country = request.headers.get(payana_country_header)

    return None if country is None else country.strip()


@payana_service_generic_exception_handler
def get_entity_id_header(request):

    entity_id = request.headers.get(payana_entity_id_header)

    return None if entity_id is None else entity_id.strip()


@payana_service_generic_exception_handler
def get_comment_id_header(request):

    comment_id = request.headers.get(payana_comment_id_header)

    return None if comment_id is None else comment_id.strip()


@payana_service_generic_exception_handler
def get_checkin_id_header(request):

    checkin_id = request.headers.get(payana_check_in_id_header)

    return None if checkin_id is None else checkin_id.strip()

@payana_service_generic_exception_handler
def get_excursion_id_header(request):

    excursion_id = request.headers.get(payana_excursion_id_header)

    return None if excursion_id is None else excursion_id.strip()

@payana_service_generic_exception_handler
def get_itinerary_id_header(request):

    itinerary_id = request.headers.get(payana_itinerary_id_header)

    return None if itinerary_id is None else itinerary_id.strip()

@payana_service_generic_exception_handler
def get_itinerary_name_header(request):

    itinerary_name = request.headers.get(payana_itinerary_name_header)

    return None if itinerary_name is None else itinerary_name.strip()

@payana_service_generic_exception_handler
def get_gcs_object_id_header(request):

    storage_object_id = request.headers.get(payana_signed_url_storage_object_header)

    return None if storage_object_id is None else storage_object_id.strip()

@payana_service_generic_exception_handler
def get_gcs_bucket_id_header(request):

    storage_bucket_id = request.headers.get(payana_signed_url_storage_bucket_header)

    return None if storage_bucket_id is None else storage_bucket_id.strip()

@payana_service_generic_exception_handler
def get_gcs_content_type_header(request):

    content_type = request.headers.get(payana_signed_url_content_type)

    return None if content_type is None else content_type