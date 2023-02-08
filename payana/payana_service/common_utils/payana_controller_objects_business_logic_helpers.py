#!/usr/bin/env python

"""Contains functions for parsers
"""

from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from flask_restx import reqparse
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler, payana_service_intermediate_exception_handler
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_profile_id_header = payana_service_constants.payana_profile_id_header


@payana_service_intermediate_exception_handler
def payana_profile_page_travel_footprint_read_parser(travelfont_obj):

    travelfont_return_obj = {}

    payana_profile_page_travel_footprint_excursion_id = bigtable_constants.payana_profile_page_travel_footprint_excursion_id
    payana_profile_page_travel_footprint_latitude = bigtable_constants.payana_profile_page_travel_footprint_latitude
    payana_profile_page_travel_footprint_longitude = bigtable_constants.payana_profile_page_travel_footprint_longitude
    payana_profile_page_travel_footprint_profile_id = bigtable_constants.payana_profile_page_travel_footprint_profile_id
    payana_profile_travel_footprint_obj_list = bigtable_constants.payana_profile_travel_footprint_obj_list
    payana_profile_page_travel_footprint_place_id = bigtable_constants.payana_profile_page_travel_footprint_place_id

    for profile_id, travelfont_obj in travelfont_obj.items():

        travelfont_return_obj[payana_profile_page_travel_footprint_profile_id] = profile_id
        travelfont_return_obj[payana_profile_travel_footprint_obj_list] = []

        for _, travelfont_valueobj in travelfont_obj.items():

            for travelfont_valueobj_key, travelfont_valueobj_value in travelfont_valueobj.items():

                place_id, excursion_id = travelfont_valueobj_key.split("##")
                latitude, longitude = travelfont_valueobj_value.split("##")

                travelfont_return_temp = {}

                travelfont_return_temp[payana_profile_page_travel_footprint_place_id] = place_id
                travelfont_return_temp[payana_profile_page_travel_footprint_excursion_id] = excursion_id
                travelfont_return_temp[payana_profile_page_travel_footprint_latitude] = latitude
                travelfont_return_temp[payana_profile_page_travel_footprint_longitude] = longitude

                travelfont_return_obj[payana_profile_travel_footprint_obj_list].append(
                    travelfont_return_temp)

    return travelfont_return_obj


@payana_service_intermediate_exception_handler
def payana_profile_page_travel_footprint_delete_parser(travelfont_obj):

    travelfont_delete_obj = {}

    payana_profile_page_travel_footprint_excursion_id = bigtable_constants.payana_profile_page_travel_footprint_excursion_id
    payana_profile_page_travel_footprint_latitude = bigtable_constants.payana_profile_page_travel_footprint_latitude
    payana_profile_page_travel_footprint_longitude = bigtable_constants.payana_profile_page_travel_footprint_longitude
    payana_profile_page_travel_footprint_column_family = bigtable_constants.payana_profile_page_travel_footprint_column_family
    payana_profile_page_travel_footprint_place_id = bigtable_constants.payana_profile_page_travel_footprint_place_id

    for _, travelfont_obj in travelfont_obj.items():

        if payana_profile_page_travel_footprint_column_family not in travelfont_delete_obj.keys():
            travelfont_delete_obj[payana_profile_page_travel_footprint_column_family] = {
            }

        for travelfont_valueobj in travelfont_obj:
            place_id = travelfont_valueobj[payana_profile_page_travel_footprint_place_id]
            excursion_id = travelfont_valueobj[payana_profile_page_travel_footprint_excursion_id]
            latitude = travelfont_valueobj[payana_profile_page_travel_footprint_latitude]
            longitude = travelfont_valueobj[payana_profile_page_travel_footprint_longitude]

            payana_profile_page_travel_footprint_column_qualifier = "##".join(
                [str(place_id), str(excursion_id)])

            payana_profile_page_travel_footprint_column_value = "##".join(
                [str(latitude), str(longitude)])

            travelfont_delete_obj[payana_profile_page_travel_footprint_column_family][
                payana_profile_page_travel_footprint_column_qualifier] = payana_profile_page_travel_footprint_column_value

    return travelfont_delete_obj


@payana_service_intermediate_exception_handler
def payana_entity_comments_object_builder(entity_id, comment_id, comment_timestamp):

    payana_entity_comment_obj = {}

    payana_comments_table_entity_id = bigtable_constants.payana_comments_table_entity_id
    payana_entity_to_comments_table_comment_id_list = bigtable_constants.payana_entity_to_comments_table_comment_id_list

    payana_entity_comment_obj[payana_comments_table_entity_id] = entity_id
    payana_entity_comment_obj[payana_entity_to_comments_table_comment_id_list] = {
        comment_id: comment_timestamp
    }

    return payana_entity_comment_obj

def payana_comment_obj_delete_builder(payana_entity_comments_read_obj_dict):
    
    payana_comments_table_delete_wrappers = []
    
    for _, payana_comment_obj_dict in payana_entity_comments_read_obj_dict.items():
        
        for comment_id, _ in payana_comment_obj_dict.items():
            
            payana_comments_table_delete_wrapper = bigtable_write_object_wrapper(
                    comment_id, "", "", "")
            
            payana_comments_table_delete_wrappers.append(payana_comments_table_delete_wrapper)
            
    return payana_comments_table_delete_wrappers