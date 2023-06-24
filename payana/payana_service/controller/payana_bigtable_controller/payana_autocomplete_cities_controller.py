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
from payana.payana_bl.bigtable_utils.PayanaCitiesAutocompleteTable import PayanaCitiesAutocompleteTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_autocomplete_cities_name_space = Namespace(
    'autocomplete/city', description='Manage autocomplete cities for a given city information')

payana_autocomplete_cities_write_success_message_post = payana_service_constants.payana_autocomplete_cities_write_success_message_post
payana_autocomplete_cities_write_success_message_put = payana_service_constants.payana_autocomplete_cities_write_success_message_put
payana_autocomplete_cities_write_failure_message_post = payana_service_constants.payana_autocomplete_cities_write_failure_message_post
payana_autocomplete_cities_create_failure_message_post = payana_service_constants.payana_autocomplete_cities_create_failure_message_post
payana_autocomplete_cities_delete_failure_message = payana_service_constants.payana_autocomplete_cities_delete_failure_message
payana_autocomplete_cities_delete_success_message = payana_service_constants.payana_autocomplete_cities_delete_success_message
payana_autocomplete_cities_objects_delete_failure_message = payana_service_constants.payana_autocomplete_cities_objects_delete_failure_message
payana_autocomplete_cities_objects_delete_success_message = payana_service_constants.payana_autocomplete_cities_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_autocomplete_city_header = payana_service_constants.payana_autocomplete_city_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_autocomplete_cities_header_exception = payana_service_constants.payana_missing_autocomplete_cities_header_exception
payana_autocomplete_cities_missing_object = payana_service_constants.payana_autocomplete_cities_missing_object
payana_city_autocomplete_table = bigtable_constants.payana_city_autocomplete_table


@payana_autocomplete_cities_name_space.route("/")
class PayanaAutocompleteCityEndPoint(Resource):

    @payana_autocomplete_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_autocomplete_cities_header_exception, payana_autocomplete_cities_name_space)

        payana_autocomplete_city_read_obj = PayanaBigTable(
            payana_city_autocomplete_table)

        row_key = bigtable_constants.payana_city_autocomplete_row_key
        city_regex = str(city)

        payana_autocomplete_city_obj = payana_autocomplete_city_read_obj.get_row_cells_column_qualifier(
            row_key, city_regex, include_column_family=True)

        if len(payana_autocomplete_city_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_autocomplete_cities_name_space)

        return payana_autocomplete_city_obj, payana_200

    @payana_autocomplete_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_autocomplete_city_read_obj = request.json

        payana_autocomplete_city_object = PayanaCitiesAutocompleteTable(
            **profile_autocomplete_city_read_obj)
        payana_autocomplete_city_obj_write_status = payana_autocomplete_city_object.update_autocomplete_city_list_bigtable()

        if not payana_autocomplete_city_obj_write_status:
            raise Exception(
                payana_autocomplete_cities_create_failure_message_post, payana_autocomplete_cities_name_space)

        return {
            status: payana_201_response,
            payana_autocomplete_city_header: bigtable_constants.payana_city_autocomplete_column_family,
            message: payana_autocomplete_cities_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_autocomplete_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        profile_autocomplete_city_read_obj = request.json

        payana_autocomplete_city_object = PayanaCitiesAutocompleteTable(
            **profile_autocomplete_city_read_obj)
        payana_autocomplete_city_obj_write_status = payana_autocomplete_city_object.update_autocomplete_city_list_bigtable()

        if not payana_autocomplete_city_obj_write_status:
            raise Exception(
                payana_autocomplete_cities_create_failure_message_post, payana_autocomplete_cities_name_space)

        return {
            status: payana_200_response,
            payana_autocomplete_city_header: bigtable_constants.payana_city_autocomplete_column_family,
            message: payana_autocomplete_cities_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_autocomplete_cities_name_space.route("/delete/")
class PayanaAutocompleteCityRowDeleteEndPoint(Resource):
    @payana_autocomplete_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_autocomplete_cities_header_exception, payana_autocomplete_cities_name_space)

        profile_autocomplete_city_read_obj = PayanaBigTable(
            payana_city_autocomplete_table)

        payana_autocomplete_city_obj_delete_status = profile_autocomplete_city_read_obj.delete_bigtable_row_with_row_key(
            city)

        if not payana_autocomplete_city_obj_delete_status:
            raise Exception(
                payana_autocomplete_cities_delete_failure_message, payana_autocomplete_cities_name_space)

        return {
            status: payana_200_response,
            payana_autocomplete_city_header: city,
            message: payana_autocomplete_cities_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_autocomplete_cities_name_space.route("/delete/values/")
class PayanaAutocompleteCityColumnValuesDeleteEndPoint(Resource):

    @payana_autocomplete_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        city = get_city_header(request)

        if city is None or len(city) == 0:
            raise KeyError(
                payana_missing_autocomplete_cities_header_exception, payana_autocomplete_cities_name_space)

        payana_autocomplete_city_object = request.json

        if payana_autocomplete_city_object is None:
            raise KeyError(payana_autocomplete_cities_missing_object,
                           payana_autocomplete_cities_name_space)

        payana_autocomplete_city_read_obj = PayanaBigTable(
            payana_city_autocomplete_table)
        
        payana_autocomplete_city_obj_delete_status = payana_autocomplete_city_read_obj.delete_bigtable_row_column_list(
            city, payana_autocomplete_city_object)

        if not payana_autocomplete_city_obj_delete_status:
            raise Exception(
                payana_autocomplete_cities_objects_delete_failure_message, payana_autocomplete_cities_name_space)

        return {
            status: payana_200_response,
            payana_autocomplete_city_header: city,
            message: payana_autocomplete_cities_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
