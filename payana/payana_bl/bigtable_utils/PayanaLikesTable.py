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


class PayanaLikesTable:

    @payana_generic_exception_handler
    def __init__(self, payana_likes, entity_id):

        self.payana_likes = payana_likes
        self.entity_id = entity_id

        self.likes_column_family = bigtable_constants.payana_likes_table_column_family

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def update_likes_bigtable(self):

        payana_likes_table_instance = PayanaBigTable(
            bigtable_constants.payana_likes_table)

        self.create_bigtable_write_objects()

        return payana_likes_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_likes_list_write_object()

    @payana_generic_exception_handler
    def set_likes_list_write_object(self):

        # participants_list write object
        for participant, timestamp in self.payana_likes.items():
            print(timestamp)
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.entity_id, self.likes_column_family, participant, timestamp))
