from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import payana_profile_id_header_parser, get_city_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaActivityGuideThumbNailTable import PayanaActivityGuideThumbNailTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_activity_guide_thumbnail_name_space = Namespace(
    'activity/thumbnail', description='Manage profile information')

payana_activity_guide_thumbnail_table_write_success_message_post = payana_service_constants.payana_activity_guide_thumbnail_table_write_success_message_post
payana_activity_guide_thumbnail_table_write_success_message_put = payana_service_constants.payana_activity_guide_thumbnail_table_write_success_message_put
payana_activity_guide_thumbnail_table_write_failure_message_post = payana_service_constants.payana_activity_guide_thumbnail_table_write_failure_message_post
payana_activity_guide_thumbnail_table_create_failure_message_post = payana_service_constants.payana_activity_guide_thumbnail_table_create_failure_message_post
payana_activity_guide_thumbnail_table_delete_failure_message = payana_service_constants.payana_activity_guide_thumbnail_table_delete_failure_message
payana_activity_guide_thumbnail_table_delete_success_message = payana_service_constants.payana_activity_guide_thumbnail_table_delete_success_message
payana_activity_guide_thumbnail_table_objects_delete_failure_message = payana_service_constants.payana_activity_guide_thumbnail_table_objects_delete_failure_message
payana_activity_guide_thumbnail_table_objects_delete_success_message = payana_service_constants.payana_activity_guide_thumbnail_table_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_city_header = payana_service_constants.payana_city_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_activity_guide_header_exception = payana_service_constants.payana_missing_activity_guide_header_exception
payana_activity_guide_thumbnail_profile_object = payana_service_constants.payana_activity_guide_thumbnail_profile_object

payana_activity_guide_thumbnail_table = bigtable_constants.payana_activity_guide_thumbnail_table


@payana_activity_guide_thumbnail_name_space.route("/")
class PayanaActivityGuideThumbnailEndPoint(Resource):

    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_activity_guide_header_exception, payana_activity_guide_thumbnail_name_space)

        payana_activity_thumbnail_read_obj = PayanaBigTable(payana_activity_guide_thumbnail_table)

        row_key = str(city)

        payana_activity_thumbnail_read_obj_dict = payana_activity_thumbnail_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_activity_thumbnail_read_obj_dict) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_activity_guide_thumbnail_name_space)

        return payana_activity_thumbnail_read_obj_dict, payana_200

    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    # @payana_activity_guide_thumbnail_name_space.expect(profile_table_model)
    @payana_service_generic_exception_handler
    def post(self):

        activity_thumbnail_object = request.json

        payana_activity_thumbnail_object = PayanaActivityGuideThumbNailTable(**activity_thumbnail_object)
        payana_activity_thumbnail_obj_write_status = payana_activity_thumbnail_object.update_activity_guide_thumbnail_bigtable()

        if not payana_activity_thumbnail_obj_write_status:
            raise Exception(
                payana_activity_guide_thumbnail_table_create_failure_message_post, payana_activity_guide_thumbnail_name_space)

        return {
            status: payana_201_response,
            message: payana_activity_guide_thumbnail_table_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        activity_thumbnail_object = request.json

        payana_activity_thumbnail_object = PayanaActivityGuideThumbNailTable(**activity_thumbnail_object)
        payana_activity_thumbnail_obj_write_status = payana_activity_thumbnail_object.update_activity_guide_thumbnail_bigtable()

        if not payana_activity_thumbnail_obj_write_status:
            raise Exception(
                payana_activity_guide_thumbnail_table_create_failure_message_post, payana_activity_guide_thumbnail_name_space)

        return {
            status: payana_200_response,
            message: payana_activity_guide_thumbnail_table_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_activity_guide_thumbnail_name_space.route("/delete/")
class PayanaActivityGuideThumbNailTableRowDeleteEndPoint(Resource):
    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_activity_guide_header_exception, payana_activity_guide_thumbnail_name_space)

        payana_activity_guide_thumbnail_read_obj = PayanaBigTable(payana_activity_guide_thumbnail_table)

        payana_activity_guide_thumbnail_obj_delete_status = payana_activity_guide_thumbnail_read_obj.delete_bigtable_row_with_row_key(
            city)

        if not payana_activity_guide_thumbnail_obj_delete_status:
            raise Exception(
                payana_activity_guide_thumbnail_table_delete_failure_message, payana_activity_guide_thumbnail_name_space)

        return {
            status: payana_200_response,
            payana_city_header: city,
            message: payana_activity_guide_thumbnail_table_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_activity_guide_thumbnail_name_space.route("/delete/values/")
class PayanaActivityGuideThumbNailTableColumnValuesDeleteEndPoint(Resource):

    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_activity_guide_header_exception, payana_activity_guide_thumbnail_name_space)

        activity_id_table_object = request.json

        if activity_id_table_object is None:
            raise KeyError(payana_activity_guide_thumbnail_profile_object,
                           payana_activity_guide_thumbnail_name_space)

        payana_activity_id_read_obj = PayanaBigTable(payana_activity_guide_thumbnail_table)

        payana_activity_guide_thumbnail_table_delete_wrappers = []

        for column_family, column_family_dict in activity_id_table_object.items():

            # Delete specific column family and column values
            for column_quantifier, column_value in column_family_dict.items():
                payana_activity_guide_thumbnail_table_delete_wrapper = bigtable_write_object_wrapper(
                    city, column_family, column_quantifier, column_value)

                payana_activity_guide_thumbnail_table_delete_wrappers.append(
                    payana_activity_guide_thumbnail_table_delete_wrapper)

            payana_activity_id_obj_delete_status = payana_activity_id_read_obj.delete_bigtable_row_columns(
                payana_activity_guide_thumbnail_table_delete_wrappers)

            if not payana_activity_id_obj_delete_status:
                raise Exception(
                    payana_activity_guide_thumbnail_table_objects_delete_failure_message, payana_activity_guide_thumbnail_name_space)

        return {
            status: payana_200_response,
            payana_city_header: city,
            message: payana_activity_guide_thumbnail_table_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_activity_guide_thumbnail_name_space.route("/delete/cf/")
class PayanaActivityGuideThumbNailTableColumnFamilyDeleteEndPoint(Resource):
    @payana_activity_guide_thumbnail_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_activity_guide_header_exception, payana_activity_guide_thumbnail_name_space)

        activity_guide_thumbnail_table_object = request.json

        if activity_guide_thumbnail_table_object is None:
            raise KeyError(payana_activity_guide_thumbnail_profile_object,
                           payana_activity_guide_thumbnail_name_space)

        payana_activity_guide_thumbnail_read_obj = PayanaBigTable(payana_activity_guide_thumbnail_table)

        for column_family, _ in activity_guide_thumbnail_table_object.items():

            payana_activity_guide_thumbnail_table_delete_wrapper = bigtable_write_object_wrapper(
                city, column_family, "", "")

            payana_activity_guide_thumbnail_obj_delete_status = payana_activity_guide_thumbnail_read_obj.delete_bigtable_row_column_family_cells(
                payana_activity_guide_thumbnail_table_delete_wrapper)

            if not payana_activity_guide_thumbnail_obj_delete_status:
                raise Exception(
                    payana_activity_guide_thumbnail_table_objects_delete_failure_message, payana_activity_guide_thumbnail_name_space)

        return {
            status: payana_200_response,
            payana_city_header: city,
            message: payana_activity_guide_thumbnail_table_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
