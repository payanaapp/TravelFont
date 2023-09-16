from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_gcs_object_id_header, get_gcs_bucket_id_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.cloud_storage_utils.PayanaGCSObjectMetadata import PayanaGCSObjectMetadata
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_bl.cloud_storage_utils.payana_delete_storage_object import payana_delete_storage_object

payana_gcs_object_name_space = Namespace(
    'gcs/object', description='Manage read/write/edit for GCS object entitities')

payana_gcs_object_success_message_delete = payana_service_constants.payana_gcs_object_success_message_delete
payana_gcs_object_failure_message_delete = payana_service_constants.payana_gcs_object_failure_message_delete
payana_gcs_object_metadata_success_message_update = payana_service_constants.payana_gcs_object_metadata_success_message_update
payana_gcs_object_metadata_failure_message_update = payana_service_constants.payana_gcs_object_metadata_failure_message_update
payana_gcs_object_cors_policy_success_message_update = payana_service_constants.payana_gcs_object_cors_policy_success_message_update
payana_gcs_object_cors_policy_failure_message_update = payana_service_constants.payana_gcs_object_cors_policy_failure_message_update
payana_gcs_object_metadata_success_message_get = payana_service_constants.payana_gcs_object_metadata_success_message_get
payana_gcs_object_metadata_failure_message_get = payana_service_constants.payana_gcs_object_metadata_failure_message_get
payana_gcs_bucket_header = payana_service_constants.payana_gcs_bucket_header
payana_gcs_object_header = payana_service_constants.payana_gcs_object_header
payana_gcs_object_metadata_header = payana_service_constants.payana_gcs_object_metadata_header
payana_gcs_cors_header = payana_service_constants.payana_gcs_cors_header
payana_gcs_object_header_missing_exception = payana_service_constants.payana_gcs_object_header_missing_exception
payana_gcs_bucket_header_missing_exception  = payana_service_constants.payana_gcs_bucket_header_missing_exception
payana_gcs_metadata_header_missing_exception  = payana_service_constants.payana_gcs_metadata_header_missing_exception
payana_gcs_cors_metadata_missing_exception  = payana_service_constants.payana_gcs_cors_metadata_missing_exception

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500


@payana_gcs_object_name_space.route("/metadata/")
class PayanaGCSObjectMetadataURLEndPoint(Resource):

    @payana_gcs_object_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_gcs_object_header_missing_exception, payana_gcs_object_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_gcs_bucket_header_missing_exception, payana_gcs_object_name_space)

        payana_metadata_gcs_read_obj = PayanaGCSObjectMetadata(gcs_bucket_id, gcs_object_id)

        payana_metadata_obj = payana_metadata_gcs_read_obj.get_metadata()
        print(payana_metadata_obj)

        if payana_metadata_obj is None:
            raise KeyError(payana_empty_row_read_exception,
                           payana_gcs_object_name_space)

        return payana_metadata_obj.metadata, payana_200
    
    @payana_gcs_object_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_gcs_object_header_missing_exception, payana_gcs_object_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_gcs_bucket_header_missing_exception, payana_gcs_object_name_space)
            
        gcs_metadata = request.json

        if gcs_metadata is None or len(gcs_metadata) == 0:
            raise KeyError(
                payana_gcs_metadata_header_missing_exception, payana_gcs_object_name_space)

        payana_metadata_gcs_read_obj = PayanaGCSObjectMetadata(gcs_bucket_id, gcs_object_id, gcs_metadata)

        payana_metadata_gcs_read_obj.set_metadata()

        return {
            status: payana_201_response,
            message: payana_gcs_object_metadata_success_message_update,
            status_code: payana_201
        }, payana_201
    
@payana_gcs_object_name_space.route("/")
class PayanaGCSObjectDeleteURLEndPoint(Resource):

    @payana_gcs_object_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_gcs_object_header_missing_exception, payana_gcs_object_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_gcs_bucket_header_missing_exception, payana_gcs_object_name_space)

        payana_metadata_gcs_read_obj = PayanaGCSObjectMetadata(gcs_bucket_id, gcs_object_id)

        payana_metadata_gcs_read_obj.delete_gcs_object()

        return {
            status: payana_200_response,
            message: payana_gcs_object_success_message_delete,
            status_code: payana_200
        }, payana_200
    
@payana_gcs_object_name_space.route("/cors/")
class PayanaGCSObjectCORSURLEndPoint(Resource):

    @payana_gcs_object_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_gcs_bucket_header_missing_exception, payana_gcs_object_name_space)
            
        gcs_metadata_cors = request.json

        if gcs_metadata_cors is None:
            raise KeyError(
                payana_gcs_cors_metadata_missing_exception, payana_gcs_object_name_space)

        payana_metadata_gcs_read_obj = PayanaGCSObjectMetadata(payana_bucket_name=gcs_bucket_id, cors_policy=gcs_metadata_cors)

        payana_metadata_gcs_read_obj.set_object_cors_policy()

        return {
            status: payana_201_response,
            message: payana_gcs_object_cors_policy_success_message_update,
            status_code: payana_201
        }, payana_201

    @payana_gcs_object_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_gcs_bucket_header_missing_exception, payana_gcs_object_name_space)

        payana_metadata_gcs_read_obj = PayanaGCSObjectMetadata(gcs_bucket_id)

        payana_metadata_cors_policy = payana_metadata_gcs_read_obj.get_object_cors_policy()

        return {
            status: payana_200_response,
            payana_gcs_cors_header: payana_metadata_cors_policy,
            message: payana_gcs_object_metadata_success_message_get,
            status_code: payana_200
        }, payana_200
