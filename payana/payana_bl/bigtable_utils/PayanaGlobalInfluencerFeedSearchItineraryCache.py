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


class PayanaGlobalInfluencerFeedSearchItineraryCache:

    @payana_generic_exception_handler
    def __init__(self, profile_id, excursion_id,
                 activities, category):

        self.profile_id = profile_id
        self.excursion_id = excursion_id
        self.activities = activities
        self.category = category
        self.row_id = None

        self.update_bigtable_write_objects = []

        self.payana_feed_search_itinerary_cache_excursion_id_column_family = bigtable_constants.payana_feed_search_itinerary_cache_excursion_id_column_family
        self.payana_feed_search_itinerary_cache_rating_column_family = bigtable_constants.payana_feed_search_itinerary_cache_rating_column_family
        self.payana_feed_search_itinerary_cache_timestamp_column_family = bigtable_constants.payana_feed_search_itinerary_cache_timestamp_column_family

        self.current_year = str(datetime.now().year)

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_row_id(self):

        self.row_id = self.profile_id

    @payana_generic_exception_handler
    def update_feed_search_itinerary_bigtable(self):

        if self.row_id is None:
            self.generate_row_id()

        payana_feed_search_itinerary_cache_instance = PayanaBigTable(
            bigtable_constants.payana_global_influencer_feed_search_itinerary_cache_table)

        self.create_bigtable_write_objects()

        return payana_feed_search_itinerary_cache_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_activities_write_object()

    @payana_generic_exception_handler
    def set_activities_write_object(self):

        # all activities write objects

        for activity in self.activities:
            if activity in bigtable_constants.payana_activity_column_family:
                for category in self.category:
                    if category in [self.payana_feed_search_itinerary_cache_rating_column_family, self.payana_feed_search_itinerary_cache_timestamp_column_family]:

                        excursion_activity_column_family_id = "_".join(
                            [activity, category, self.payana_feed_search_itinerary_cache_excursion_id_column_family])

                        for city, excursion_id_list in self.excursion_id.items():
                            # excursion id write object
                            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                                self.row_id, excursion_activity_column_family_id, city, "##".join(excursion_id_list)))

            else:
                # to-do : raise exception that it is an invalid activity
                print("Invalid activity")
                pass
