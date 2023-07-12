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
from payana.payana_bl.gmail_utils.PayanaSignUpMailNotificationTable import PayanaSignUpMailNotificationTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

payana_mail_id_sign_up_notification_name_space = Namespace(
    'signup', description='Manage mail ID sign up notifications')

payana_mail_id_sign_up_notification_write_success_message_post = payana_service_constants.payana_mail_id_sign_up_notification_write_success_message_post
payana_mail_id_sign_up_notification_write_failure_message_post = payana_service_constants.payana_mail_id_sign_up_notification_write_failure_message_post

status = payana_service_constants.status
message = payana_service_constants.message
status_code = payana_service_constants.status_code
payana_empty_row_read_exception = payana_service_constants.payana_empty_row_read_exception

payana_mail_id_sign_up_notification_profile_id_header = payana_service_constants.payana_mail_id_sign_up_notification_profile_id_header

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

payana_missing_mail_id_sign_up_notification_header_exception = payana_service_constants.payana_missing_mail_id_sign_up_notification_header_exception
payana_mail_sign_up_notification_table = bigtable_constants.payana_mail_sign_up_notification_table


@payana_mail_id_sign_up_notification_name_space.route("/")
class PayanaMailSignupNotificationEndPoint(Resource):

    @payana_mail_id_sign_up_notification_name_space.doc(responses={200: payana_200_response, 400: payana_400_response, 500: payana_500_response})
    @payana_service_generic_exception_handler
    def post(self):

        profile_id = get_profile_id_header(request)

        if profile_id is None or len(profile_id) == 0:
            raise KeyError(
                payana_missing_mail_id_sign_up_notification_header_exception, payana_mail_id_sign_up_notification_name_space)
            
        profile_mail_id_sign_up_notification_read_obj = request.json

        payana_mail_id_sign_up_notification_object = PayanaSignUpMailNotificationTable(
            **profile_mail_id_sign_up_notification_read_obj)
        payana_mail_id_sign_up_notification_obj_write_status = payana_mail_id_sign_up_notification_object.update_mail_sign_up_notification_bigtable()

        if payana_mail_id_sign_up_notification_obj_write_status is None:
            raise Exception(
                payana_mail_id_sign_up_notification_write_failure_message_post, payana_mail_id_sign_up_notification_name_space)

        return {
            status: payana_201_response,
            payana_mail_id_sign_up_notification_profile_id_header: profile_id,
            message: payana_mail_id_sign_up_notification_write_success_message_post,
            status_code: payana_201
        }, payana_201
