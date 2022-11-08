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
    def __init__(self, profile_id, travel_buddy_profile_id, global_influencer=False, favorite=False, sent_pending_request=False, received_pending_request=False, new_friend_request=False):

        self.profile_id = profile_id
        self.travel_buddy_profile_id = travel_buddy_profile_id
        self.global_influencer = global_influencer
        self.update_bigtable_write_objects = []
        self.favorite = favorite
        self.sent_pending_request = sent_pending_request
        self.received_pending_request = received_pending_request
        self.new_friend_request = new_friend_request

        self.payana_travel_buddy_table_column_family_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_travel_buddy_list
        self.payana_travel_buddy_table_column_family_favorite_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_favorite_travel_buddy_list
        self.payana_travel_buddy_table_column_family_top_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_top_travel_buddy_list
        self.payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list
        self.payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list
        self.payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_travel_buddy_bigtable(self):

        payana_travel_buddy_instance = PayanaBigTable(
            bigtable_constants.payana_travel_buddy_list_table)

        self.create_bigtable_write_objects()

        return payana_travel_buddy_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        current_timestamp_unix = str(time.time())

        if self.new_friend_request:
            self.set_profile_id_write_object(current_timestamp_unix)
            self.set_travel_buddy_profile_id_write_object(
                current_timestamp_unix)

        if self.global_influencer:
            self.set_global_influencer_profile_id_write_object(
                current_timestamp_unix)

        if self.favorite:
            self.set_favorite_travel_buddy_write_object(current_timestamp_unix)

        if self.sent_pending_request:
            self.set_sent_pending_requests_travel_buddy_write_object(
                current_timestamp_unix)

        if self.received_pending_request:
            self.set_received_pending_requests_travel_buddy_write_object(
                current_timestamp_unix)

    @payana_generic_exception_handler
    def set_profile_id_write_object(self, current_timestamp_unix):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.payana_travel_buddy_table_column_family_travel_buddy_list, self.travel_buddy_profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_favorite_travel_buddy_write_object(self, current_timestamp_unix):

        # favorite buddy write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.payana_travel_buddy_table_column_family_favorite_travel_buddy_list, self.travel_buddy_profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_top_travel_buddy_write_object(self, current_timestamp_unix):

        # top buddy write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.payana_travel_buddy_table_column_family_top_travel_buddy_list, self.travel_buddy_profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_sent_pending_requests_travel_buddy_write_object(self, current_timestamp_unix):

        # sent pending requests write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list, self.travel_buddy_profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_received_pending_requests_travel_buddy_write_object(self, current_timestamp_unix):

        # received pending requests write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.travel_buddy_profile_id, self.payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list, self.profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_travel_buddy_profile_id_write_object(self, current_timestamp_unix):

        # travel buddy write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.travel_buddy_profile_id, self.payana_travel_buddy_table_column_family_travel_buddy_list, self.profile_id, current_timestamp_unix))

    @payana_generic_exception_handler
    def set_global_influencer_profile_id_write_object(self, current_timestamp_unix):

        # global_influencer write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list, self.travel_buddy_profile_id, current_timestamp_unix))
