from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.models.payana_bigtable_models.payana_profile_table_model import profile_table_model_schema
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

profile_table_name_space = Namespace(
    'profile', description='Manage profile information')

profile_table_model = profile_table_name_space.model('Profile Table Model',
                                                     profile_table_model_schema)

success_message_post = payana_service_constants.success_message_post
success_message_put = payana_service_constants.success_message_put
payana_profile_id_header = payana_service_constants.payana_profile_id_header
payana_200_response = payana_service_constants.payana_200_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response
payana_missing_profile_id_header_exception = payana_service_constants.payana_missing_profile_id_header_exception

@profile_table_name_space.route("/")
class PayanaProfileTableEndPoint(Resource):

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

            profile_id = payana_profile_id_header_parser()

            if profile_id is None:
                raise KeyError(payana_missing_profile_id_header_exception)

            payana_bigtable = PayanaBigTable(
                bigtable_constants.payana_profile_table)

            row_key = str(profile_id).encode()
            payana_bigtable_dict = payana_bigtable.get_row_dict_without_column_family(row_key)

            return payana_bigtable_dict

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @profile_table_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

            profile_table_object = request.json

            payana_profile_object = PayanaProfileTable(**profile_table_object)
            payana_profile_object.update_profile_info_bigtable()

            return {
                "status": success_message_post,
                "name": payana_profile_object.profile_id
            }

    @profile_table_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @profile_table_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def put(self):

            profile_id = payana_profile_id_header_parser()

            if profile_id is None:
                raise KeyError(payana_missing_profile_id_header_exception)

            profile_table_object = request.json

            payana_profile_object = PayanaProfileTable(**profile_table_object)
            payana_profile_object.update_profile_info_bigtable()

            return {
                "status": success_message_put,
                "name": payana_profile_object.profile_id
            }
        