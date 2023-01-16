from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser, get_profile_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.models.payana_bigtable_models.payana_profile_table_model import profile_table_model_schema
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

profile_table_name_space = Namespace(
    'info', description='Manage profile information')

# profile_table_model = profile_table_name_space.model('Profile Table Model',
#                                                      profile_table_model_schema)

payana_profile_table_write_success_message_post = payana_service_constants.payana_profile_table_write_success_message_post
payana_profile_table_write_success_message_put = payana_service_constants.payana_profile_table_write_success_message_put
payana_profile_table_write_failure_message_post = payana_service_constants.payana_profile_table_write_failure_message_post
payana_profile_table_create_failure_message_post = payana_service_constants.payana_profile_table_create_failure_message_post
status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

success_message_put = payana_service_constants.success_message_put
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

payana_profile_table = bigtable_constants.payana_profile_table


@profile_table_name_space.route("/")
class PayanaProfileTableEndPoint(Resource):

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        payana_profile_read_obj = PayanaBigTable(payana_profile_table)

        row_key = str(profile_id)

        payana_profile_read_obj_dict = payana_profile_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_profile_read_obj_dict) == 0:
            raise Exception(payana_empty_row_read_exception,
                            profile_table_name_space)

        return payana_profile_read_obj_dict, payana_200

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    # @profile_table_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

        profile_table_object = request.json

        payana_profile_object = PayanaProfileTable(**profile_table_object)
        payana_profile_obj_write_status = payana_profile_object.update_profile_info_bigtable()

        if not payana_profile_obj_write_status:
            raise Exception(
                payana_profile_table_create_failure_message_post, profile_table_name_space)

        return {
            status: payana_201_response,
            payana_profile_id_header: payana_profile_object.profile_id,
            message: payana_profile_table_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(payana_missing_profile_id_header_exception)

        profile_table_object = request.json
        # profile_table_object = json.loads(profile_table_object_json)

        payana_profile_read_obj = PayanaBigTable(payana_profile_table)

        payana_profile_obj_edit_status = payana_profile_read_obj.insert_columns_column_family(
            profile_id, profile_table_object)

        if not payana_profile_obj_edit_status:
            raise Exception(
                payana_profile_table_write_failure_message_post, profile_table_name_space)

        return {
            status: payana_200_response,
            payana_profile_id_header: profile_id,
            message: payana_profile_table_write_success_message_put,
            status_code: payana_200
        }, payana_200
