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


class PayanaProfileTravelFootPrintTable:

    @payana_generic_exception_handler
    def __init__(self, profile_id, travelfont_obj_list):

        self.payana_profile_page_travel_footprint_profile_id = bigtable_constants.payana_profile_page_travel_footprint_profile_id
        self.payana_profile_page_travel_footprint_place_id = bigtable_constants.payana_profile_page_travel_footprint_place_id
        self.payana_profile_page_travel_footprint_excursion_id = bigtable_constants.payana_profile_page_travel_footprint_excursion_id
        self.payana_profile_page_travel_footprint_latitude = bigtable_constants.payana_profile_page_travel_footprint_latitude
        self.payana_profile_page_travel_footprint_longitude = bigtable_constants.payana_profile_page_travel_footprint_longitude
        self.payana_profile_page_travel_footprint_column_family = bigtable_constants.payana_profile_page_travel_footprint_column_family

        self.payana_profile_page_travel_footprint_column_qualifier = ""

        self.payana_profile_page_travel_footprint_column_value = ""

        self.profile_id = profile_id
        self.travelfont_obj_list = travelfont_obj_list

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_profile_travel_footprint_bigtable(self):

        payana_profile_table_instance = PayanaBigTable(
            bigtable_constants.payana_profile_travel_footprint_table)
        
        self.create_bigtable_write_objects()

        return payana_profile_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_profile_travel_footprint_write_object()

    @payana_generic_exception_handler
    def set_profile_travel_footprint_write_object(self):
        
        for travelfont_obj in self.travelfont_obj_list:
            
            place_id = travelfont_obj[self.payana_profile_page_travel_footprint_place_id]
            excursion_id = travelfont_obj[self.payana_profile_page_travel_footprint_excursion_id]
            latitude = travelfont_obj[self.payana_profile_page_travel_footprint_latitude]
            longitude = travelfont_obj[self.payana_profile_page_travel_footprint_longitude]
            
            payana_profile_page_travel_footprint_column_qualifier = "##".join(
                [str(place_id), str(excursion_id)])

            payana_profile_page_travel_footprint_column_value = "##".join(
                [str(latitude), str(longitude)])
            
            # profile_name write object
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_profile_page_travel_footprint_column_family, payana_profile_page_travel_footprint_column_qualifier, payana_profile_page_travel_footprint_column_value))
