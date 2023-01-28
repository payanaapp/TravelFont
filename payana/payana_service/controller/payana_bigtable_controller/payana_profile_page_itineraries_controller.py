from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser, get_profile_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.models.payana_bigtable_models.payana_profile_table_model import profile_table_model_schema
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

profile_page_itineraries_name_space = Namespace(
    'itineraries', description='Manage profile page itineraries')

payana_profile_page_itineraries_write_success_message_post = payana_service_constants.payana_profile_page_itineraries_write_success_message_post
payana_profile_page_itineraries_write_success_message_put = payana_service_constants.payana_profile_page_itineraries_write_success_message_put
payana_profile_page_itineraries_write_failure_message_post = payana_service_constants.payana_profile_page_itineraries_write_failure_message_post
payana_profile_page_itineraries_create_failure_message_post = payana_service_constants.payana_profile_page_itineraries_create_failure_message_post
payana_profile_page_itineraries_delete_failure_message_post = payana_service_constants.payana_profile_page_itineraries_delete_failure_message_post
payana_profile_page_itineraries_delete_success_message_put = payana_service_constants.payana_profile_page_itineraries_delete_success_message_put
payana_profile_page_itinerary_objects_delete_failure_message = payana_service_constants.payana_profile_page_itinerary_objects_delete_failure_message
payana_profile_page_itinerary_objects_delete_success_message = payana_service_constants.payana_profile_page_itinerary_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_profile_id_header = payana_service_constants.payana_profile_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_profile_id_header_exception = payana_service_constants.payana_missing_profile_id_header_exception
payana_missing_profile_page_itinerary_object = payana_service_constants.payana_missing_profile_page_itinerary_object

payana_profile_page_itinerary_table = bigtable_constants.payana_profile_page_itinerary_table


@profile_page_itineraries_name_space.route("/")
class PayanaProfilePageItinerariesEndPoint(Resource):

    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_page_itinerary_read_obj = PayanaBigTable(
            payana_profile_page_itinerary_table)

        row_key = str(profile_id)

        payana_profile_page_itinerary_read_obj_dict = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_profile_page_itinerary_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                            profile_page_itineraries_name_space)

        return payana_profile_page_itinerary_read_obj_dict, payana_200

    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    # @profile_page_itineraries_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_itinerary_read_obj = request.json

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_read_obj)
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

        if not payana_profile_page_itinerary_obj_write_status:
            raise Exception(
                payana_profile_page_itineraries_create_failure_message_post, profile_page_itineraries_name_space)

        return {
            status: payana_201_response,
            payana_profile_id_header: payana_profile_page_itinerary_object.profile_id,
            message: payana_profile_page_itineraries_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_itinerary_read_obj = request.json

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_read_obj)
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()

        if not payana_profile_page_itinerary_obj_write_status:
            raise Exception(
                payana_profile_page_itineraries_write_failure_message_post, profile_page_itineraries_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_itineraries_write_success_message_put,
            status_code: payana_200
        }, payana_200


@profile_page_itineraries_name_space.route("/delete/")
class PayanaProfilePageItinerariesRowDeleteEndPoint(Resource):
    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_page_itinerary_read_obj = PayanaBigTable(
            payana_profile_page_itinerary_table)

        payana_profile_page_itinerary_obj_delete_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_with_row_key(
            profile_id)

        if not payana_profile_page_itinerary_obj_delete_status:
            raise Exception(
                payana_profile_page_itineraries_delete_failure_message_post, profile_page_itineraries_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_itineraries_delete_success_message_put,
            status_code: payana_200
        }, payana_200


@profile_page_itineraries_name_space.route("/delete/values/")
class PayanaProfilePageItinerariesColumnValuesDeleteEndPoint(Resource):

    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_itinerary_object = request.json

        if profile_page_itinerary_object is None:
            raise KeyError(payana_missing_profile_page_itinerary_object)

        payana_profile_page_itinerary_read_obj = PayanaBigTable(
            payana_profile_page_itinerary_table)

        payana_profile_page_itinerary_table_delete_wrappers = []

        for column_family, column_family_dict in profile_page_itinerary_object.items():

            # Delete specific column family and column values
            for column_quantifier, column_value in column_family_dict.items():
                payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                    profile_id, column_family, column_quantifier, column_value)

                payana_profile_page_itinerary_table_delete_wrappers.append(
                    payana_profile_page_itinerary_table_delete_wrapper)

            payana_profile_page_itinerary_obj_delete_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_columns(
                payana_profile_page_itinerary_table_delete_wrappers)

            if not payana_profile_page_itinerary_obj_delete_status:
                raise Exception(
                    payana_profile_page_itinerary_objects_delete_failure_message, profile_page_itineraries_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@profile_page_itineraries_name_space.route("/delete/cf/")
class PayanaProfileTableColumnFamilyDeleteEndPoint(Resource):
    @profile_page_itineraries_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_itinerary_object = request.json

        if profile_page_itinerary_object is None:
            raise KeyError(payana_missing_profile_page_itinerary_object)

        payana_profile_page_itinerary_read_obj = PayanaBigTable(
            payana_profile_page_itinerary_table)

        for column_family, _ in profile_page_itinerary_object.items():

            payana_profile_page_itinerary_delete_wrapper = bigtable_write_object_wrapper(
                profile_id, column_family, "", "")

            payana_profile_page_itinerary_obj_delete_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column_family_cells(
                payana_profile_page_itinerary_delete_wrapper)

            if not payana_profile_page_itinerary_obj_delete_status:
                raise Exception(
                    payana_profile_page_itinerary_objects_delete_failure_message, profile_page_itineraries_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
