from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_country_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_country_cities_name_space = Namespace(
    'country/city', description='Manage cities in a country information')

payana_country_cities_write_success_message_post = payana_service_constants.payana_country_cities_write_success_message_post
payana_country_cities_write_success_message_put = payana_service_constants.payana_country_cities_write_success_message_put
payana_country_cities_write_failure_message_post = payana_service_constants.payana_country_cities_write_failure_message_post
payana_country_cities_create_failure_message_post = payana_service_constants.payana_country_cities_create_failure_message_post
payana_country_cities_delete_failure_message = payana_service_constants.payana_country_cities_delete_failure_message
payana_country_cities_delete_success_message = payana_service_constants.payana_country_cities_delete_success_message
payana_country_cities_objects_delete_failure_message = payana_service_constants.payana_country_cities_objects_delete_failure_message
payana_country_cities_objects_delete_success_message = payana_service_constants.payana_country_cities_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_country_header = payana_service_constants.payana_country_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_country_header_exception = payana_service_constants.payana_missing_country_header_exception
payana_missing_country_cities_object = payana_service_constants.payana_missing_country_cities_object
payana_place_country_table = bigtable_constants.payana_place_country_table


@payana_country_cities_name_space.route("/")
class PayanaCountryCityEndPoint(Resource):

    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)

        payana_country_city_read_obj = PayanaBigTable(
            payana_place_country_table)

        row_key = str(country)

        payana_country_city_obj = payana_country_city_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_country_city_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_country_cities_name_space)

        return payana_country_city_obj, payana_200

    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)

        profile_country_city_read_obj = request.json

        payana_country_city_object = PayanaCountryTable(
            **profile_country_city_read_obj)
        payana_country_city_obj_write_status = payana_country_city_object.update_country_bigtable()

        if not payana_country_city_obj_write_status:
            raise Exception(
                payana_country_cities_create_failure_message_post, payana_country_cities_name_space)

        return {
            status: payana_201_response,
            payana_country_header: country,
            message: payana_country_cities_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)

        profile_country_city_read_obj = request.json

        payana_country_city_object = PayanaCountryTable(
            **profile_country_city_read_obj)
        payana_country_city_obj_write_status = payana_country_city_object.update_country_bigtable()

        if not payana_country_city_obj_write_status:
            raise Exception(
                payana_country_cities_create_failure_message_post, payana_country_cities_name_space)

        return {
            status: payana_200_response,
            payana_country_header: country,
            message: payana_country_cities_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_country_cities_name_space.route("/delete/")
class PayanaCountryCityRowDeleteEndPoint(Resource):
    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)

        profile_country_city_read_obj = PayanaBigTable(
            payana_place_country_table)

        payana_country_city_obj_delete_status = profile_country_city_read_obj.delete_bigtable_row_with_row_key(
            country)

        if not payana_country_city_obj_delete_status:
            raise Exception(
                payana_country_cities_delete_failure_message, payana_country_cities_name_space)

        return {
            status: payana_200_response,
            payana_country_header: country,
            message: payana_country_cities_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_country_cities_name_space.route("/delete/values/")
class PayanaCountryCityColumnValuesDeleteEndPoint(Resource):

    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)

        payana_country_city_object = request.json

        if payana_country_city_object is None:
            raise KeyError(payana_missing_country_cities_object,
                           payana_country_cities_name_space)

        payana_country_city_read_obj = PayanaBigTable(
            payana_place_country_table)
        
        payana_country_city_obj_delete_status = payana_country_city_read_obj.delete_bigtable_row_column_list(
            country, payana_country_city_object)

        if not payana_country_city_obj_delete_status:
            raise Exception(
                payana_country_cities_objects_delete_failure_message, payana_country_cities_name_space)

        return {
            status: payana_200_response,
            payana_country_header: country,
            message: payana_country_cities_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_country_cities_name_space.route("/delete/cf/")
class PayanaLCountryCityColumnFamilyDeleteEndPoint(Resource):
    @payana_country_cities_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        country = get_country_header(request)

        if country is None or len(country) == 0:
            raise KeyError(
                payana_missing_country_header_exception, payana_country_cities_name_space)
            
        payana_country_city_object = request.json

        if payana_country_city_object is None:
            raise KeyError(payana_missing_country_cities_object,
                           payana_country_cities_name_space)

        payana_country_city_read_obj = PayanaBigTable(
            payana_place_country_table)
        
        for column_family, _ in payana_country_city_object.items():

            payana_country_city_delete_wrapper = bigtable_write_object_wrapper(
                country, column_family, "", "")

            payana_country_city_obj_delete_status = payana_country_city_read_obj.delete_bigtable_row_column_family_cells(
                payana_country_city_delete_wrapper)

            if not payana_country_city_obj_delete_status:
                raise Exception(
                    payana_country_cities_objects_delete_failure_message, payana_country_cities_name_space)

        return {
            status: payana_200_response,
            payana_country_header: country,
            message: payana_country_cities_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
