from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_city_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaGlobalCityRatingItineraryTable import PayanaGlobalCityRatingItineraryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_global_city_itinerary_rating_name_space = Namespace(
    'global/rating/city', description='Manage the CRUD operations of the global city rating itinerary table')

payana_global_city_rating_itinerary_objects_write_success_message_post = payana_service_constants.payana_global_city_rating_itinerary_objects_write_success_message_post
payana_global_city_rating_itinerary_objects_write_success_message_put = payana_service_constants.payana_global_city_rating_itinerary_objects_write_success_message_put
payana_global_city_rating_itinerary_objects_write_failure_message_post = payana_service_constants.payana_global_city_rating_itinerary_objects_write_failure_message_post
payana_global_city_rating_itinerary_objects_create_failure_message_post = payana_service_constants.payana_global_city_rating_itinerary_objects_create_failure_message_post
payana_global_city_rating_itinerary_objects_delete_failure_message = payana_service_constants.payana_global_city_rating_itinerary_objects_delete_failure_message
payana_global_city_rating_itinerary_objects_values_delete_success_message = payana_service_constants.payana_global_city_rating_itinerary_objects_values_delete_success_message
payana_global_city_rating_itinerary_objects_values_delete_failure_message = payana_service_constants.payana_global_city_rating_itinerary_objects_values_delete_failure_message
payana_global_city_rating_itinerary_objects_delete_success_message = payana_service_constants.payana_global_city_rating_itinerary_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_global_city_rating_itinerary_id_header = payana_service_constants.payana_global_city_rating_itinerary_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_global_city_rating_itinerary_objects_header_exception = payana_service_constants.payana_missing_global_city_rating_itinerary_objects_header_exception
payana_missing_global_city_rating_itinerary_object = payana_service_constants.payana_missing_global_city_rating_itinerary_object
payana_global_city_itinerary_table = bigtable_constants.payana_global_city_itinerary_table


@payana_global_city_itinerary_rating_name_space.route("/")
class PayanaGlobalCityRatingItineraryObjectEndPoint(Resource):

    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        payana_global_city_itinerary_rating_read_obj = PayanaBigTable(
            payana_global_city_itinerary_table)

        row_key = str(city)

        payana_global_city_itinerary_rating_obj = payana_global_city_itinerary_rating_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_global_city_itinerary_rating_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_global_city_itinerary_rating_name_space)

        return payana_global_city_itinerary_rating_obj, payana_200

    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        profile_global_city_itinerary_rating_read_obj = request.json

        payana_global_city_itinerary_rating_object = PayanaGlobalCityRatingItineraryTable(
            **profile_global_city_itinerary_rating_read_obj)
        payana_global_city_itinerary_rating_obj_write_status = payana_global_city_itinerary_rating_object.update_global_city_itinerary_bigtable()

        if not payana_global_city_itinerary_rating_obj_write_status:
            raise Exception(
                payana_global_city_rating_itinerary_objects_create_failure_message_post, payana_global_city_itinerary_rating_name_space)

        return {
            status: payana_201_response,
            payana_global_city_rating_itinerary_id_header: city,
            message: payana_global_city_rating_itinerary_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        payana_global_city_itinerary_rating_object = request.json

        profile_global_city_itinerary_rating_read_obj = request.json

        payana_global_city_itinerary_rating_object = PayanaGlobalCityRatingItineraryTable(
            **profile_global_city_itinerary_rating_read_obj)
        payana_global_city_itinerary_rating_obj_write_status = payana_global_city_itinerary_rating_object.update_global_city_itinerary_bigtable()

        if not payana_global_city_itinerary_rating_obj_write_status:
            raise Exception(
                payana_global_city_rating_itinerary_objects_create_failure_message_post, payana_global_city_itinerary_rating_name_space)

        return {
            status: payana_200_response,
            payana_global_city_rating_itinerary_id_header: city,
            message: payana_global_city_rating_itinerary_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_global_city_itinerary_rating_name_space.route("/delete/")
class PayanaGlobalCityRatingItineraryObjectRowDeleteEndPoint(Resource):
    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        profile_global_city_rating_itinerary_read_obj = PayanaBigTable(
            payana_global_city_itinerary_table)

        payana_global_city_rating_itinerary_obj_delete_status = profile_global_city_rating_itinerary_read_obj.delete_bigtable_row_with_row_key(
            city)

        if not payana_global_city_rating_itinerary_obj_delete_status:
            raise Exception(
                payana_global_city_rating_itinerary_objects_delete_failure_message, payana_global_city_itinerary_rating_name_space)

        return {
            status: payana_200_response,
            payana_global_city_rating_itinerary_id_header: city,
            message: payana_global_city_rating_itinerary_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_global_city_itinerary_rating_name_space.route("/delete/values/")
class PayanaGlobalCityRatingItineraryObjectColumnValuesDeleteEndPoint(Resource):

    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        payana_global_city_rating_itinerary_object = request.json

        if payana_global_city_rating_itinerary_object is None:
            raise KeyError(payana_missing_global_city_rating_itinerary_object,
                           payana_global_city_itinerary_rating_name_space)

        payana_global_city_rating_itinerary_read_obj = PayanaBigTable(
            payana_global_city_itinerary_table)

        payana_global_city_rating_itinerary_obj_delete_status = payana_global_city_rating_itinerary_read_obj.delete_bigtable_row_column_list(
            city, payana_global_city_rating_itinerary_object)

        if not payana_global_city_rating_itinerary_obj_delete_status:
            raise Exception(
                payana_global_city_rating_itinerary_objects_values_delete_failure_message, payana_global_city_itinerary_rating_name_space)

        return {
            status: payana_200_response,
            payana_global_city_rating_itinerary_id_header: city,
            message: payana_global_city_rating_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_global_city_itinerary_rating_name_space.route("/delete/cf/")
class PayanaGlobalCityRatingItineraryObjectColumnFamilyDeleteEndPoint(Resource):
    @payana_global_city_itinerary_rating_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_global_city_rating_itinerary_objects_header_exception, payana_global_city_itinerary_rating_name_space)

        payana_global_city_rating_itinerary_object = request.json

        if payana_global_city_rating_itinerary_object is None:
            raise KeyError(payana_missing_global_city_rating_itinerary_object,
                           payana_global_city_itinerary_rating_name_space)

        payana_global_city_rating_itinerary_read_obj = PayanaBigTable(
            payana_global_city_itinerary_table)

        for column_family, _ in payana_global_city_rating_itinerary_object.items():

            payana_global_city_rating_itinerary_delete_wrapper = bigtable_write_object_wrapper(
                city, column_family, "", "")

            payana_global_city_rating_itinerary_obj_delete_status = payana_global_city_rating_itinerary_read_obj.delete_bigtable_row_column_family_cells(
                payana_global_city_rating_itinerary_delete_wrapper)

            if not payana_global_city_rating_itinerary_obj_delete_status:
                raise Exception(
                    payana_global_city_rating_itinerary_objects_values_delete_failure_message, payana_global_city_itinerary_rating_name_space)

        return {
            status: payana_200_response,
            payana_global_city_rating_itinerary_id_header: city,
            message: payana_global_city_rating_itinerary_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
