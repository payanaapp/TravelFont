from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_profile_id_header, get_entity_id_header, get_comment_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_entity_comments_object_builder, payana_comment_obj_delete_builder
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaCommentsTable import PayanaCommentsTable
from payana.payana_bl.bigtable_utils.PayanaEntityToCommentsTable import PayanaEntityToCommentsTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_comments_name_space = Namespace(
    'comments', description='Manage comments for all entitities')

payana_comments_write_success_message_post = payana_service_constants.payana_comments_write_success_message_post
payana_comments_write_success_message_put = payana_service_constants.payana_comments_write_success_message_put
payana_comments_write_failure_message_post = payana_service_constants.payana_comments_write_failure_message_post
payana_comments_create_failure_message_post = payana_service_constants.payana_comments_create_failure_message_post
payana_comments_delete_failure_message = payana_service_constants.payana_comments_delete_failure_message
payana_comments_delete_success_message = payana_service_constants.payana_comments_delete_success_message
payana_comments_objects_delete_failure_message = payana_service_constants.payana_comments_objects_delete_failure_message
payana_comments_objects_delete_success_message = payana_service_constants.payana_comments_objects_delete_success_message

payana_entity_comments_write_success_message_post = payana_service_constants.payana_entity_comments_write_success_message_post
payana_entity_comments_write_success_message_put = payana_service_constants.payana_entity_comments_write_success_message_put
payana_entity_comments_write_failure_message_post = payana_service_constants.payana_entity_comments_write_failure_message_post
payana_entity_comments_create_failure_message_post = payana_service_constants.payana_entity_comments_create_failure_message_post
payana_entity_comments_delete_failure_message = payana_service_constants.payana_entity_comments_delete_failure_message
payana_entity_comments_delete_success_message = payana_service_constants.payana_entity_comments_delete_success_message
payana_entity_comments_objects_delete_failure_message = payana_service_constants.payana_entity_comments_objects_delete_failure_message
payana_entity_comments_objects_delete_success_message = payana_service_constants.payana_entity_comments_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_entity_id_header = payana_service_constants.payana_entity_id_header
payana_comment_id_header = payana_service_constants.payana_comment_id_header
payana_comment_id_list_header = payana_service_constants.payana_comment_id_list_header
payana_comment_id_missing_exception_message = payana_service_constants.payana_comment_id_missing_exception_message

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_entity_id_header_exception = payana_service_constants.payana_missing_entity_id_header_exception
payana_missing_comments_object = payana_service_constants.payana_missing_comments_object
payana_missing_entity_comments_object = payana_service_constants.payana_missing_entity_comments_object
payana_missing_entity_comment_id_list_object = payana_service_constants.payana_missing_entity_comment_id_list_object
payana_missing_comment_id_header_exception = payana_service_constants.payana_missing_comment_id_header_exception

payana_comments_table = bigtable_constants.payana_comments_table
payana_entity_to_comments_table = bigtable_constants.payana_entity_to_comments_table


@payana_comments_name_space.route("/details/")
class PayanaCommentDetailsEndPoint(Resource):

    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        comment_id = get_comment_id_header(request)

        if comment_id is None or len(comment_id) == 0:
            raise KeyError(
                payana_missing_comment_id_header_exception, payana_comments_name_space)

        payana_comments_read_obj = PayanaBigTable(
            payana_comments_table)

        row_key = str(comment_id)

        payana_comments_read_obj_dict = payana_comments_read_obj.get_row_dict(
            row_key, include_column_family=False)

        if len(payana_comments_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_comments_name_space)

        return payana_comments_read_obj_dict, payana_200


@payana_comments_name_space.route("/")
class PayanaCommentsEndPoint(Resource):

    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception,
                           payana_comments_name_space)

        payana_entity_comments_read_obj = PayanaBigTable(
            payana_entity_to_comments_table)

        row_key = str(entity_id)

        payana_entity_comments_read_obj_dict = payana_entity_comments_read_obj.get_row_dict(
            row_key, include_column_family=False)

        if len(payana_entity_comments_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_comments_name_space)

        return payana_entity_comments_read_obj_dict, payana_200

    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception,
                           payana_comments_name_space)

        profile_comments_read_obj = request.json

        payana_comments_object = PayanaCommentsTable(
            **profile_comments_read_obj)
        payana_comments_obj_write_status = payana_comments_object.update_comment_bigtable()

        if not payana_comments_obj_write_status:
            raise Exception(
                payana_comments_create_failure_message_post, payana_comments_name_space)

        comment_id = payana_comments_object.comment_id
        comment_timestamp = payana_comments_object.comment_timestamp

        if comment_id is None or comment_id == "":
            raise Exception(
                payana_comments_create_failure_message_post, payana_comments_name_space)

        payana_entity_comments_object = payana_entity_comments_object_builder(
            entity_id, comment_id, comment_timestamp)

        payana_entity_to_comment_id_list_obj = PayanaEntityToCommentsTable(
            **payana_entity_comments_object)

        payana_entity_to_comment_id_list_obj_write_status = payana_entity_to_comment_id_list_obj.update_entity_to_comments_bigtable()

        if not payana_entity_to_comment_id_list_obj_write_status:
            raise Exception(
                payana_entity_comments_create_failure_message_post, payana_comments_name_space)

        return {
            status: payana_201_response,
            payana_entity_id_header: payana_comments_object.entity_id,
            message: payana_comments_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception,
                           payana_comments_name_space)

        profile_comments_read_obj = request.json

        payana_comments_object = PayanaCommentsTable(
            **profile_comments_read_obj)

        comment_id = payana_comments_object.comment_id

        if comment_id is None or comment_id == "":
            raise Exception(
                payana_comment_id_missing_exception_message, payana_comments_name_space)

        payana_comments_obj_write_status = payana_comments_object.update_comment_bigtable()

        if not payana_comments_obj_write_status:
            raise Exception(
                payana_comments_write_failure_message_post, payana_comments_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_entity_comments_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_comments_name_space.route("/entity/delete/")
class PayanaEntityCommentsRowDeleteEndPoint(Resource):
    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception,
                           payana_comments_name_space)

        payana_entity_comments_read_obj = PayanaBigTable(
            payana_entity_to_comments_table)

        row_key = str(entity_id)

        payana_entity_comments_read_obj_dict = payana_entity_comments_read_obj.get_row_dict(
            row_key, include_column_family=False)

        if len(payana_entity_comments_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_comments_name_space)

        payana_comments_table_delete_wrappers = payana_comment_obj_delete_builder(
            payana_entity_comments_read_obj_dict)

        payana_entity_comment_obj_delete_status = payana_entity_comments_read_obj.delete_bigtable_row_with_row_key(
            entity_id)

        if not payana_entity_comment_obj_delete_status:
            raise Exception(
                payana_entity_comments_delete_failure_message, payana_comments_name_space)

        payana_comment_obj = PayanaBigTable(
            payana_comments_table)

        payana_comment_obj_delete_status = payana_comment_obj.delete_bigtable_rows(
            payana_comments_table_delete_wrappers)

        if not payana_comment_obj_delete_status:
            raise Exception(
                payana_comments_delete_failure_message, payana_comments_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_entity_comments_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_comments_name_space.route("/delete/")
class PayanaEntityCommentsRowDeleteEndPoint(Resource):
    @payana_comments_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(payana_missing_entity_id_header_exception,
                           payana_comments_name_space)

        payana_entity_comments_id_list_object = request.json

        if payana_entity_comments_id_list_object is None:
            raise KeyError(
                payana_missing_entity_comment_id_list_object, payana_comments_name_space)

        payana_entity_comment_obj = PayanaBigTable(
            payana_entity_to_comments_table)

        payana_entity_comment_obj_delete_status = payana_entity_comment_obj.delete_bigtable_row_column_list(
            entity_id, payana_entity_comments_id_list_object)

        if not payana_entity_comment_obj_delete_status:
            raise Exception(
                payana_entity_comments_objects_delete_failure_message, payana_comments_name_space)
            
        payana_comments_table_delete_wrappers = []

        for _, comment_id_list in payana_entity_comments_id_list_object.items():

            # Delete specific column family and column values
            for comment_id in comment_id_list:
                payana_comments_table_delete_wrapper = bigtable_write_object_wrapper(
                    comment_id, "", "", "")

                payana_comments_table_delete_wrappers.append(
                    payana_comments_table_delete_wrapper)

        payana_comment_obj = PayanaBigTable(
            payana_comments_table)

        payana_comment_obj_delete_status = payana_comment_obj.delete_bigtable_rows(
            payana_comments_table_delete_wrappers)

        if not payana_comment_obj_delete_status:
            raise Exception(
                payana_comments_delete_failure_message, payana_comments_name_space)

        return {
            status: payana_200_response,
            bigtable_constants.payana_entity_to_comments_table_comment_id_list: payana_entity_comments_id_list_object[bigtable_constants.payana_entity_to_comments_table_comment_id_list],
            message: payana_comments_delete_success_message,
            status_code: payana_200
        }, payana_200
