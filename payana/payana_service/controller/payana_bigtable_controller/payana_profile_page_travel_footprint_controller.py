from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser, get_profile_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaProfileTravelFootPrintTable import PayanaProfileTravelFootPrintTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

profile_page_travelfont_name_space = Namespace(
    'travelfont', description='Manage profile page travel footprint table')

payana_profile_page_travelfont_write_success_message_post = payana_service_constants.payana_profile_page_travelfont_write_success_message_post
payana_profile_page_travelfont_write_success_message_put = payana_service_constants.payana_profile_page_travelfont_write_success_message_put
payana_profile_page_travelfont_write_failure_message_post = payana_service_constants.payana_profile_page_travelfont_write_failure_message_post
payana_profile_page_travelfont_create_failure_message_post = payana_service_constants.payana_profile_page_travelfont_create_failure_message_post
payana_profile_page_travelfont_delete_failure_message = payana_service_constants.payana_profile_page_travelfont_delete_failure_message
payana_profile_page_travelfont_delete_success_message = payana_service_constants.payana_profile_page_travelfont_delete_success_message
payana_profile_page_travelfont_objects_delete_failure_message = payana_service_constants.payana_profile_page_travelfont_objects_delete_failure_message
payana_profile_page_travelfont_objects_delete_success_message = payana_service_constants.payana_profile_page_travelfont_objects_delete_success_message

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
payana_missing_profile_page_travelfont_object = payana_service_constants.payana_missing_profile_page_travelfont_object

payana_profile_travel_footprint_table = bigtable_constants.payana_profile_travel_footprint_table


@profile_page_travelfont_name_space.route("/")
class PayanaProfilePageTravelFontEndPoint(Resource):

    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_page_travel_footprint_read_obj = PayanaBigTable(
            payana_profile_travel_footprint_table)

        row_key = str(profile_id)

        payana_profile_page_travel_footprint_read_obj_dict = payana_profile_page_travel_footprint_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_profile_page_travel_footprint_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           profile_page_travelfont_name_space)

        return payana_profile_page_travel_footprint_read_parser(payana_profile_page_travel_footprint_read_obj_dict), payana_200

    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    # @profile_page_travelfont_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_travel_footprint_read_obj = request.json

        payana_profile_page_travel_footprint_object = PayanaProfileTravelFootPrintTable(
            **profile_page_travel_footprint_read_obj)
        payana_profile_page_travel_footprint_obj_write_status = payana_profile_page_travel_footprint_object.update_profile_travel_footprint_bigtable()

        if not payana_profile_page_travel_footprint_obj_write_status:
            raise Exception(
                payana_profile_page_travelfont_create_failure_message_post, profile_page_travelfont_name_space)

        return {
            status: payana_201_response,
            payana_profile_id_header: payana_profile_page_travel_footprint_object.profile_id,
            message: payana_profile_page_travelfont_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_travel_footprint_read_obj = request.json

        payana_profile_page_travel_footprint_object = PayanaProfileTravelFootPrintTable(
            **profile_page_travel_footprint_read_obj)
        payana_profile_page_travel_footprint_obj_write_status = payana_profile_page_travel_footprint_object.update_profile_travel_footprint_bigtable()

        if not payana_profile_page_travel_footprint_obj_write_status:
            raise Exception(
                payana_profile_page_travelfont_write_failure_message_post, profile_page_travelfont_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_travelfont_write_success_message_put,
            status_code: payana_200
        }, payana_200


@profile_page_travelfont_name_space.route("/delete/")
class PayanaProfilePageTravelFontRowDeleteEndPoint(Resource):
    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_page_travel_footprint_read_obj = PayanaBigTable(
            payana_profile_travel_footprint_table)

        payana_profile_page_travel_footprint_obj_delete_status = payana_profile_page_travel_footprint_read_obj.delete_bigtable_row_with_row_key(
            profile_id)

        if not payana_profile_page_travel_footprint_obj_delete_status:
            raise Exception(
                payana_profile_page_travelfont_delete_failure_message, profile_page_travelfont_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_travelfont_delete_success_message,
            status_code: payana_200
        }, payana_200


@profile_page_travelfont_name_space.route("/delete/values/")
class PayanaProfilePageTravelFontColumnValuesDeleteEndPoint(Resource):

    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_page_travel_footprint_object = request.json
        
        profile_page_travel_footprint_object = payana_profile_page_travel_footprint_delete_parser(profile_page_travel_footprint_object)

        if profile_page_travel_footprint_object is None:
            raise KeyError(payana_missing_profile_page_travelfont_object)

        payana_profile_page_travel_footprint_read_obj = PayanaBigTable(
            payana_profile_travel_footprint_table)

        payana_profile_page_travel_footprint_table_delete_wrappers = []

        for column_family, column_family_dict in profile_page_travel_footprint_object.items():

            # Delete specific column family and column values
            for column_quantifier, column_value in column_family_dict.items():
                payana_profile_page_travel_footprint_table_delete_wrapper = bigtable_write_object_wrapper(
                    profile_id, column_family, column_quantifier, column_value)

                payana_profile_page_travel_footprint_table_delete_wrappers.append(
                    payana_profile_page_travel_footprint_table_delete_wrapper)

            payana_profile_page_travel_footprint_obj_delete_status = payana_profile_page_travel_footprint_read_obj.delete_bigtable_row_columns(
                payana_profile_page_travel_footprint_table_delete_wrappers)

            if not payana_profile_page_travel_footprint_obj_delete_status:
                raise Exception(
                    payana_profile_page_travelfont_objects_delete_failure_message, profile_page_travelfont_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_travelfont_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@profile_page_travelfont_name_space.route("/delete/cf/")
class PayanaProfilePageTravelFontColumnFamilyDeleteEndPoint(Resource):
    @profile_page_travelfont_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_page_travel_footprint_read_obj = PayanaBigTable(
            payana_profile_travel_footprint_table)
        
        payana_profile_page_travel_footprint_column_family = bigtable_constants.payana_profile_page_travel_footprint_column_family

        payana_profile_page_travel_footprint_delete_wrapper = bigtable_write_object_wrapper(
            profile_id, payana_profile_page_travel_footprint_column_family, "", "")

        payana_profile_page_travel_footprint_obj_delete_status = payana_profile_page_travel_footprint_read_obj.delete_bigtable_row_column_family_cells(
            payana_profile_page_travel_footprint_delete_wrapper)

        if not payana_profile_page_travel_footprint_obj_delete_status:
            raise Exception(
                payana_profile_page_travelfont_objects_delete_failure_message, profile_page_travelfont_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_page_travelfont_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
