from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_profile_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaGlobalInfluencerFeedSearchItineraryCache import PayanaGlobalInfluencerFeedSearchItineraryCache
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_global_city_influencers_feed_search_itinerary_cache_name_space = Namespace(
    'feed/search/', description='Manage the CRUD operations of the global influencers feed search itinerary cache table')

payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_post = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_post
payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_put = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_put
payana_global_influencers_feed_search_itinerary_cache_objects_write_failure_message_post = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_write_failure_message_post
payana_global_influencers_feed_search_itinerary_cache_objects_create_failure_message_post = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_create_failure_message_post
payana_global_influencers_feed_search_itinerary_cache_objects_delete_failure_message = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_delete_failure_message
payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_success_message = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_success_message
payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_failure_message = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_failure_message
payana_global_influencers_feed_search_itinerary_cache_objects_delete_success_message = payana_service_constants.payana_global_influencers_feed_search_itinerary_cache_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_influencers_feed_search_itinerary_profile_id_header = payana_service_constants.payana_influencers_feed_search_itinerary_profile_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception = payana_service_constants.payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception
payana_missing_influencers_feed_search_itinerary_cache_itinerary_object = payana_service_constants.payana_missing_influencers_feed_search_itinerary_cache_itinerary_object
payana_global_influencer_feed_search_itinerary_cache_table = bigtable_constants.payana_global_influencer_feed_search_itinerary_cache_table


@payana_global_city_influencers_feed_search_itinerary_cache_name_space.route("/")
class PayanaGlobalInfluencerFeedSearchItineraryCacheObjectEndPoint(Resource):

    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_read_obj = PayanaBigTable(
            payana_global_influencer_feed_search_itinerary_cache_table)

        row_key = str(profile_id)

        payana_global_influencer_feed_search_itinerary_cache_obj = payana_global_influencer_feed_search_itinerary_cache_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_global_influencer_feed_search_itinerary_cache_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return payana_global_influencer_feed_search_itinerary_cache_obj, payana_200

    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        profile_global_influencer_feed_search_itinerary_cache_read_obj = request.json

        payana_global_influencer_feed_search_itinerary_cache_object = PayanaGlobalInfluencerFeedSearchItineraryCache(
            **profile_global_influencer_feed_search_itinerary_cache_read_obj)
        payana_global_influencer_feed_search_itinerary_cache_obj_write_status = payana_global_influencer_feed_search_itinerary_cache_object.update_feed_search_itinerary_bigtable()

        if not payana_global_influencer_feed_search_itinerary_cache_obj_write_status:
            raise Exception(
                payana_global_influencers_feed_search_itinerary_cache_objects_create_failure_message_post, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return {
            status: payana_201_response,
            payana_influencers_feed_search_itinerary_profile_id_header: profile_id,
            message: payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_object = request.json

        profile_global_influencer_feed_search_itinerary_cache_read_obj = request.json

        payana_global_influencer_feed_search_itinerary_cache_object = PayanaGlobalInfluencerFeedSearchItineraryCache(
            **profile_global_influencer_feed_search_itinerary_cache_read_obj)
        payana_global_influencer_feed_search_itinerary_cache_obj_write_status = payana_global_influencer_feed_search_itinerary_cache_object.update_feed_search_itinerary_bigtable()

        if not payana_global_influencer_feed_search_itinerary_cache_obj_write_status:
            raise Exception(
                payana_global_influencers_feed_search_itinerary_cache_objects_create_failure_message_post, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return {
            status: payana_200_response,
            payana_influencers_feed_search_itinerary_profile_id_header: profile_id,
            message: payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_global_city_influencers_feed_search_itinerary_cache_name_space.route("/delete/")
class PayanaGlobalInfluencerFeedSearchItineraryCacheObjectRowDeleteEndPoint(Resource):
    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        profile_global_influencer_feed_search_itinerary_cache_read_obj = PayanaBigTable(
            payana_global_influencer_feed_search_itinerary_cache_table)

        payana_global_influencer_feed_search_itinerary_cache_obj_delete_status = profile_global_influencer_feed_search_itinerary_cache_read_obj.delete_bigtable_row_with_row_key(
            profile_id)

        if not payana_global_influencer_feed_search_itinerary_cache_obj_delete_status:
            raise Exception(
                payana_global_influencers_feed_search_itinerary_cache_objects_delete_failure_message, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return {
            status: payana_200_response,
            payana_influencers_feed_search_itinerary_profile_id_header: profile_id,
            message: payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_global_city_influencers_feed_search_itinerary_cache_name_space.route("/delete/values/")
class PayanaGlobalInfluencerFeedSearchItineraryCacheObjectColumnValuesDeleteEndPoint(Resource):

    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_object = request.json

        if payana_global_influencer_feed_search_itinerary_cache_object is None:
            raise KeyError(payana_missing_influencers_feed_search_itinerary_cache_itinerary_object,
                           payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_read_obj = PayanaBigTable(
            payana_global_influencer_feed_search_itinerary_cache_table)

        payana_global_influencer_feed_search_itinerary_cache_obj_delete_status = payana_global_influencer_feed_search_itinerary_cache_read_obj.delete_bigtable_row_column_list(
            profile_id, payana_global_influencer_feed_search_itinerary_cache_object)

        if not payana_global_influencer_feed_search_itinerary_cache_obj_delete_status:
            raise Exception(
                payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_failure_message, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return {
            status: payana_200_response,
            payana_influencers_feed_search_itinerary_profile_id_header: profile_id,
            message: payana_global_influencers_feed_search_itinerary_cache_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_global_city_influencers_feed_search_itinerary_cache_name_space.route("/delete/cf/")
class PayanaGlobalInfluencerFeedSearchItineraryCacheObjectColumnFamilyDeleteEndPoint(Resource):
    @payana_global_city_influencers_feed_search_itinerary_cache_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_object = request.json

        if payana_global_influencer_feed_search_itinerary_cache_object is None:
            raise KeyError(payana_missing_influencers_feed_search_itinerary_cache_itinerary_object,
                           payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        payana_global_influencer_feed_search_itinerary_cache_read_obj = PayanaBigTable(
            payana_global_influencer_feed_search_itinerary_cache_table)

        for column_family, _ in payana_global_influencer_feed_search_itinerary_cache_object.items():

            payana_global_influencer_feed_search_itinerary_cache_delete_wrapper = bigtable_write_object_wrapper(
                profile_id, column_family, "", "")

            payana_global_influencer_feed_search_itinerary_cache_obj_delete_status = payana_global_influencer_feed_search_itinerary_cache_read_obj.delete_bigtable_row_column_family_cells(
                payana_global_influencer_feed_search_itinerary_cache_delete_wrapper)

            if not payana_global_influencer_feed_search_itinerary_cache_obj_delete_status:
                raise Exception(
                    payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_failure_message, payana_global_city_influencers_feed_search_itinerary_cache_name_space)

        return {
            status: payana_200_response,
            payana_influencers_feed_search_itinerary_profile_id_header: profile_id,
            message: payana_global_influencers_feed_search_itinerary_cache_objects_delete_success_message,
            status_code: payana_200
        }, payana_200
