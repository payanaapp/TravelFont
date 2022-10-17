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
from payana.payana_bl.bigtable_utils.PayanaEntityToCommentsTable import PayanaEntityToCommentsTable
from payana.payana_bl.common_utils.payana_bl_generic_utils import payana_generate_id

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaCommentsTable:

    @payana_generic_exception_handler
    def __init__(self, comment_timestamp, profile_id, profile_name, comment, likes_count, comment_id, entity_id):

        self.comment_timestamp = comment_timestamp
        self.profile_id = profile_id
        self.profile_name = profile_name
        self.comment = comment
        self.likes_count = likes_count
        self.comment_id = comment_id
        self.entity_id = entity_id

        self.column_family_id = bigtable_constants.payana_comments_table_comments_family_id
        self.update_bigtable_write_objects = []
        self.comment_json_obj = {}

    @payana_generic_exception_handler
    def generate_comment_id(self):

        comment_id_terms = [self.profile_name, self.entity_id]
        self.comment_id = payana_generate_id(comment_id_terms)

    @payana_generic_exception_handler
    def update_comment_bigtable(self):

        if self.comment_id is None or self.comment_id == "":
            self.generate_comment_id()

        # Update comments table
        payana_comments_table_instance = PayanaBigTable(
            bigtable_constants.payana_comments_table)

        self.create_bigtable_write_objects()

        return payana_comments_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_comment_timestamp_write_object()
        self.set_profile_id_write_object()
        self.set_profile_name_write_object()
        self.set_comment_write_object()
        self.set_likes_count_write_object()
        self.set_comment_id_write_object()
        self.set_entity_id_write_object()

    @payana_generic_exception_handler
    def set_comment_timestamp_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_timestamp, self.comment_timestamp))

    @payana_generic_exception_handler
    def set_profile_id_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_profile_id, self.profile_id))

    @payana_generic_exception_handler
    def set_profile_name_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_profile_name, self.profile_name))

    @payana_generic_exception_handler
    def set_comment_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_comment, self.comment))

    @payana_generic_exception_handler
    def set_likes_count_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_likes_count, self.likes_count))

    @payana_generic_exception_handler
    def set_comment_id_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_comment_id, self.comment_id))

    @payana_generic_exception_handler
    def set_entity_id_write_object(self):

        # payana comments write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.comment_id, self.column_family_id, bigtable_constants.payana_comments_table_entity_id, self.entity_id))
