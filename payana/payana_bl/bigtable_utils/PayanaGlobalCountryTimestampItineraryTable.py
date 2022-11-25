#!/usr/bin/env python

"""Demonstrates how to write ProfileInfo into BigTable
"""

import argparse
import random
import json
import time
import hashlib
from datetime import datetime
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler


# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaGlobalCountryTimestampItineraryTable:

    @payana_generic_exception_handler
    def __init__(self, country, activity_guide_id,
                 itinerary_id, excursion_id, checkin_id,
                 activities):

        self.country = country
        self.itinerary_id = itinerary_id
        self.excursion_id = excursion_id
        self.checkin_id = checkin_id
        self.activities = activities
        self.row_id = None
        self.activity_guide_id = activity_guide_id

        self.update_bigtable_write_objects = []

        self.activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family
        self.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value = bigtable_constants.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value

        self.current_year = str(datetime.now().year)

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_row_id(self):

        self.row_id = self.country + "##" + self.current_year

    @payana_generic_exception_handler
    def update_global_country_itinerary_bigtable(self):

        if self.row_id is None:
            self.generate_row_id()

        payana_global_country_itinerary_instance = PayanaBigTable(
            bigtable_constants.payana_global_country_itinerary_table)

        self.create_bigtable_write_objects()

        return payana_global_country_itinerary_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_activities_write_object()

    @payana_generic_exception_handler
    def set_activities_write_object(self):

        # all activities write objects

        for activity in self.activities:
            if activity in bigtable_constants.payana_activity_column_family:

                itinerary_activity_column_family_id = "_".join(
                    [activity, self.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

                excursion_activity_column_family_id = "_".join(
                    [activity, self.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

                checkin_activity_column_family_id = "_".join(
                    [activity, self.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])
                
                activity_guide_activity_column_family_id = "_".join(
                    [activity, self.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_activity_guide_id_quantifier_value])

                for timestamp, itinerary in self.itinerary_id.items():
                    # itinerary id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, itinerary_activity_column_family_id, timestamp, itinerary))

                for timestamp, excursion in self.excursion_id.items():
                    # excursion id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, excursion_activity_column_family_id, timestamp, excursion))

                for timestamp, checkin in self.checkin_id.items():
                    # checkin id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, checkin_activity_column_family_id, timestamp, checkin))
                    
                for timestamp, activity_guide in self.activity_guide_id.items():
                    # checkin id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, activity_guide_activity_column_family_id, timestamp, activity_guide))

            else:
                # to-do : raise exception that it is an invalid activity
                print("Invalid activity")
                pass
