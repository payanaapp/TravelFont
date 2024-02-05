#!/usr/bin/env python

"""Demonstrates how to write ProfileInfo into BigTable
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
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaAuthProfileTable:

    @payana_generic_exception_handler
    def __init__(self, auth_information):

        self.auth_information = auth_information

        if bigtable_constants.payana_auth_mail_id in self.auth_information:
            self.mail_id = self.auth_information[bigtable_constants.payana_auth_mail_id]
        else:
            pass

        if bigtable_constants.payana_auth_profile_name in self.auth_information:
            self.profile_name = self.auth_information[bigtable_constants.payana_auth_profile_name]
        else:
            pass
        
        if bigtable_constants.payana_auth_profile_picture_id in self.auth_information:
                self.profile_picture_id = self.auth_information[bigtable_constants.payana_auth_profile_picture_id]
        else:
            pass

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_auth_profile_info_bigtable(self):

        payana_auth_profile_table_instance = PayanaBigTable(
            bigtable_constants.payana_profile_auth_table)

        self.create_bigtable_write_objects()

        return payana_auth_profile_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_profile_name_write_object()
        self.set_prpfile_picture_id_write_object()

    @payana_generic_exception_handler
    def set_profile_name_write_object(self):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.mail_id, bigtable_constants.payana_auth_information, bigtable_constants.payana_auth_profile_name, self.profile_name))
        
    @payana_generic_exception_handler
    def set_prpfile_picture_id_write_object(self):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.mail_id, bigtable_constants.payana_auth_information, bigtable_constants.payana_auth_profile_picture_id, self.profile_picture_id))
