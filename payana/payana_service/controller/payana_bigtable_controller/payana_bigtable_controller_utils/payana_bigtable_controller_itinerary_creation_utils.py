#!/usr/bin/env python

"""Demonstrates how to create a bigtable cluster, connect to Cloud Bigtable instance,
create and write a table, read from the table
"""
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_bl.bigtable_utils.PayanaCheckinTable import PayanaCheckinTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler


@payana_service_generic_exception_handler
def get_profile_page_itinerary_table(profile_id):

    payana_profile_page_itinerary_table = bigtable_constants.payana_profile_page_itinerary_table

    payana_profile_page_itinerary_read_obj = PayanaBigTable(
        payana_profile_page_itinerary_table)

    row_key = str(profile_id)

    payana_profile_page_itinerary_read_obj_dict = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_key, include_column_family=True)

    return payana_profile_page_itinerary_read_obj_dict


@payana_service_generic_exception_handler
def get_itinerary_object(itinerary_id):

    payana_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_itinerary_table)

    row_key = str(itinerary_id)

    payana_itinerary_obj = payana_itinerary_read_obj.get_row_dict(
        row_key, include_column_family=True)

    return payana_itinerary_obj


@payana_service_generic_exception_handler
def update_itinerary_object(itinerary_id, payana_itinerary_object):

    payana_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_itinerary_table)

    payana_itinerary_obj_write_status = payana_itinerary_read_obj.insert_columns_column_family(
        itinerary_id, payana_itinerary_object)

    return payana_itinerary_read_obj, payana_itinerary_obj_write_status


@ payana_service_generic_exception_handler
def delete_excursion_object(excursion_id):

    profile_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    payana_excursion_obj_delete_status = profile_excursion_read_obj.delete_bigtable_row_with_row_key(
        excursion_id)

    return payana_excursion_obj_delete_status


@ payana_service_generic_exception_handler
def delete_itinerary_object(itinerary_id, payana_itinerary_object):

    payana_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_itinerary_table)

    payana_itinerary_obj_delete_status = payana_itinerary_read_obj.delete_bigtable_row_column_list(
        itinerary_id, payana_itinerary_object)

    return payana_itinerary_obj_delete_status


@ payana_service_generic_exception_handler
def delete_profile_page_itinerary_object_column_values(payana_profile_page_itinerary_table_delete_wrappers):

    payana_profile_page_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_profile_page_itinerary_table)

    payana_profile_page_itinerary_obj_delete_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_columns(
        payana_profile_page_itinerary_table_delete_wrappers)

    return payana_profile_page_itinerary_obj_delete_status


@ payana_service_generic_exception_handler
def create_checkin_object(payana_checkin_object):

    payana_checkin_object = PayanaCheckinTable(**payana_checkin_object)
    payana_checkin_obj_write_status = payana_checkin_object.update_checkin_bigtable()

    return payana_checkin_object, payana_checkin_obj_write_status


@ payana_service_generic_exception_handler
def update_checkin_object(checkin_id, payana_checkin_object):

    payana_checkin_read_obj = PayanaBigTable(
        bigtable_constants.payana_checkin_table)

    payana_checkin_obj_edit_status = payana_checkin_read_obj.insert_columns_column_family(
        checkin_id, payana_checkin_object)

    return payana_checkin_obj_edit_status


@ payana_service_generic_exception_handler
def delete_checkin_object(checkin_id):
    payana_checkin_read_obj = PayanaBigTable(
        bigtable_constants.payana_checkin_table)

    payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_with_row_key(
        checkin_id)

    return payana_checkin_obj_delete_status


@ payana_service_generic_exception_handler
def update_excursion_metadata_object(excursion_id, payana_excursion_object):
    payana_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    payana_excursion_obj_write_status = payana_excursion_read_obj.insert_columns_column_family(
        excursion_id, payana_excursion_object)

    return payana_excursion_read_obj, payana_excursion_obj_write_status


@ payana_service_generic_exception_handler
def delete_excursion_metadata_object(excursion_id, payana_excursion_object):
    payana_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row_column_list(
        excursion_id, payana_excursion_object)

    return payana_excursion_obj_delete_status


@ payana_service_generic_exception_handler
def create_itinerary_metadata_object(profile_itinerary_read_obj):

    payana_itinerary_object = PayanaItineraryTable(
        **profile_itinerary_read_obj)

    payana_itinerary_obj_write_status = payana_itinerary_object.update_itinerary_bigtable()

    return payana_itinerary_object, payana_itinerary_obj_write_status


@ payana_service_generic_exception_handler
def create_profile_page_itinerary_object(profile_page_itinerary_read_obj):

    payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
        **profile_page_itinerary_read_obj)

    payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

    return payana_profile_page_itinerary_object, payana_profile_page_itinerary_obj_write_status


@ payana_service_generic_exception_handler
def get_excursion_object(excursion_id):

    payana_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    row_key = str(excursion_id)

    payana_excursion_obj = payana_excursion_read_obj.get_row_dict(
        row_key, include_column_family=True)

    return payana_excursion_obj


@ payana_service_generic_exception_handler
def create_excursion_object(profile_excursion_read_obj):

    payana_excursion_object = PayanaExcursionTable(
        **profile_excursion_read_obj)

    payana_excursion_obj_write_status = payana_excursion_object.update_excursion_bigtable()

    return payana_excursion_object, payana_excursion_obj_write_status


@ payana_service_generic_exception_handler
def get_checkin_object(checkin_id):

    payana_checkin_read_obj = PayanaBigTable(
        bigtable_constants.payana_checkin_table)

    row_key = str(checkin_id)

    payana_checkin_read_obj_dict = payana_checkin_read_obj.get_row_dict(
        row_key, include_column_family=True)

    return payana_checkin_read_obj_dict


@ payana_service_generic_exception_handler
def update_excursion_object(excursion_id, payana_excursion_object):

    payana_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    payana_excursion_obj_write_status = payana_excursion_read_obj.insert_columns_column_family(
        excursion_id, payana_excursion_object)

    return payana_excursion_obj_write_status


@ payana_service_generic_exception_handler
def delete_excursion_column_value(excursion_id, payana_excursion_object):

    payana_excursion_read_obj = PayanaBigTable(
        bigtable_constants.payana_excursion_table)

    payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row_column_list(
        excursion_id, payana_excursion_object)

    return payana_excursion_obj_delete_status


@ payana_service_generic_exception_handler
def delete_checkin_column_value(checkin_id, payana_checkin_object):

    payana_checkin_read_obj = PayanaBigTable(
        bigtable_constants.payana_checkin_table)

    payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_column_list(
        checkin_id, payana_checkin_object)

    return payana_checkin_obj_delete_status


@ payana_service_generic_exception_handler
def delete_checkin_row(checkin_id):

    payana_checkin_read_obj = PayanaBigTable(
        bigtable_constants.payana_checkin_table)

    payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_with_row_key(
        checkin_id)

    return payana_checkin_obj_delete_status


@ payana_service_generic_exception_handler
def delete_profile_page_itinerary_table_entity_id(profile_id, profile_page_itinerary_object):
    payana_profile_page_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_profile_page_itinerary_table)

    payana_profile_page_itinerary_table_delete_wrappers = []

    for column_family, column_family_dict in profile_page_itinerary_object.items():

        for activity in bigtable_constants.payana_activity_column_family:
            activity_column_family_mapping = "_".join(
                [activity, column_family])

            # Delete specific column family and column values
            for column_quantifier, column_value in column_family_dict.items():
                payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                    profile_id, activity_column_family_mapping, column_quantifier, column_value)

                payana_profile_page_itinerary_table_delete_wrappers.append(
                    payana_profile_page_itinerary_table_delete_wrapper)

    payana_profile_page_itinerary_obj_delete_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_columns(
        payana_profile_page_itinerary_table_delete_wrappers)

    return payana_profile_page_itinerary_obj_delete_status


@ payana_service_generic_exception_handler
def delete_itinerary_object(itinerary_id):
    profile_itinerary_read_obj = PayanaBigTable(
        bigtable_constants.payana_itinerary_table)

    payana_itinerary_obj_delete_status = profile_itinerary_read_obj.delete_bigtable_row_with_row_key(
        itinerary_id)
    
    return payana_itinerary_obj_delete_status
