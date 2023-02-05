#!/usr/bin/env python

"""Contains functions for parsers
"""

from flask_restx import reqparse
from payana.payana_service.constants import payana_service_constants

payana_profile_id_header = payana_service_constants.payana_profile_id_header

def payana_profile_id_header_parser():

    profile_id_parser = reqparse.RequestParser()
    profile_id_parser.add_argument(payana_profile_id_header, location='headers')

    args = profile_id_parser.parse_args()
    profile_id = args[payana_profile_id_header]

    return profile_id

def get_profile_id_header(request):
    
    profile_id = request.headers.get('profile_id')
    
    return profile_id.strip()

def get_entity_id_header(request):
    
    entity_id = request.headers.get('entity_id')
    
    return entity_id.strip()