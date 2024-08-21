import copy
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json
import random

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_excursion_id_header, get_profile_id_header, get_itinerary_id_header, get_itinerary_name_header, get_city_header, get_activity_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.models.payana_bigtable_models.payana_itinerary_flow_model import payana_excursion_object_model, payana_itinerary_object_model, profile_page_itinerary_model
from payana.payana_service.controller.payana_bigtable_controller.payana_bigtable_controller_utils.payana_bigtable_controller_itinerary_creation_utils import get_profile_page_itinerary_table, get_itinerary_object, delete_excursion_object, delete_itinerary_object, delete_profile_page_itinerary_object_column_values, get_excursion_object, update_excursion_metadata_object, create_excursion_object, create_profile_page_itinerary_object, delete_checkin_object, delete_profile_page_itinerary_table_entity_id, update_itinerary_object
from payana.payana_bl.cloud_storage_utils.payana_generate_gcs_signed_url import payana_generate_download_signed_url

payana_excursion_objects_name_space = Namespace(
    'excursion', description='Manage the CRUD operations of the excursion table')

payana_excursion_objects_write_success_message_post = payana_service_constants.payana_excursion_objects_write_success_message_post
payana_excursion_objects_write_success_message_put = payana_service_constants.payana_excursion_objects_write_success_message_put
payana_excursion_objects_write_failure_message_post = payana_service_constants.payana_excursion_objects_write_failure_message_post
payana_excursion_objects_create_failure_message_post = payana_service_constants.payana_excursion_objects_create_failure_message_post
payana_excursion_objects_delete_failure_message = payana_service_constants.payana_excursion_objects_delete_failure_message
payana_excursion_objects_values_delete_success_message = payana_service_constants.payana_excursion_objects_values_delete_success_message
payana_excursion_objects_values_delete_failure_message = payana_service_constants.payana_excursion_objects_values_delete_failure_message
payana_excursion_objects_delete_success_message = payana_service_constants.payana_excursion_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_excursion_id_header = payana_service_constants.payana_excursion_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_excursion_objects_header_exception = payana_service_constants.payana_missing_excursion_objects_header_exception
payana_missing_excursion_object = payana_service_constants.payana_missing_excursion_object
payana_excursion_table = bigtable_constants.payana_excursion_table


@payana_excursion_objects_name_space.route("/")
class PayanaExcursionObjectEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        row_key = str(excursion_id)

        payana_excursion_obj = payana_excursion_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_excursion_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        return payana_excursion_obj, payana_200

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_excursion_read_obj = request.json

        payana_excursion_object = PayanaExcursionTable(
            **profile_excursion_read_obj)
        payana_excursion_obj_write_status = payana_excursion_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        excursion_id = payana_excursion_object.excursion_id

        return {
            status: payana_201_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)

        payana_excursion_obj_write_status = payana_excursion_read_obj.insert_columns_column_family(
            excursion_id, payana_excursion_object)

        if not payana_excursion_obj_write_status:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/")
class PayanaExcursionObjectRowDeleteEndPoint(Resource):
    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        payana_excursion_obj_delete_status = profile_excursion_read_obj.delete_bigtable_row_with_row_key(
            excursion_id)

        if not payana_excursion_obj_delete_status:
            raise Exception(
                payana_excursion_objects_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/values/")
class PayanaExcursionObjectColumnValuesDeleteEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        if payana_excursion_object is None:
            raise KeyError(payana_missing_excursion_object,
                           payana_excursion_objects_name_space)

        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row_column_list(
            excursion_id, payana_excursion_object)

        if not payana_excursion_obj_delete_status:
            raise Exception(
                payana_excursion_objects_values_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/cf/")
class PayanaExcursionObjectColumnFamilyDeleteEndPoint(Resource):
    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        if payana_excursion_object is None:
            raise KeyError(payana_missing_excursion_object,
                           payana_excursion_objects_name_space)

        payana_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_table)

        for column_family, _ in payana_excursion_object.items():

            payana_excursion_delete_wrapper = bigtable_write_object_wrapper(
                excursion_id, column_family, "", "")

            payana_excursion_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column_family_cells(
                payana_excursion_delete_wrapper)

            if not payana_excursion_obj_delete_status:
                raise Exception(
                    payana_excursion_objects_values_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/create/")
class PayanaExcursionTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        payana_itinerary_create_payload = request.json

        # Step 1 - Create an excursion object
        profile_excursion_read_obj = copy.deepcopy(
            payana_excursion_object_model)

        profile_excursion_read_obj[bigtable_constants.payana_excursion_activities_list] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_activities_list]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_activity_guide] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_activity_guide]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_create_timestamp] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_last_updated_timestamp] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_description] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]
        # profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
        #     bigtable_constants.payana_excursion_itinerary_position] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_itinerary_position]

        payana_excursion_object = PayanaExcursionTable(
            **profile_excursion_read_obj)
        payana_excursion_object.generate_excursion_id()

        excursion_id = payana_excursion_object.excursion_id
        excursion_name = payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]

        if excursion_id is None or len(excursion_id) == 0:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Step 2 - Get profile Itinerary object
        row_key = str(
            payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id])

        payana_profile_page_itinerary_read_obj_dict = get_profile_page_itinerary_table(
            payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id])

        itinerary_name = ", ".join(
            payana_itinerary_create_payload[bigtable_constants.payana_itinerary_column_family_cities_list])

        running_itinerary_count = 0
        itinerary_id = ""

        if payana_profile_page_itinerary_read_obj_dict is not None and not len(payana_profile_page_itinerary_read_obj_dict) == 0:

            # Step 3 - Find the itinerary ID/count
            column_qualifier = "_".join([bigtable_constants.payana_generic_activity_column_family,
                                        bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value])

            if column_qualifier in payana_profile_page_itinerary_read_obj_dict[row_key] and itinerary_name in payana_profile_page_itinerary_read_obj_dict[row_key][column_qualifier]:
                itinerary_id = payana_profile_page_itinerary_read_obj_dict[
                    row_key][column_qualifier][itinerary_name]

            # Step 4 - Get the excursion count itinerary object (if it exists)
            if itinerary_id is not None and not len(itinerary_id) == 0:
                row_key = str(itinerary_id)

                payana_itinerary_obj = get_itinerary_object(itinerary_id)

                if len(payana_itinerary_obj) == 0:
                    raise KeyError(payana_empty_row_read_exception,
                                   payana_excursion_objects_name_space)

                running_itinerary_count = max([int(iter) for iter in payana_itinerary_obj[itinerary_id]
                                              [bigtable_constants.payana_itinerary_column_family_excursion_id_list].keys()])

        running_itinerary_count += 1
        payana_excursion_object.excursion_itinerary_position = str(
            running_itinerary_count)

        # Step 5 - Create an itinerary object
        profile_itinerary_read_obj = copy.deepcopy(
            payana_itinerary_object_model)

        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_column_family_excursion_id_list] = {
            str(running_itinerary_count): excursion_id}
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_activities_list] = payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][
            bigtable_constants.payana_itinerary_column_family_description] = itinerary_name

        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][
            bigtable_constants.payana_itinerary_column_family_itinerary_owner_profile_id] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][bigtable_constants.payana_itinerary_last_updated_timestamp] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_column_family_cities_list] = payana_itinerary_create_payload[
            bigtable_constants.payana_itinerary_column_family_cities_list]

        payana_itinerary_object = PayanaItineraryTable(
            **profile_itinerary_read_obj)

        if itinerary_id is None or len(itinerary_id) == 0:
            payana_itinerary_object.generate_itinerary_id()
        else:
            payana_itinerary_object.itinerary_id = itinerary_id

        itinerary_id = payana_itinerary_object.itinerary_id

        # Step 6 - Update itinerary ID/Name in excursion object
        payana_excursion_object.excursion_itinerary_id = itinerary_id
        payana_excursion_object.excursion_itinerary_name = itinerary_name

        # Step 7 - Add to the user's profile itinerary list object
        profile_page_itinerary_read_obj = copy.deepcopy(
            profile_page_itinerary_model)

        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_profile_id] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value] = {
            itinerary_name: itinerary_id}

        if payana_itinerary_create_payload[bigtable_constants.payana_excursion_activity_guide].lower() == "true":
            profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value] = {
                payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]: excursion_id}
        else:
            profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value] = {
                payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]: excursion_id}

        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(
            payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list].keys())

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_read_obj)

        # Step 8 - BigTable write across all 3 tables - excursion, itinerary, profile itinerary table
        # Excursion table
        payana_excursion_obj_write_status = payana_excursion_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Itinerary table
        payana_itinerary_obj_write_status = payana_itinerary_object.update_itinerary_bigtable()

        if not payana_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table column value entry
            payana_revert_itinerary_object = {
                bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
                    str(running_itinerary_count): excursion_id}
            }

            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_revert_itinerary_object)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            raise Exception(
                payana_service_constants.payana_itinerary_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Profile itinerary table
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

        if not payana_profile_page_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table object
            payana_revert_itinerary_object = {
                bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
                    str(running_itinerary_count): excursion_id}
            }
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_revert_itinerary_object)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete profile page itinerary object
            payana_profile_page_itinerary_table_delete_wrappers = []

            column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value

            if payana_itinerary_create_payload[bigtable_constants.payana_excursion_activity_guide].lower() == "true":
                column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value

            profile_page_itinerary_reversion_object = {
                column_family_mapping_quantifier_value: {excursion_name: excursion_id}}

            for column_family, column_family_dict in profile_page_itinerary_reversion_object.items():

                for activity in [bigtable_constants.payana_generic_activity_column_family] + list(payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list].keys()):
                    activity_column_family_mapping = "_".join(
                        [activity, column_family])

                    # Delete specific column family and column values
                    for column_quantifier, column_value in column_family_dict.items():
                        payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                            payana_itinerary_create_payload[
                                bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id], activity_column_family_mapping, column_quantifier, column_value)

                        payana_profile_page_itinerary_table_delete_wrappers.append(
                            payana_profile_page_itinerary_table_delete_wrapper)

            payana_profile_page_itinerary_obj_delete_status = delete_profile_page_itinerary_object_column_values(
                payana_profile_page_itinerary_table_delete_wrappers)

            if not payana_profile_page_itinerary_obj_delete_status:
                # Add logging
                pass

            raise Exception(
                payana_service_constants.payana_profile_page_itineraries_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_201_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201


@payana_excursion_objects_name_space.route("/edit/metadata/")
class PayanaExcursionObjectTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_service_constants.payana_missing_profile_id_header_exception,
                           payana_excursion_objects_name_space)

        # Step 1 - Fetch existing excursion object
        payana_excursion_existing_obj = get_excursion_object(excursion_id)
        payana_excursion_existing_obj = payana_excursion_existing_obj[excursion_id]

        if len(payana_excursion_existing_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        # Step 2 - Update the excursion object
        payana_excursion_object = request.json
        payana_excursion_new_obj, payana_excursion_obj_write_status = update_excursion_metadata_object(
            excursion_id, payana_excursion_object)

        if not payana_excursion_obj_write_status:
            # Revert to previous excursion object
            create_excursion_object(payana_excursion_existing_obj)

            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Step 3 - If the update is description (excursion name) or activities_list, update the profile itinerary object
        # 3A - update the new description/name with new activities if changed, or the old activity set if unchanged
        if (bigtable_constants.payana_excursion_metadata in payana_excursion_object
                and bigtable_constants.payana_excursion_column_family_description in payana_excursion_object[bigtable_constants.payana_excursion_metadata]) or bigtable_constants.payana_excursion_activities_list in payana_excursion_object:

            profile_page_itinerary_obj = copy.deepcopy(
                profile_page_itinerary_model)

            profile_page_itinerary_obj[bigtable_constants.payana_profile_table_profile_id] = profile_id

            existing_description = payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][
                bigtable_constants.payana_excursion_column_family_description]

            new_description = existing_description

            if (bigtable_constants.payana_excursion_metadata in payana_excursion_object
                    and bigtable_constants.payana_excursion_column_family_description in payana_excursion_object[bigtable_constants.payana_excursion_metadata]):
                new_description = payana_excursion_object[bigtable_constants.payana_excursion_metadata][
                    bigtable_constants.payana_excursion_column_family_description]

            if payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_activity_guide]:
                profile_page_itinerary_obj[bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value] = {
                    new_description: excursion_id
                }
            else:
                profile_page_itinerary_obj[bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value] = {
                    new_description: excursion_id
                }

            if bigtable_constants.payana_excursion_activities_list in payana_excursion_object:
                profile_page_itinerary_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(payana_excursion_object[
                    bigtable_constants.payana_excursion_activities_list].keys())
            else:
                profile_page_itinerary_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(payana_excursion_existing_obj[
                    bigtable_constants.payana_excursion_activities_list].keys())

            _, payana_profile_page_itinerary_obj_write_status = create_profile_page_itinerary_object(
                profile_page_itinerary_obj)

            # 4B - delete the existing description/name of the existing activities
            if payana_profile_page_itinerary_obj_write_status and bigtable_constants.payana_excursion_column_family_description in payana_excursion_object[bigtable_constants.payana_excursion_metadata]:
                payana_profile_page_itinerary_table_delete_wrappers = []

                existing_activities = payana_excursion_existing_obj[
                    bigtable_constants.payana_excursion_activities_list]

                for activity in [bigtable_constants.payana_generic_activity_column_family] + list(existing_activities.keys()):
                    if payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_activity_guide]:
                        activity_cf = "_".join([activity,
                                                bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value])
                    else:
                        activity_cf = "_".join([activity,
                                                bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value])

                    payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(profile_id, activity_cf,
                                                                                                       existing_description, excursion_id)

                    payana_profile_page_itinerary_table_delete_wrappers.append(
                        payana_profile_page_itinerary_table_delete_wrapper)

                _ = delete_profile_page_itinerary_object_column_values(
                    payana_profile_page_itinerary_table_delete_wrappers)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/excursion/")
class PayanaExcursionObjectDeleteTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_profile_id_header_exception, payana_excursion_objects_name_space)

        # Step 1 - Fetch existing excursion object
        payana_excursion_existing_obj = get_excursion_object(excursion_id)
        payana_excursion_existing_obj = payana_excursion_existing_obj[excursion_id]

        if len(payana_excursion_existing_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        # Step 2 - Delete excursion object
        payana_excursion_obj_delete_status = delete_excursion_object(
            excursion_id)

        if not payana_excursion_obj_delete_status:
            # revert excursion object
            raise Exception(
                payana_excursion_objects_delete_failure_message, payana_excursion_objects_name_space)

        # Step 3 - Delete all checkin objects
        if bigtable_constants.payana_excursion_column_family_checkin_id_list in payana_excursion_existing_obj:
            checkin_id_list = payana_excursion_existing_obj[
                bigtable_constants.payana_excursion_column_family_checkin_id_list]

            for _, checkin_id in checkin_id_list.items():
                delete_checkin_object_status = delete_checkin_object(
                    checkin_id)

                if not delete_checkin_object_status:
                    # Add logging to auto-handle later
                    pass

        # Step 4 - Update Itinerary object by removing the excursion ID
        payana_itinerary_delete_obj = {bigtable_constants.payana_itinerary_column_family_excursion_id_list: {payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_position]: payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_id]}}

        payana_delete_itinerary_object_status = delete_itinerary_object(payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata]
                                                                        [bigtable_constants.payana_excursion_itinerary_id], payana_itinerary_delete_obj)

        if payana_delete_itinerary_object_status:
            # Add logging to auto-handle later
            pass

        # Step 5 - Update profile page itinerary object
        profile_page_itinerary_object = {}

        if not payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_activity_guide].lower() == "true":
            profile_page_itinerary_object[bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value] = {
                payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_description]: excursion_id}
            profile_page_itinerary_object[bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value] = {
                payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_description]: excursion_id}
        else:
            profile_page_itinerary_object[bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value] = {
                payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_description]: excursion_id}
            profile_page_itinerary_object[bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value] = {
                payana_excursion_existing_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_description]: excursion_id}

        payana_delete_profile_page_itinerary_table_entity_id_status = delete_profile_page_itinerary_table_entity_id(
            profile_id, profile_page_itinerary_object)

        if not payana_delete_profile_page_itinerary_table_entity_id_status:
            # Add logging to auto-handle later
            pass

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/clone/")
class PayanaExcursionTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_itinerary_objects_header_exception, payana_excursion_objects_name_space)

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_profile_id_header_exception, payana_excursion_objects_name_space)

        # Step 1 - Get excursion object
        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        excursion_id = str(excursion_id)

        payana_excursion_obj = payana_excursion_read_obj.get_row_dict(
            excursion_id, include_column_family=True)

        if len(payana_excursion_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        payana_excursion_obj = payana_excursion_obj[excursion_id]

        # Step 2 - Get itinerary object
        payana_itinerary_read_obj = PayanaBigTable(
            bigtable_constants.payana_itinerary_table)

        itinerary_id = str(itinerary_id)

        payana_itinerary_obj = payana_itinerary_read_obj.get_row_dict(
            itinerary_id, include_column_family=True)

        if len(payana_itinerary_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        payana_itinerary_obj = payana_itinerary_obj[itinerary_id]

        # Step 3 - Get profile itinerary object
        payana_profile_page_itinerary_read_obj = PayanaBigTable(
            bigtable_constants.payana_profile_page_itinerary_table)

        profile_id = str(profile_id)

        payana_profile_page_itinerary_read_obj_dict = payana_profile_page_itinerary_read_obj.get_row_dict(
            profile_id, include_column_family=True)

        if len(payana_profile_page_itinerary_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        # Step 4 - Clone the excursion object
        payana_excursion_clone_obj = copy.deepcopy(payana_excursion_obj)

        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_id] = ""
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_id] = str(itinerary_id)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_itinerary_name] = payana_itinerary_obj[
            bigtable_constants.payana_itinerary_metadata][bigtable_constants.payana_itinerary_column_family_description]

        new_excursion_running_count = max([int(iter) for iter in payana_itinerary_obj
                                           [bigtable_constants.payana_itinerary_column_family_excursion_id_list].keys()]) + 1
        new_excursion_running_count = str(new_excursion_running_count)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_position] = new_excursion_running_count

        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id] = str(profile_id)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_column_family_participants_list] = {
        }
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_clone_parent_id] = excursion_id

        # Step 5 - Generate new excursion ID
        payana_excursion_clone_object = PayanaExcursionTable(
            **payana_excursion_clone_obj)
        payana_excursion_clone_object.generate_excursion_id()

        new_excursion_id = payana_excursion_clone_object.excursion_id
        new_excursion_name = payana_excursion_clone_object.description

        # Step 6 - prepare the itinerary edit object
        payana_itinerary_edit_obj = {bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
            new_excursion_running_count: new_excursion_id}}

        # Step 7 - prepare the profile page itinerary object
        profile_page_itinerary_edit_obj = copy.deepcopy(
            profile_page_itinerary_model)

        profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_profile_id] = profile_id

        if payana_excursion_clone_object.activity_guide.lower() == "true":
            profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value] = {
                new_excursion_name: new_excursion_id}
        else:
            profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value] = {
                new_excursion_name: new_excursion_id}

        profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(
            payana_excursion_clone_object.activities_list.keys())

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_edit_obj)

        # Step 8 - BigTable write across all 3 tables - excursion, itinerary, profile itinerary table
        # Excursion table
        payana_excursion_obj_write_status = payana_excursion_clone_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                new_excursion_id)

            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Itinerary table
        payana_itinerary_obj_write_status = update_itinerary_object(
            itinerary_id, payana_itinerary_edit_obj)

        if not payana_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table column value entry
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_itinerary_edit_obj)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            raise Exception(
                payana_service_constants.payana_itinerary_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Profile itinerary table
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

        if not payana_profile_page_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table object
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_itinerary_edit_obj)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete profile page itinerary object
            payana_profile_page_itinerary_table_delete_wrappers = []

            column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value

            if payana_excursion_clone_object.activity_guide.lower() == "true":
                column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value

            profile_page_itinerary_reversion_object = {
                column_family_mapping_quantifier_value: {new_excursion_name: new_excursion_id}}

            for column_family, column_family_dict in profile_page_itinerary_reversion_object.items():

                for activity in [bigtable_constants.payana_generic_activity_column_family] + list(payana_excursion_clone_object.activities_list.keys()):
                    activity_column_family_mapping = "_".join(
                        [activity, column_family])

                    # Delete specific column family and column values
                    for column_quantifier, column_value in column_family_dict.items():
                        payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                            profile_id, activity_column_family_mapping, column_quantifier, column_value)

                        payana_profile_page_itinerary_table_delete_wrappers.append(
                            payana_profile_page_itinerary_table_delete_wrapper)

            payana_profile_page_itinerary_obj_delete_status = delete_profile_page_itinerary_object_column_values(
                payana_profile_page_itinerary_table_delete_wrappers)

            if not payana_profile_page_itinerary_obj_delete_status:
                # Add logging
                pass

            raise Exception(
                payana_service_constants.payana_profile_page_itineraries_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_201_response,
            payana_excursion_id_header: new_excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201


@payana_excursion_objects_name_space.route("/clone/new/")
class PayanaExcursionTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_profile_id_header_exception, payana_excursion_objects_name_space)

        itinerary_name = get_itinerary_name_header(request)

        if itinerary_name is None or len(itinerary_name) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_itinerary_objects_header_exception, payana_excursion_objects_name_space)

        # Step 1 - Get excursion object
        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        excursion_id = str(excursion_id)

        payana_excursion_obj = payana_excursion_read_obj.get_row_dict(
            excursion_id, include_column_family=True)

        if len(payana_excursion_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        payana_excursion_obj = payana_excursion_obj[excursion_id]

        # Step 2 - Create an itinerary object template
        profile_itinerary_read_obj = copy.deepcopy(
            payana_itinerary_object_model)

        payana_itinerary_object = PayanaItineraryTable(
            **profile_itinerary_read_obj)
        payana_itinerary_object.generate_itinerary_id()
        payana_itinerary_object.description = itinerary_name

        itinerary_id = str(payana_itinerary_object.itinerary_id)

        # Step 3 - Get profile itinerary object
        # payana_profile_page_itinerary_read_obj = PayanaBigTable(
        #     bigtable_constants.payana_profile_page_itinerary_table)

        # profile_id = str(profile_id)

        # payana_profile_page_itinerary_read_obj_dict = payana_profile_page_itinerary_read_obj.get_row_dict(
        #     profile_id, include_column_family=True)

        # if len(payana_profile_page_itinerary_read_obj_dict) == 0:
        #     payana_profile_page_itinerary_read_obj_dict = {}

        # Step 4 - Clone the excursion object
        payana_excursion_clone_obj = copy.deepcopy(payana_excursion_obj)

        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_id] = ""
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_id] = str(itinerary_id)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_name] = itinerary_name

        new_excursion_running_count = 1
        new_excursion_running_count = str(new_excursion_running_count)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_itinerary_position] = new_excursion_running_count

        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id] = str(profile_id)
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_column_family_participants_list] = {
        }
        payana_excursion_clone_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_clone_parent_id] = excursion_id

        # Step 5 - Generate new excursion ID
        payana_excursion_clone_object = PayanaExcursionTable(
            **payana_excursion_clone_obj)
        payana_excursion_clone_object.generate_excursion_id()

        new_excursion_id = payana_excursion_clone_object.excursion_id
        new_excursion_name = payana_excursion_clone_object.description

        # Step 6 - prepare the itinerary edit object
        payana_itinerary_edit_obj = {bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
            new_excursion_running_count: new_excursion_id}}

        payana_itinerary_object.excursion_id_list = payana_itinerary_edit_obj[
            bigtable_constants.payana_itinerary_column_family_excursion_id_list]

        payana_itinerary_object.itinerary_owner_profile_id = profile_id
        payana_itinerary_object.activities_list = payana_excursion_clone_object.activities_list

        # Step 7 - prepare the profile page itinerary object
        profile_page_itinerary_edit_obj = copy.deepcopy(
            profile_page_itinerary_model)

        profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_profile_id] = profile_id

        if payana_excursion_clone_object.activity_guide.lower() == "true":
            profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value] = {
                new_excursion_name: new_excursion_id}
        else:
            profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value] = {
                new_excursion_name: new_excursion_id}

        profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_saved_itinerary_id_mapping_quantifier_value] = {
            itinerary_name: itinerary_id}

        profile_page_itinerary_edit_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(
            payana_excursion_clone_object.activities_list.keys())

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_edit_obj)

        # Step 8 - BigTable write across all 3 tables - excursion, itinerary, profile itinerary table
        # Excursion table
        payana_excursion_obj_write_status = payana_excursion_clone_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                new_excursion_id)

            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Itinerary table
        payana_itinerary_obj_write_status = payana_itinerary_object.update_itinerary_bigtable()

        if not payana_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table column value entry
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_itinerary_edit_obj)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            raise Exception(
                payana_service_constants.payana_itinerary_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Profile itinerary table
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

        if not payana_profile_page_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table object
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_itinerary_edit_obj)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete profile page itinerary object
            payana_profile_page_itinerary_table_delete_wrappers = []

            column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value

            if payana_excursion_clone_object.activity_guide.lower() == "true":
                column_family_mapping_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value

            profile_page_itinerary_reversion_object = {
                column_family_mapping_quantifier_value: {new_excursion_name: new_excursion_id}}

            for column_family, column_family_dict in profile_page_itinerary_reversion_object.items():

                for activity in [bigtable_constants.payana_generic_activity_column_family] + list(payana_excursion_clone_object.activities_list.keys()):
                    activity_column_family_mapping = "_".join(
                        [activity, column_family])

                    # Delete specific column family and column values
                    for column_quantifier, column_value in column_family_dict.items():
                        payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                            profile_id, activity_column_family_mapping, column_quantifier, column_value)

                        payana_profile_page_itinerary_table_delete_wrappers.append(
                            payana_profile_page_itinerary_table_delete_wrapper)

            payana_profile_page_itinerary_obj_delete_status = delete_profile_page_itinerary_object_column_values(
                payana_profile_page_itinerary_table_delete_wrappers)

            if not payana_profile_page_itinerary_obj_delete_status:
                # Add logging
                pass

            raise Exception(
                payana_service_constants.payana_profile_page_itineraries_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_201_response,
            payana_excursion_id_header: new_excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201


@payana_excursion_objects_name_space.route("/home/")
class PayanaExcursionObjectHomeEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_service_constants.payana_missing_city_header_exception, payana_excursion_objects_name_space)

        city = str(city)

        activity = get_activity_id_header(request)

        if activity is None or len(activity) == 0:
            activity = bigtable_constants.payana_generic_activity_column_family
        elif activity not in bigtable_constants.payana_activity_column_family:
            raise KeyError(
                payana_service_constants.payana_invalid_activity_id_exception, payana_excursion_objects_name_space)

        activity = str(activity)

        # Step 1 - fetch neighboring cities
        payana_neighboring_cities_read_obj = PayanaBigTable(
            bigtable_constants.payana_neighboring_cities_table)
        payana_homepage_cities_list = payana_neighboring_cities_read_obj.get_row_dict(
            city, include_column_family=True)

        if payana_homepage_cities_list is None or len(payana_homepage_cities_list) == 0 or city not in payana_homepage_cities_list:
            raise Exception(
                payana_service_constants.payana_city_not_found_exception, payana_excursion_objects_name_space)

        payana_homepage_cities_list = payana_homepage_cities_list[city][
            bigtable_constants.payana_neighboring_cities_column_family]

        # Step 2 - get city wise ranked excursion/activity objects
        payana_homepage_return_obj = {payana_service_constants.payana_activity_guide_header: [
        ], payana_service_constants.payana_excursion_guide_header: []}

        for homepage_city in payana_homepage_cities_list:
            payana_global_city_itinerary_read_obj = PayanaBigTable(
                bigtable_constants.payana_global_city_itinerary_table)
            payana_global_city_itinerary_read_row_obj = payana_global_city_itinerary_read_obj.get_row_dict(
                homepage_city, include_column_family=True)

            if payana_global_city_itinerary_read_row_obj is None or len(payana_global_city_itinerary_read_row_obj) == 0 or homepage_city not in payana_global_city_itinerary_read_row_obj:
                raise (payana_service_constants.payana_top_excursion_guides_not_found_exception,
                       payana_excursion_objects_name_space)

            payana_global_city_itinerary_read_row_obj = payana_global_city_itinerary_read_row_obj[
                homepage_city]

            activity_guide_identifier = '_'.join([activity, bigtable_constants.payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value,
                                                 bigtable_constants.payana_global_city_itinerary_table_activity_guide_id_quantifier_value])
            excursion_identifier = '_'.join([activity, bigtable_constants.payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value,
                                            bigtable_constants.payana_global_city_itinerary_table_excursion_id_quantifier_value])

            activity_guide_id_list = {}
            if activity_guide_identifier in payana_global_city_itinerary_read_row_obj:
                activity_guide_id_list = payana_global_city_itinerary_read_row_obj[
                    activity_guide_identifier]

            excursion_id_list = {}
            if excursion_identifier in payana_global_city_itinerary_read_row_obj:
                excursion_id_list = payana_global_city_itinerary_read_row_obj[excursion_identifier]

            # Step 3 - for each excursion, activity ID, get metadata
            payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)
            gcs_payana_itinerary_pictures_bucket_name = bigtable_constants.payana_gcs_itinerary_pictures

            # sort by timestamp later
            for excursion_id in {**excursion_id_list, **activity_guide_id_list}:
                
                payana_excursion_object = payana_excursion_read_obj.get_row_dict(
                    excursion_id, include_column_family=True)

                if payana_excursion_object is None or len(payana_excursion_object) == 0 or excursion_id not in payana_excursion_object or bigtable_constants.payana_excursion_column_family_image_id_list not in payana_excursion_object[excursion_id]:
                    continue

                payana_excursion_object[excursion_id][bigtable_constants.payana_excursion_image_id_signed_url_mapping] = {
                }
                
                # Step 4 - fetch image IDs and get the signed download URLs
                if activity == bigtable_constants.payana_generic_activity_column_family and excursion_id in activity_guide_id_list:
                    # fetch activity guide thumbnail images
                    payana_activity_thumbnail_obj = PayanaBigTable(
                        bigtable_constants.payana_activity_guide_thumbnail_table)

                    payana_activity_thumbnail_obj_read = payana_activity_thumbnail_obj.get_row_dict(
                        homepage_city, include_column_family=True)

                    if homepage_city in payana_activity_thumbnail_obj_read:
                        for activity_id in bigtable_constants.payana_activity_column_family:
                            activity_thumbnail_identifier = '_'.join(
                                [activity_id, bigtable_constants.payana_activity_thumbnail])
                            if activity_thumbnail_identifier in payana_activity_thumbnail_obj_read[homepage_city]:
                                rand_int = random.randint(0, len(
                                    payana_activity_thumbnail_obj_read[homepage_city][activity_thumbnail_identifier])-1)
                                image_id = list(payana_activity_thumbnail_obj_read[homepage_city][activity_thumbnail_identifier].keys())[
                                    rand_int]
                                payana_profile_picture_download_signed_url_content = payana_generate_download_signed_url(
                                    gcs_payana_itinerary_pictures_bucket_name, image_id)
                                payana_excursion_object[excursion_id][bigtable_constants.payana_excursion_image_id_signed_url_mapping].update({activity_id: {image_id: payana_profile_picture_download_signed_url_content
                                                                                                                                                             }})
                else:
                    for _, image_id in payana_excursion_object[excursion_id][bigtable_constants.payana_excursion_column_family_image_id_list].items():
                        payana_profile_picture_download_signed_url_content = payana_generate_download_signed_url(
                            gcs_payana_itinerary_pictures_bucket_name, image_id)

                        payana_excursion_object[excursion_id][bigtable_constants.payana_excursion_image_id_signed_url_mapping].update({image_id: payana_profile_picture_download_signed_url_content
                                                                                                                                       })
                        if len(payana_excursion_object[excursion_id][bigtable_constants.payana_excursion_image_id_signed_url_mapping]) == 4:
                            break

                if excursion_id in activity_guide_id_list:
                    payana_homepage_return_obj[payana_service_constants.payana_activity_guide_header].append(
                        payana_excursion_object)
                else:
                    payana_homepage_return_obj[payana_service_constants.payana_excursion_guide_header].append(
                        payana_excursion_object)

        return payana_homepage_return_obj, payana_200
