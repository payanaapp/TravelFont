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


class PayanaUsersAutocompleteTable:

    @payana_generic_exception_handler
    def __init__(self, city, payana_autocomplete_users_list):

        self.city = city
        self.payana_users_list = payana_autocomplete_users_list

        self.payana_users_autocomplete_column_family = bigtable_constants.payana_users_autocomplete_column_family

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def update_autocomplete_users_list_bigtable(self):

        payana_autocomplete_users_list_table_instance = PayanaBigTable(
            bigtable_constants.payana_users_autocomplete_table)

        self.create_bigtable_write_objects()

        return payana_autocomplete_users_list_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_autocomplete_city_list_write_object()

    @payana_generic_exception_handler
    def set_autocomplete_city_list_write_object(self):

        for user, rating in self.payana_users_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.city, self.payana_users_autocomplete_column_family, user, rating))
