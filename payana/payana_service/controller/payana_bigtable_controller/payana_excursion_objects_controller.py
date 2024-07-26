import copy
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_excursion_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.models.payana_bigtable_models.payana_itinerary_flow_model import payana_excursion_object_model, payana_itinerary_object_model, profile_page_itinerary_model
from payana.payana_service.controller.payana_bigtable_controller.payana_bigtable_controller_utils.payana_bigtable_controller_itinerary_creation_utils import get_profile_page_itinerary_table, get_itinerary_object, delete_excursion_object, delete_itinerary_object, delete_profile_page_itinerary_object_column_values

payana_excursion_objects_name_space = Namespace(
    'excursion', description='Manage the CRUD operations of the excursion table')

payana_excursion_objects_write_success_message_post = payana_service_constants.payana_excursion_objects_write_success_message_post
payana_excursion_objects_write_success_message_put = payana_service_constants.payana_excursion_objects_write_success_message_put
payana_excursion_objects_write_failure_message_post = payana_service_constants.payana_excursion_objects_write_failure_message_post
payana_excursion_objects_create_failure_message_post = payana_service_constants.payana_excursion_objects_create_failure_message_post
payana_excursion_objects_delete_failure_message = payana_service_constants.payana_excursion_objects_delete_failure_message
payana_excursion_objects_values_delete_success_message = payana_service_constants.payana_excursion_objects_values_delete_success_message
payana_excursion_objects_values_delete_failure_message = payana_service_constants.payana_excursion_objects_values_delete_failure_message
payana_excursion_objects_delete_success_message = payana_service_constants.payana_excursion_objects_delete_success_message

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_excursion_id_header = payana_service_constants.payana_excursion_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_excursion_objects_header_exception = payana_service_constants.payana_missing_excursion_objects_header_exception
payana_missing_excursion_object = payana_service_constants.payana_missing_excursion_object
payana_excursion_table = bigtable_constants.payana_excursion_table


@payana_excursion_objects_name_space.route("/")
class PayanaExcursionObjectEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        row_key = str(excursion_id)

        payana_excursion_obj = payana_excursion_read_obj.get_row_dict(
            row_key, include_column_family=True)

        if len(payana_excursion_obj) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_excursion_objects_name_space)

        return payana_excursion_obj, payana_200

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_excursion_read_obj = request.json

        payana_excursion_object = PayanaExcursionTable(
            **profile_excursion_read_obj)
        payana_excursion_obj_write_status = payana_excursion_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        excursion_id = payana_excursion_object.excursion_id

        return {
            status: payana_201_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def put(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)

        payana_excursion_obj_write_status = payana_excursion_read_obj.insert_columns_column_family(
            excursion_id, payana_excursion_object)

        if not payana_excursion_obj_write_status:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_put,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/")
class PayanaExcursionObjectRowDeleteEndPoint(Resource):
    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        profile_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        payana_excursion_obj_delete_status = profile_excursion_read_obj.delete_bigtable_row_with_row_key(
            excursion_id)

        if not payana_excursion_obj_delete_status:
            raise Exception(
                payana_excursion_objects_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_values_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/values/")
class PayanaExcursionObjectColumnValuesDeleteEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        if payana_excursion_object is None:
            raise KeyError(payana_missing_excursion_object,
                           payana_excursion_objects_name_space)

        payana_excursion_read_obj = PayanaBigTable(
            payana_excursion_table)

        payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row_column_list(
            excursion_id, payana_excursion_object)

        if not payana_excursion_obj_delete_status:
            raise Exception(
                payana_excursion_objects_values_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/delete/cf/")
class PayanaExcursionObjectColumnFamilyDeleteEndPoint(Resource):
    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        excursion_id = get_excursion_id_header(request)

        if excursion_id is None or len(excursion_id) == 0:
            raise KeyError(
                payana_missing_excursion_objects_header_exception, payana_excursion_objects_name_space)

        payana_excursion_object = request.json

        if payana_excursion_object is None:
            raise KeyError(payana_missing_excursion_object,
                           payana_excursion_objects_name_space)

        payana_excursion_checkin_permission_read_obj = PayanaBigTable(
            payana_excursion_table)

        for column_family, _ in payana_excursion_object.items():

            payana_excursion_delete_wrapper = bigtable_write_object_wrapper(
                excursion_id, column_family, "", "")

            payana_excursion_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column_family_cells(
                payana_excursion_delete_wrapper)

            if not payana_excursion_obj_delete_status:
                raise Exception(
                    payana_excursion_objects_values_delete_failure_message, payana_excursion_objects_name_space)

        return {
            status: payana_200_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_delete_success_message,
            status_code: payana_200
        }, payana_200


@payana_excursion_objects_name_space.route("/create/")
class PayanaExcursionTransactionEndPoint(Resource):

    @payana_excursion_objects_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        payana_itinerary_create_payload = request.json

        # To-Do: Refactor

        # Step 1 - Create an excursion object
        profile_excursion_read_obj = copy.deepcopy(
            payana_excursion_object_model)

        profile_excursion_read_obj[bigtable_constants.payana_excursion_activities_list] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_activities_list]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_activity_guide] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_activity_guide]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_create_timestamp] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][bigtable_constants.payana_excursion_column_family_last_updated_timestamp] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_excursion_read_obj[bigtable_constants.payana_excursion_metadata][
            bigtable_constants.payana_excursion_column_family_description] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]

        payana_excursion_object = PayanaExcursionTable(
            **profile_excursion_read_obj)
        payana_excursion_object.generate_excursion_id()

        excursion_id = payana_excursion_object.excursion_id

        if excursion_id is None or len(excursion_id) == 0:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Step 2 - Get profile Itinerary object
        row_key = str(
            payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id])

        payana_profile_page_itinerary_read_obj_dict = get_profile_page_itinerary_table(
            payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id])

        itinerary_name = ", ".join(
            payana_itinerary_create_payload[bigtable_constants.payana_itinerary_column_family_cities_list])

        running_itinerary_count = 0
        itinerary_id = ""

        if payana_profile_page_itinerary_read_obj_dict is not None and not len(payana_profile_page_itinerary_read_obj_dict) == 0:

            # Step 3 - Find the itinerary ID/count
            column_qualifier = "_".join([bigtable_constants.payana_generic_activity_column_family,
                                        bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value])

            if column_qualifier in payana_profile_page_itinerary_read_obj_dict[row_key] and itinerary_name in payana_profile_page_itinerary_read_obj_dict[row_key][column_qualifier]:
                itinerary_id = payana_profile_page_itinerary_read_obj_dict[
                    row_key][column_qualifier][itinerary_name]

            # Step 4 - Get the excursion count itinerary object (if it exists)
            if itinerary_id is not None and not len(itinerary_id) == 0:
                row_key = str(itinerary_id)

                payana_itinerary_obj = get_itinerary_object(itinerary_id)

                if len(payana_itinerary_obj) == 0:
                    raise KeyError(payana_empty_row_read_exception,
                                   payana_excursion_objects_name_space)

                running_itinerary_count = max([int(iter) for iter in payana_itinerary_obj[itinerary_id]
                                              [bigtable_constants.payana_itinerary_column_family_excursion_id_list].keys()])

        running_itinerary_count += 1

        # Step 5 - Create an itinerary object
        profile_itinerary_read_obj = copy.deepcopy(
            payana_itinerary_object_model)

        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_column_family_excursion_id_list] = {
            str(running_itinerary_count): excursion_id}
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_activities_list] = payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][
            bigtable_constants.payana_itinerary_column_family_description] = itinerary_name

        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][
            bigtable_constants.payana_itinerary_column_family_itinerary_owner_profile_id] = payana_itinerary_create_payload[bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_metadata][bigtable_constants.payana_itinerary_last_updated_timestamp] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_create_timestamp]
        profile_itinerary_read_obj[bigtable_constants.payana_itinerary_column_family_cities_list] = payana_itinerary_create_payload[
            bigtable_constants.payana_itinerary_column_family_cities_list]

        payana_itinerary_object = PayanaItineraryTable(
            **profile_itinerary_read_obj)

        if itinerary_id is None or len(itinerary_id) == 0:
            payana_itinerary_object.generate_itinerary_id()
        else:
            payana_itinerary_object.itinerary_id = itinerary_id

        itinerary_id = payana_itinerary_object.itinerary_id

        # Step 6 - Update itinerary ID/Name in excursion object
        payana_excursion_object.excursion_itinerary_id = itinerary_id
        payana_excursion_object.excursion_itinerary_name = itinerary_name

        # Step 7 - Add to the user's profile itinerary list object
        profile_page_itinerary_read_obj = copy.deepcopy(
            profile_page_itinerary_model)

        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_profile_id] = payana_itinerary_create_payload[
            bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]
        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value] = {
            itinerary_name: itinerary_id}

        if payana_itinerary_create_payload[bigtable_constants.payana_excursion_activity_guide].lower() == "true":
            profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value] = {
                payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]: excursion_id}
        else:
            profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value] = {
                payana_itinerary_create_payload[bigtable_constants.payana_excursion_name]: excursion_id}

        profile_page_itinerary_read_obj[bigtable_constants.payana_profile_page_itinerary_table_activities] = list(
            payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list].keys())

        payana_profile_page_itinerary_object = PayanaProfilePageItineraryTable(
            **profile_page_itinerary_read_obj)

        # Step 8 - BigTable write across all 3 tables - excursion, itinerary, profile itinerary table
        # Excursion table
        payana_excursion_obj_write_status = payana_excursion_object.update_excursion_bigtable()

        if not payana_excursion_obj_write_status:
            raise Exception(
                payana_excursion_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Itinerary table
        payana_itinerary_obj_write_status = payana_itinerary_object.update_itinerary_bigtable()
        print(excursion_id)

        if not payana_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table column value entry
            payana_revert_itinerary_object = {
                bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
                    str(running_itinerary_count): excursion_id}
            }

            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_revert_itinerary_object)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            raise Exception(
                payana_service_constants.payana_itinerary_objects_create_failure_message_post, payana_excursion_objects_name_space)

        # Profile itinerary table
        payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_object.update_payana_profile_page_itinerary_bigtable()
        print(itinerary_id)
        if not payana_profile_page_itinerary_obj_write_status:
            # delete excursion object
            payana_excursion_obj_delete_status = delete_excursion_object(
                excursion_id)

            if not payana_excursion_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete itinerary table object
            payana_revert_itinerary_object = {
                bigtable_constants.payana_itinerary_column_family_excursion_id_list: {
                    str(running_itinerary_count): excursion_id}
            }
            payana_itinerary_obj_delete_status = delete_itinerary_object(
                itinerary_id, payana_revert_itinerary_object)

            if not payana_itinerary_obj_delete_status:
                # Add logging here to auto-handle failed requests as CRON job once a day
                pass

            # delete profile page itinerary object
            payana_profile_page_itinerary_table_delete_wrappers = []
            profile_page_itinerary_object = {}

            for column_family, column_family_dict in profile_page_itinerary_object.items():

                for activity in payana_itinerary_create_payload[bigtable_constants.payana_itinerary_activities_list]:
                    activity_column_family_mapping = "_".join(
                        [activity, column_family])

                    # Delete specific column family and column values
                    for column_quantifier, column_value in column_family_dict.items():
                        payana_profile_page_itinerary_table_delete_wrapper = bigtable_write_object_wrapper(
                            payana_itinerary_create_payload[
                                bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id], activity_column_family_mapping, column_quantifier, column_value)

                        payana_profile_page_itinerary_table_delete_wrappers.append(
                            payana_profile_page_itinerary_table_delete_wrapper)

            payana_profile_page_itinerary_obj_delete_status = delete_profile_page_itinerary_object_column_values(
                payana_profile_page_itinerary_table_delete_wrappers)

            if not payana_profile_page_itinerary_obj_delete_status:
                # Add logging
                pass

            raise Exception(
                payana_service_constants.payana_profile_page_itineraries_create_failure_message_post, payana_excursion_objects_name_space)

        return {
            status: payana_201_response,
            payana_excursion_id_header: excursion_id,
            message: payana_excursion_objects_write_success_message_post,
            status_code: payana_201
        }, payana_201
