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


class PayanaEntityToCommentsTable:

    @payana_generic_exception_handler
    def __init__(self, entity_id, payana_comment_id_list):

        self.comment_id_list = payana_comment_id_list
        self.entity_id = entity_id

        self.column_family_id = bigtable_constants.payana_entity_to_comments_table_comment_id_list
        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def update_entity_to_comments_bigtable(self):

        payana_entity_to_comments_table_instance = PayanaBigTable(
            bigtable_constants.payana_entity_to_comments_table)

        self.create_bigtable_write_objects()

        return payana_entity_to_comments_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_comment_id_list_write_object()

    @payana_generic_exception_handler
    def set_comment_id_list_write_object(self):

        # payana comments write object
        for comment_id, timestamp in self.comment_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.entity_id, self.column_family_id, comment_id, timestamp))
