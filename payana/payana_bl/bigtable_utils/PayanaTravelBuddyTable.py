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


# google cloud bigtable imports
from google.cloud.bigtable import column_family

class PayanaTravelBuddyTable:

    @payana_generic_exception_handler
    def __init__(self, profile_id, friend_profile_id):

        self.profile_id = profile_id
        self.friend_profile_id = friend_profile_id
        self.update_bigtable_write_objects = []
        self.travel_buddy_list_column_family_id = bigtable_constants.payana_travel_buddy_table_column_family

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_travel_buddy_bigtable(self):

        payana_travel_buddy_instance = PayanaBigTable(
            bigtable_constants.payana_travel_buddy_list_table)

        self.create_bigtable_write_objects()

        payana_travel_buddy_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        current_timestamp_unix = str(time.time())
        self.set_profile_id_write_object(current_timestamp_unix)
        self.set_friend_profile_id_write_object(current_timestamp_unix)

    @payana_generic_exception_handler
    def set_profile_id_write_object(self, current_timestamp_unix):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.travel_buddy_list_column_family_id, self.friend_profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_friend_profile_id_write_object(self, current_timestamp_unix):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.friend_profile_id, self.travel_buddy_list_column_family_id, self.profile_id, current_timestamp_unix))
