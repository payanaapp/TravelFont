from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json

from payana.payana_service.server import service_settings
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_parsers import get_gcs_object_id_header, get_gcs_bucket_id_header, get_gcs_content_type_header
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_service.common_utils.payana_controller_objects_business_logic_helpers import payana_profile_page_travel_footprint_read_parser, payana_profile_page_travel_footprint_delete_parser
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_read_row_key_wrapper
from payana.payana_bl.cloud_storage_utils.PayanaSignedURL import PayanaSignedURL
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_signed_url_name_space = Namespace(
    'signed_url', description='Manage signed URL for GCS entitities')

payana_signed_url_success_message_get = payana_service_constants.payana_signed_url_success_message_get
payana_signed_url_storage_bucket_header = payana_service_constants.payana_signed_url_storage_bucket_header
payana_signed_url_storage_object_header = payana_service_constants.payana_signed_url_storage_object_header
payana_signed_url_storage_bucket_header_missing_exception = payana_service_constants.payana_signed_url_storage_bucket_header_missing_exception
payana_signed_url_storage_object_header_missing_exception  = payana_service_constants.payana_signed_url_storage_object_header_missing_exception
payana_signed_url_content_type_header_missing_exception = payana_service_constants.payana_signed_url_content_type_header_missing_exception

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


@payana_signed_url_name_space.route("/upload/")
class PayanaSignedUploadURLEndPoint(Resource):

    @payana_signed_url_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_signed_url_storage_object_header_missing_exception, payana_signed_url_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_signed_url_storage_bucket_header_missing_exception, payana_signed_url_name_space)
            
        content_type = get_gcs_content_type_header(request)

        if content_type is None or len(content_type) == 0:
            raise KeyError(
                payana_signed_url_content_type_header_missing_exception, payana_signed_url_name_space)
            
        payana_signed_url_read_obj = PayanaSignedURL(gcs_bucket_id, gcs_object_id, content_type)

        payana_signed_url = payana_signed_url_read_obj.get_signed_upload_url()

        if len(payana_signed_url) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_signed_url_name_space)

        return payana_signed_url, payana_200
    

@payana_signed_url_name_space.route("/download/")
class PayanaSignedDownloadURLEndPoint(Resource):

    @payana_signed_url_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_signed_url_storage_object_header_missing_exception, payana_signed_url_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_signed_url_storage_bucket_header_missing_exception, payana_signed_url_name_space)

        payana_signed_url_read_obj = PayanaSignedURL(gcs_bucket_id, gcs_object_id)

        payana_signed_url = payana_signed_url_read_obj.get_signed_download_url()

        if len(payana_signed_url) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_signed_url_name_space)

        return payana_signed_url, payana_200
    

@payana_signed_url_name_space.route("/upload/resumable/")
class PayanaSignedResumableURLUploadEndPoint(Resource):

    @payana_signed_url_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def get(self):

        gcs_object_id = get_gcs_object_id_header(request)

        if gcs_object_id is None or len(gcs_object_id) == 0:
            raise KeyError(
                payana_signed_url_storage_object_header_missing_exception, payana_signed_url_name_space)
            
        gcs_bucket_id = get_gcs_bucket_id_header(request)

        if gcs_bucket_id is None or len(gcs_bucket_id) == 0:
            raise KeyError(
                payana_signed_url_storage_bucket_header_missing_exception, payana_signed_url_name_space)

        payana_signed_url_read_obj = PayanaSignedURL(gcs_bucket_id, gcs_object_id)

        payana_signed_url = payana_signed_url_read_obj.get_signed_resumable_upload_url()

        if len(payana_signed_url) == 0:
            raise KeyError(payana_empty_row_read_exception,
                           payana_signed_url_name_space)

        return payana_signed_url, payana_200
    
