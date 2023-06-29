#!/usr/bin/env python

"""Demonstrates how to write comments into BigTable
"""

import argparse
import random
import json
import time
import hashlib
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler


# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaSignUpMailNotificationTable:

    @payana_generic_exception_handler
    def __init__(self, profile_id, sign_up_mail_id_list):

        self.profile_id = profile_id
        self.sign_up_mail_id_list = sign_up_mail_id_list

        self.payana_sign_up_mail_id_list_column_family = bigtable_constants.payana_sign_up_mail_id_list_column_family

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def update_mail_sign_up_notification_bigtable(self):

        payana_mail_sign_up_notification_table_instance = PayanaBigTable(
            bigtable_constants.payana_mail_sign_up_notification_table)

        self.create_bigtable_write_objects()

        return payana_mail_sign_up_notification_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_mail_sign_up_notification_write_object()

    @payana_generic_exception_handler
    def set_mail_sign_up_notification_write_object(self):

        for mail_id, timestamp in self.sign_up_mail_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_sign_up_mail_id_list_column_family, mail_id, timestamp))
