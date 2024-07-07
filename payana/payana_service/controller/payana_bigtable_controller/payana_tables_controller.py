from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields, Namespace, reqparse
import json
import threading

from payana.payana_service.constants import payana_service_constants
from payana.payana_service.common_utils.payana_service_exception_handlers import payana_service_generic_exception_handler
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_init import payana_cloud_storage_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_cleanup import payana_cloud_storage_cleanup

payana_tables_name_space = Namespace(
    'tables', description='Manage tables for all entitities')

payana_tables_create_success_message = "Payana tables successfully created!"
payana_tables_create_failure_message = "Payana tables failed to create!"
payana_tables_delete_success_message = "Payana tables  successfully deleted!"
payana_tables_delete_failure_message = "Failed to delete the Payana tables"

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file
gcs_client_config_path = bigtable_constants.gcs_client_config_path

@payana_tables_name_space.route("/")
class PayanaTablesEndPoint(Resource):

    @payana_tables_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        payana_thread_bigtable = threading.Thread(target=payana_bigtable_init, args=(client_config_file_path, bigtable_tables_schema_path))
        payana_thread_bigtable.start()
        # payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)
        
        # payana_thread_gcs = threading.Thread(target=payana_cloud_storage_init, args=(gcs_client_config_path))
        # payana_thread_gcs.start()
        payana_cloud_storage_init(gcs_client_config_path)

        return {
            status: payana_201_response,
            message: payana_tables_create_success_message,
            status_code: payana_201
        }, payana_201


@payana_tables_name_space.route("/")
class PayanaLikesRowDeleteEndPoint(Resource):
    @payana_tables_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def delete(self):

        # payana_thread = threading.Thread(target=payana_bigtable_cleanup, args=(client_config_file_path, bigtable_tables_schema_path))
        # payana_thread.start()
        payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
        payana_cloud_storage_cleanup(gcs_client_config_path)

        return {
            status: payana_200_response,
            message: payana_tables_delete_success_message,
            status_code: payana_200
        }, payana_200
        