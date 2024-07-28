from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json
import copy

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_itinerary_id_header, get_profile_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.controller.payana_bigtable_controller.payana_bigtable_controller_utils.payana_bigtable_controller_itinerary_creation_utils import get_itinerary_object, update_itinerary_object, create_itinerary_metadata_object, create_profile_page_itinerary_object, delete_profile_page_itinerary_object_column_values
from payana.payana_service.models.payana_bigtable_models.payana_itinerary_flow_model import profile_page_itinerary_model

payana_itinerary_objects_name_space = Namespace(
    'itinerary', description='Manage the CRUD operations of the excursion table')

payana_itinerary_objects_write_success_message_post = payana_service_constants.payana_itinerary_objects_write_success_message_post
payana_itinerary_objects_write_success_message_put = payana_service_constants.payana_itinerary_objects_write_success_message_put
payana_itinerary_objects_write_failure_message_post = payana_service_constants.payana_itinerary_objects_write_failure_message_post
payana_itinerary_objects_create_failure_message_post = payana_service_constants.payana_itinerary_objects_create_failure_message_post
payana_itinerary_objects_delete_failure_message = payana_service_constants.payana_itinerary_objects_delete_failure_message
payana_itinerary_objects_values_delete_success_message = payana_service_constants.payana_itinerary_objects_values_delete_success_message
payana_itinerary_objects_values_delete_failure_message = payana_service_constants.payana_itinerary_objects_values_delete_failure_message
payana_itinerary_objects_delete_success_message = payana_service_constants.payana_itinerary_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_itinerary_id_header = payana_service_constants.payana_itinerary_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_itinerary_objects_header_exception = payana_service_constants.payana_missing_itinerary_objects_header_exception
payana_missing_itinerary_object = payana_service_constants.payana_missing_itinerary_object
payana_itinerary_table = bigtable_constants.payana_itinerary_table


@payana_itinerary_objects_name_space.route("/")
class PayanaItineraryObjectEndPoint(Resource):

    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        payana_itinerary_read_obj = PayanaBigTable(
            payana_itinerary_table)

        row_key = str(itinerary_id)

        payana_itinerary_obj = payana_itinerary_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_itinerary_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_itinerary_objects_name_space)

        return payana_itinerary_obj, payana_200

    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_itinerary_read_obj = request.json

        payana_itinerary_object = PayanaItineraryTable(
            **profile_itinerary_read_obj)
        payana_itinerary_obj_write_status = payana_itinerary_object.update_itinerary_bigtable()

        if not payana_itinerary_obj_write_status:
            raise Exception(
                payana_itinerary_objects_create_failure_message_post, payana_itinerary_objects_name_space)

        itinerary_id = payana_itinerary_object.itinerary_id

        return {
            status: payana_201_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        payana_itinerary_object = request.json

        payana_itinerary_read_obj = PayanaBigTable(payana_itinerary_table)

        payana_itinerary_obj_write_status = payana_itinerary_read_obj.insert_columns_column_family(
            itinerary_id, payana_itinerary_object)

        if not payana_itinerary_obj_write_status:
            raise Exception(
                payana_itinerary_objects_create_failure_message_post, payana_itinerary_objects_name_space)

        return {
            status: payana_200_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_itinerary_objects_name_space.route("/delete/")
class PayanaExcursionObjectRowDeleteEndPoint(Resource):
    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        profile_itinerary_read_obj = PayanaBigTable(
            payana_itinerary_table)

        payana_itinerary_obj_delete_status = profile_itinerary_read_obj.delete_bigtable_row_with_row_key(
            itinerary_id)

        if not payana_itinerary_obj_delete_status:
            raise Exception(
                payana_itinerary_objects_delete_failure_message, payana_itinerary_objects_name_space)

        return {
            status: payana_200_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_itinerary_objects_name_space.route("/delete/values/")
class PayanaExcursionObjectColumnValuesDeleteEndPoint(Resource):

    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        payana_itinerary_object = request.json

        if payana_itinerary_object is None:
            raise KeyError(payana_missing_itinerary_object,
                           payana_itinerary_objects_name_space)

        payana_excursion_read_obj = PayanaBigTable(
            payana_itinerary_table)

        payana_itinerary_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row_column_list(
            itinerary_id, payana_itinerary_object)

        if not payana_itinerary_obj_delete_status:
            raise Exception(
                payana_itinerary_objects_values_delete_failure_message, payana_itinerary_objects_name_space)

        return {
            status: payana_200_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_itinerary_objects_name_space.route("/delete/cf/")
class PayanaExcursionObjectColumnFamilyDeleteEndPoint(Resource):
    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        payana_itinerary_object = request.json

        if payana_itinerary_object is None:
            raise KeyError(payana_missing_itinerary_object,
                           payana_itinerary_objects_name_space)

        payana_itinerary_checkin_permission_read_obj = PayanaBigTable(
            payana_itinerary_table)

        for column_family, _ in payana_itinerary_object.items():

            payana_itinerary_delete_wrapper = bigtable_write_object_wrapper(
                itinerary_id, column_family, "", "")

            payana_itinerary_obj_delete_status = payana_itinerary_checkin_permission_read_obj.delete_bigtable_row_column_family_cells(
                payana_itinerary_delete_wrapper)

            if not payana_itinerary_obj_delete_status:
                raise Exception(
                    payana_itinerary_objects_values_delete_failure_message, payana_itinerary_objects_name_space)

        return {
            status: payana_200_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_itinerary_objects_name_space.route("/edit/metadata/")
class PayanaItineraryObjectTransactionEndPoint(Resource):

    @payana_itinerary_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        itinerary_id = get_itinerary_id_header(request)

        if itinerary_id is None or len(itinerary_id) == 0:
            raise KeyError(
                payana_missing_itinerary_objects_header_exception, payana_itinerary_objects_name_space)

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_service_constants.payana_missing_profile_id_header_exception,
                           payana_itinerary_objects_name_space)

        # Step 1 - Fetch the existing itinerary metadata object
        payana_itinerary_existing_obj = get_itinerary_object(itinerary_id)
        payana_itinerary_existing_obj = payana_itinerary_existing_obj[itinerary_id]
        existing_it_name = payana_itinerary_existing_obj[bigtable_constants.payana_itinerary_metadata][
            bigtable_constants.payana_itinerary_column_family_description]

        # Step 2 - Update the itinerary object metadata
        payana_itinerary_object = request.json
        payana_itinerary_read_obj, payana_itinerary_obj_write_status = update_itinerary_object(
            itinerary_id, payana_itinerary_object)

        if not payana_itinerary_obj_write_status:
            # Step 3 - Revert the changes to Step 2 using Step 1 original object
            payana_itinerary_object, payana_itinerary_obj_write_status = create_itinerary_metadata_object(
                payana_itinerary_existing_obj)

            raise Exception(
                payana_itinerary_objects_create_failure_message_post, payana_itinerary_objects_name_space)

        # Step 4 - Update the profile page itinerary object metadata (only if the metadata update is name/description)
        if bigtable_constants.payana_itinerary_metadata in payana_itinerary_object and bigtable_constants.payana_itinerary_column_family_description in payana_itinerary_object[bigtable_constants.payana_itinerary_metadata]:

            # 4A - update the new description/name
            profile_page_itinerary_obj = copy.deepcopy(
                profile_page_itinerary_model)

            profile_page_itinerary_obj[bigtable_constants.payana_profile_table_profile_id] = profile_id

            new_description = payana_itinerary_object[bigtable_constants.payana_itinerary_metadata][
                bigtable_constants.payana_itinerary_column_family_description]

            profile_page_itinerary_obj[bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value] = {
                new_description: itinerary_id
            }

            _, payana_profile_page_itinerary_obj_write_status = create_profile_page_itinerary_object(
                profile_page_itinerary_obj)

            # 4B - delete the existing description/name
            if payana_profile_page_itinerary_obj_write_status:
                payana_profile_page_itinerary_table_delete_wrappers = []
                generic_activity_cf = "_".join([bigtable_constants.payana_generic_activity_column_family,
                                               bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value])

                payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(profile_id, generic_activity_cf,
                                                                                                   existing_it_name, itinerary_id)

                payana_profile_page_itinerary_table_delete_wrappers.append(
                    payana_profile_page_itinerary_table_delete_wrapper)

                _ = delete_profile_page_itinerary_object_column_values(
                    payana_profile_page_itinerary_table_delete_wrappers)

        return {
            status: payana_200_response,
            payana_itinerary_id_header: itinerary_id,
            message: payana_itinerary_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200
