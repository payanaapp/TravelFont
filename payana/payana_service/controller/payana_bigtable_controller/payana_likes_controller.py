from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser, get_entity_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaLikesTable import PayanaLikesTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_likes_name_space = Namespace(
    'likes', description='Manage likes for all entitities')

payana_likes_write_success_message_post = payana_service_constants.payana_likes_write_success_message_post
payana_likes_write_success_message_put = payana_service_constants.payana_likes_write_success_message_put
payana_likes_write_failure_message_post = payana_service_constants.payana_likes_write_failure_message_post
payana_likes_create_failure_message_post = payana_service_constants.payana_likes_create_failure_message_post
payana_likes_delete_failure_message = payana_service_constants.payana_likes_delete_failure_message
payana_likes_objects_delete_success_message = payana_service_constants.payana_likes_objects_delete_success_message
payana_likes_objects_delete_failure_message = payana_service_constants.payana_likes_objects_delete_failure_message
payana_likes_objects_delete_success_message = payana_service_constants.payana_likes_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_entity_id_header = payana_service_constants.payana_entity_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_entity_id_header_exception = payana_service_constants.payana_missing_entity_id_header_exception
payana_missing_likes_object = payana_service_constants.payana_missing_likes_object

payana_likes_table = bigtable_constants.payana_likes_table

@payana_likes_name_space.route("/")
class PayanaLikesEndPoint(Resource):

    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        payana_likes_read_obj = PayanaBigTable(
            payana_likes_table)

        row_key = str(entity_id)

        payana_likes_read_obj_dict = payana_likes_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_likes_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_likes_name_space)

        return payana_likes_read_obj_dict, payana_200

    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        profile_likes_read_obj = request.json
        print(profile_likes_read_obj)

        payana_likes_object = PayanaLikesTable(
            **profile_likes_read_obj)
        payana_likes_obj_write_status = payana_likes_object.update_likes_bigtable()

        if not payana_likes_obj_write_status:
            raise Exception(
                payana_likes_create_failure_message_post, payana_likes_name_space)

        return {
            status: payana_201_response,
            payana_entity_id_header: payana_likes_object.entity_id,
            message: payana_likes_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        profile_likes_read_obj = request.json

        payana_likes_object = PayanaLikesTable(
            **profile_likes_read_obj)
        payana_likes_obj_write_status = payana_likes_object.update_likes_bigtable()

        if not payana_likes_obj_write_status:
            raise Exception(
                payana_likes_write_failure_message_post, payana_likes_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_likes_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_likes_name_space.route("/delete/")
class PayanaLikesRowDeleteEndPoint(Resource):
    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        payana_likes_read_obj = PayanaBigTable(
            payana_likes_table)

        payana_likes_obj_delete_status = payana_likes_read_obj.delete_bigtable_row_with_row_key(
            entity_id)

        if not payana_likes_obj_delete_status:
            raise Exception(
                payana_likes_delete_failure_message, payana_likes_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_likes_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_likes_name_space.route("/delete/values/")
class PayanaLikesColumnValuesDeleteEndPoint(Resource):

    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        profile_likes_object = request.json

        if profile_likes_object is None:
            raise KeyError(payana_missing_likes_object)

        payana_likes_read_obj = PayanaBigTable(
            payana_likes_table)

        payana_likes_table_delete_wrappers = []

        for column_family, column_family_dict in profile_likes_object.items():

            # Delete specific column family and column values
            for column_quantifier, column_value in column_family_dict.items():
                payana_likes_table_delete_wrapper = bigtable_write_object_wrapper(
                    entity_id, column_family, column_quantifier, column_value)

                payana_likes_table_delete_wrappers.append(
                    payana_likes_table_delete_wrapper)

            payana_likes_obj_delete_status = payana_likes_read_obj.delete_bigtable_row_columns(
                payana_likes_table_delete_wrappers)

            if not payana_likes_obj_delete_status:
                raise Exception(
                    payana_likes_objects_delete_failure_message, payana_likes_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_likes_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_likes_name_space.route("/delete/cf/")
class PayanaLikesColumnFamilyDeleteEndPoint(Resource):
    @payana_likes_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception)

        payana_likes_read_obj = PayanaBigTable(
            payana_likes_table)
        
        payana_like_column_family = bigtable_constants.payana_likes_table_column_family

        payana_likes_delete_wrapper = bigtable_write_object_wrapper(
            entity_id, payana_like_column_family, "", "")

        payana_likes_obj_delete_status = payana_likes_read_obj.delete_bigtable_row_column_family_cells(
            payana_likes_delete_wrapper)

        if not payana_likes_obj_delete_status:
            raise Exception(
                payana_likes_objects_delete_failure_message, payana_likes_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_likes_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
