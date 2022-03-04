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

place_id_obj = {
    "place_id": "1234567",
    "city": "cupertino##california##usa",
    "state": "california##usa",
    "country": "usa",
    "zipcode": "95014"
}

class PayanaPlaceIdMetadataTable:

    @payana_generic_exception_handler
    def __init__(self, place_id, city,
                 state, country, zipcode):

        self.place_id = place_id
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

        self.update_bigtable_write_objects = []

        self.column_family_id = bigtable_constants.payana_column_family_place_metadata
        self.quantifier_place_id = bigtable_constants.payana_quantifier_place_id
        self.quantifier_city = bigtable_constants.payana_quantifier_city
        self.quantifier_state = bigtable_constants.payana_quantifier_state
        self.quantifier_country = bigtable_constants.payana_quantifier_country
        self.quantifier_zipcode = bigtable_constants.payana_quantifier_zipcode

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_place_metadata_bigtable(self):

        payana_place_metadata_table_instance = PayanaBigTable(
            bigtable_constants.payana_place_metadata_table)

        self.create_bigtable_write_objects()

        payana_place_metadata_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_place_id_write_object()
        self.set_city_write_object()
        self.set_country_write_object()
        self.set_zipcode_write_object()
        self.set_state_write_object()

    @payana_generic_exception_handler
    def set_place_id_write_object(self):

        # place_id write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.place_id, self.column_family_id, self.quantifier_place_id, self.place_id))

    @payana_generic_exception_handler
    def set_city_write_object(self):

        # city write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.place_id, self.column_family_id, self.quantifier_city, self.city))

    @payana_generic_exception_handler
    def set_country_write_object(self):

        # country write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.place_id, self.column_family_id, self.quantifier_country, self.country))

    @payana_generic_exception_handler
    def set_zipcode_write_object(self):

        # zipcode write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.place_id, self.column_family_id, self.quantifier_zipcode, self.zipcode))

    @payana_generic_exception_handler
    def set_state_write_object(self):

        # state write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.place_id, self.column_family_id, self.quantifier_state, self.state))
