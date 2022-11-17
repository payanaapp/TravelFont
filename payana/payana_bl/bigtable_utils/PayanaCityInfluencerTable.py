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


class PayanaCityInfluencerTable:

    @payana_generic_exception_handler
    def __init__(self, city, city_global_influencers, activities):

        self.city = city
        self.city_global_influencers = city_global_influencers
        self.activities = activities

        self.row_id = self.city

        self.update_bigtable_write_objects = []

        self.payana_city_to_influencers_table_global_influencers_column_family = bigtable_constants.payana_city_to_influencers_table_global_influencers_column_family

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_city_influencers_bigtable(self):

        payana_city_influencer_instance = PayanaBigTable(
            bigtable_constants.payana_city_to_influencers_table)

        self.create_bigtable_write_objects()

        return payana_city_influencer_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_city_influencers_write_object()

    @payana_generic_exception_handler
    def set_city_influencers_write_object(self):

        # all activities write objects

        for activity in self.activities:
            if activity in bigtable_constants.payana_activity_column_family:

                activity_city_influencer_column_family_id =  "_".join([activity, self.payana_city_to_influencers_table_global_influencers_column_family])

                for city_influencer, rating in self.city_global_influencers.items():
                    # itinerary id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, activity_city_influencer_column_family_id, city_influencer, rating))
            
            else:
                # to-do : raise exception that it is an invalid activity
                print("Invalid activity")
                pass
