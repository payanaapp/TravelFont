from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_entity_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaExcursionCheckinPermissionTable import PayanaExcursionCheckinPermissionTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_excursion_checkin_objects_permission_name_space = Namespace(
    'edit/permission', description='Manage the edit permissions of the excursion guide participants')

payana_excursion_checkin_objects_permission_write_success_message_post = payana_service_constants.payana_excursion_checkin_objects_permission_write_success_message_post
payana_excursion_checkin_objects_permission_write_success_message_put = payana_service_constants.payana_excursion_checkin_objects_permission_write_success_message_put
payana_excursion_checkin_objects_permission_write_failure_message_post = payana_service_constants.payana_excursion_checkin_objects_permission_write_failure_message_post
payana_excursion_checkin_objects_permission_create_failure_message_post = payana_service_constants.payana_excursion_checkin_objects_permission_create_failure_message_post
payana_excursion_checkin_objects_permission_delete_failure_message = payana_service_constants.payana_excursion_checkin_objects_permission_delete_failure_message
payana_excursion_checkin_objects_permission_delete_success_message = payana_service_constants.payana_excursion_checkin_objects_permission_delete_success_message
payana_excursion_checkin_objects_permission_objects_delete_failure_message = payana_service_constants.payana_excursion_checkin_objects_permission_objects_delete_failure_message
payana_excursion_checkin_objects_permission_objects_delete_success_message = payana_service_constants.payana_excursion_checkin_objects_permission_objects_delete_success_message

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

payana_missing_excursion_checkin_objects_permission_header_exception = payana_service_constants.payana_missing_excursion_checkin_objects_permission_header_exception
payana_missing_excursion_checkin_objects_permission_object = payana_service_constants.payana_missing_excursion_checkin_objects_permission_object
payana_excursion_checkin_permission_table = bigtable_constants.payana_excursion_checkin_permission_table


@payana_excursion_checkin_objects_permission_name_space.route("/")
class PayanaExcursionObjectPermissionEndPoint(Resource):

    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)

        payana_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_checkin_permission_table)

        row_key = str(entity_id)

        payana_excursion_checkin_permission_obj = payana_excursion_checkin_permission_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_excursion_checkin_permission_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_checkin_objects_permission_name_space)

        return payana_excursion_checkin_permission_obj, payana_200

    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)

        profile_excursion_checkin_permission_read_obj = request.json

        payana_excursion_checkin_permission_object = PayanaExcursionCheckinPermissionTable(
            **profile_excursion_checkin_permission_read_obj)
        payana_excursion_checkin_permission_obj_write_status = payana_excursion_checkin_permission_object.update_excursion_bigtable()

        if not payana_excursion_checkin_permission_obj_write_status:
            raise Exception(
                payana_excursion_checkin_objects_permission_create_failure_message_post, payana_excursion_checkin_objects_permission_name_space)

        return {
            status: payana_201_response,
            payana_entity_id_header: entity_id,
            message: payana_excursion_checkin_objects_permission_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)

        profile_excursion_checkin_permission_read_obj = request.json

        payana_excursion_checkin_permission_object = PayanaExcursionCheckinPermissionTable(
            **profile_excursion_checkin_permission_read_obj)
        payana_excursion_checkin_permission_obj_write_status = payana_excursion_checkin_permission_object.update_excursion_bigtable()

        if not payana_excursion_checkin_permission_obj_write_status:
            raise Exception(
                payana_excursion_checkin_objects_permission_create_failure_message_post, payana_excursion_checkin_objects_permission_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_excursion_checkin_objects_permission_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_excursion_checkin_objects_permission_name_space.route("/delete/")
class PayanaExcursionObjectPermissionRowDeleteEndPoint(Resource):
    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)

        profile_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_checkin_permission_table)

        payana_excursion_checkin_permission_obj_delete_status = profile_excursion_checkin_permission_read_obj.delete_bigtable_row_with_row_key(
            entity_id)

        if not payana_excursion_checkin_permission_obj_delete_status:
            raise Exception(
                payana_excursion_checkin_objects_permission_delete_failure_message, payana_excursion_checkin_objects_permission_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_excursion_checkin_objects_permission_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_checkin_objects_permission_name_space.route("/delete/values/")
class PayanaExcursionObjectPermissionColumnValuesDeleteEndPoint(Resource):

    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)

        payana_excursion_checkin_permission_object = request.json

        if payana_excursion_checkin_permission_object is None:
            raise KeyError(payana_missing_excursion_checkin_objects_permission_object,
                           payana_excursion_checkin_objects_permission_name_space)

        payana_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_checkin_permission_table)
        
        payana_excursion_checkin_permission_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column_list(
            entity_id, payana_excursion_checkin_permission_object)

        if not payana_excursion_checkin_permission_obj_delete_status:
            raise Exception(
                payana_excursion_checkin_objects_permission_objects_delete_failure_message, payana_excursion_checkin_objects_permission_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_excursion_checkin_objects_permission_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_checkin_objects_permission_name_space.route("/delete/cf/")
class PayanaExcursionObjectPermissionColumnFamilyDeleteEndPoint(Resource):
    @payana_excursion_checkin_objects_permission_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        entity_id = get_entity_id_header(request)

        if entity_id is None or len(entity_id) == 0:
            raise KeyError(
                payana_missing_excursion_checkin_objects_permission_header_exception, payana_excursion_checkin_objects_permission_name_space)
            
        payana_excursion_checkin_permission_object = request.json

        if payana_excursion_checkin_permission_object is None:
            raise KeyError(payana_missing_excursion_checkin_objects_permission_object,
                           payana_excursion_checkin_objects_permission_name_space)

        payana_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_checkin_permission_table)
        
        for column_family, _ in payana_excursion_checkin_permission_object.items():

            payana_excursion_checkin_permission_delete_wrapper = bigtable_write_object_wrapper(
                entity_id, column_family, "", "")

            payana_excursion_checkin_permission_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column_family_cells(
                payana_excursion_checkin_permission_delete_wrapper)

            if not payana_excursion_checkin_permission_obj_delete_status:
                raise Exception(
                    payana_excursion_checkin_objects_permission_objects_delete_failure_message, payana_excursion_checkin_objects_permission_name_space)

        return {
            status: payana_200_response,
            payana_entity_id_header: entity_id,
            message: payana_excursion_checkin_objects_permission_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
