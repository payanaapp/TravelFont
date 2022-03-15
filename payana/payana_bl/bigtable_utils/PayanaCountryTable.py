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


class PayanaCountryTable:

    @payana_generic_exception_handler
    def __init__(self, country, city_list):

        self.country = country
        self.city_list = city_list

        self.update_bigtable_write_objects = []

        self.column_family_id = bigtable_constants.payana_country_table_column_family_city_list

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_country_bigtable(self):

        payana_country_table_instance = PayanaBigTable(
            bigtable_constants.payana_place_country_table)

        self.create_bigtable_write_objects()

        payana_country_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_city_write_object()

    @payana_generic_exception_handler
    def set_city_write_object(self):
        
        # city list write object
        for city, score in self.city_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.country, self.column_family_id, city, score))
