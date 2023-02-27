#!/usr/bin/env python

"""Contains functions for parsers
"""

from flask_restx import reqparse
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler

payana_profile_id_header = payana_service_constants.payana_profile_id_header


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

    profile_id = request.headers.get('profile_id')

    return None if profile_id is None else profile_id.strip()


@payana_service_generic_exception_handler
def get_entity_id_header(request):

    entity_id = request.headers.get('entity_id')

    return None if entity_id is None else entity_id.strip()


@payana_service_generic_exception_handler
def get_comment_id_header(request):

    comment_id = request.headers.get('comment_id')

    return None if comment_id is None else comment_id.strip()


@payana_service_generic_exception_handler
def get_checkin_id_header(request):

    checkin_id = request.headers.get('checkin_id')

    return None if checkin_id is None else checkin_id.strip()
