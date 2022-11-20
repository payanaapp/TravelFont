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
from payana.payana_bl.common_utils.payana_bl_generic_utils import payana_generate_id

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaExcursionCheckinPermissionTable:

    @payana_generic_exception_handler
    def __init__(self, excursion_id, participants_list, admin):

        self.excursion_id = excursion_id
        self.participants_list = participants_list
        self.admin = admin

        self.payana_excursion_checkin_permission_participants_column_family = bigtable_constants.payana_excursion_checkin_permission_participants_column_family
        self.payana_excursion_checkin_permission_table_admin_column_family = bigtable_constants.payana_excursion_checkin_permission_table_admin_column_family

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_excursion_bigtable(self):

        payana_excursion_checkin_permission_table_instance = PayanaBigTable(
            bigtable_constants.payana_excursion_checkin_permission_table)

        self.create_bigtable_write_objects()

        return payana_excursion_checkin_permission_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_admin_write_object()
        self.set_participants_list_write_object()

    @payana_generic_exception_handler
    def set_admin_write_object(self):

        # excursion_id_list write object
        for admin, timestamp in self.admin.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.payana_excursion_checkin_permission_table_admin_column_family, admin, timestamp))

    @payana_generic_exception_handler
    def set_participants_list_write_object(self):

        # participants_list write object
        for participant, timestamp in self.participants_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.payana_excursion_checkin_permission_participants_column_family, participant, timestamp))
