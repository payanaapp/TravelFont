from tabnanny import check
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_checkin_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaCheckinTable import PayanaCheckinTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_checkin_name_space = Namespace(
    'checkin', description='Manage payana check in objects')

# profile_table_model = payana_checkin_name_space.model('Profile Table Model',
#                                                      profile_table_model_schema)

payana_check_in_write_success_message_post = payana_service_constants.payana_check_in_write_success_message_post
payana_check_in_write_success_message_put = payana_service_constants.payana_check_in_write_success_message_put
payana_check_in_write_failure_message_post = payana_service_constants.payana_check_in_write_failure_message_post
payana_check_in_create_failure_message_post = payana_service_constants.payana_check_in_create_failure_message_post
payana_check_in_delete_failure_message = payana_service_constants.payana_check_in_delete_failure_message
payana_check_in_delete_success_message = payana_service_constants.payana_check_in_delete_success_message
payana_check_in_objects_delete_failure_message = payana_service_constants.payana_check_in_objects_delete_failure_message
payana_check_in_objects_delete_success_message = payana_service_constants.payana_check_in_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_check_in_id_header = payana_service_constants.payana_check_in_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_check_in_id_header_exception = payana_service_constants.payana_check_in_id_missing_exception_message
payana_check_in_id_empty_exception_message = payana_service_constants.payana_check_in_id_empty_exception_message
payana_missing_check_in_object = payana_service_constants.payana_missing_check_in_object

payana_checkin_table = bigtable_constants.payana_checkin_table


@payana_checkin_name_space.route("/")
class PayanaCheckinTableEndPoint(Resource):

    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        checkin_id = get_checkin_id_header(request)

        if checkin_id is None or len(checkin_id) == 0:
            raise KeyError(
                payana_missing_check_in_id_header_exception, payana_checkin_name_space)

        payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)

        row_key = str(checkin_id)

        payana_checkin_read_obj_dict = payana_checkin_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_checkin_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_checkin_name_space)

        return payana_checkin_read_obj_dict, payana_200

    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    # @payana_checkin_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

        payana_checkin_object = request.json

        payana_checkin_object = PayanaCheckinTable(**payana_checkin_object)
        payana_checkin_obj_write_status = payana_checkin_object.update_checkin_bigtable()

        if not payana_checkin_obj_write_status:
            raise Exception(
                payana_check_in_create_failure_message_post, payana_checkin_name_space)

        return {
            status: payana_201_response,
            payana_check_in_id_header: payana_checkin_object.checkin_id,
            message: payana_check_in_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        checkin_id = get_checkin_id_header(request)

        if checkin_id is None or len(checkin_id) == 0:
            raise KeyError(
                payana_missing_check_in_id_header_exception, payana_checkin_name_space)

        payana_checkin_object = request.json

        payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)

        payana_checkin_metadata = bigtable_constants.payana_checkin_metadata
        payana_checkin_id = bigtable_constants.payana_checkin_id

        if payana_checkin_object[payana_checkin_metadata][payana_checkin_id] is None or payana_checkin_object[payana_checkin_metadata][payana_checkin_id] == "":
            raise Exception(
                payana_check_in_id_empty_exception_message, payana_checkin_name_space)

        payana_checkin_obj_edit_status = payana_checkin_read_obj.insert_columns_column_family(
            checkin_id, payana_checkin_object)

        if not payana_checkin_obj_edit_status:
            raise Exception(
                payana_check_in_write_failure_message_post, payana_checkin_name_space)

        return {
            status: payana_200_response,
            payana_check_in_id_header: checkin_id,
            message: payana_check_in_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_checkin_name_space.route("/delete/")
class PayanaCheckinTableRowDeleteEndPoint(Resource):
    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        checkin_id = get_checkin_id_header(request)

        if checkin_id is None or len(checkin_id) == 0:
            raise KeyError(
                payana_missing_check_in_id_header_exception, payana_checkin_name_space)

        payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)

        payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_with_row_key(
            checkin_id)

        if not payana_checkin_obj_delete_status:
            raise Exception(
                payana_check_in_delete_failure_message, payana_checkin_name_space)

        return {
            status: payana_200_response,
            payana_check_in_id_header: checkin_id,
            message: payana_check_in_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_checkin_name_space.route("/delete/values/")
class PayanaCheckinTableColumnValuesDeleteEndPoint(Resource):

    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        checkin_id = get_checkin_id_header(request)

        if checkin_id is None or len(checkin_id) == 0:
            raise KeyError(
                payana_missing_check_in_id_header_exception, payana_checkin_name_space)

        payana_checkin_object = request.json

        if payana_checkin_object is None:
            raise KeyError(payana_missing_check_in_object,
                           payana_checkin_name_space)

        payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)

        payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_column_list(
            checkin_id, payana_checkin_object)

        if not payana_checkin_obj_delete_status:
            raise Exception(
                payana_check_in_objects_delete_failure_message, payana_checkin_name_space)

        return {
            status: payana_200_response,
            payana_check_in_id_header: checkin_id,
            message: payana_check_in_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_checkin_name_space.route("/delete/cf/")
class PayanaCheckinTableColumnFamilyDeleteEndPoint(Resource):
    @payana_checkin_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        checkin_id = get_checkin_id_header(request)

        if checkin_id is None or len(checkin_id) == 0:
            raise KeyError(
                payana_missing_check_in_id_header_exception, payana_checkin_name_space)

        payana_checkin_object = request.json

        if payana_checkin_object is None:
            raise KeyError(payana_missing_check_in_object,
                           payana_checkin_name_space)

        payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)

        for column_family, _ in payana_checkin_object.items():

            payana_checkin_table_delete_wrapper = bigtable_write_object_wrapper(
                checkin_id, column_family, "", "")

            payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row_column_family_cells(
                payana_checkin_table_delete_wrapper)

            if not payana_checkin_obj_delete_status:
                raise Exception(
                    payana_check_in_objects_delete_failure_message, payana_checkin_name_space)

        return {
            status: payana_200_response,
            payana_check_in_id_header: checkin_id,
            message: payana_check_in_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
