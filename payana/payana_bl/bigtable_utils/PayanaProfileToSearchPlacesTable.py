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


class PayanaProfileToSearchPlacesTable:

    @payana_generic_exception_handler
    def __init__(self, profile_id, searched_cities_activities, searched_state_activities, searched_place_id_activities, searched_country_activities):

        self.profile_id = profile_id
        self.searched_cities_activities = searched_cities_activities
        self.searched_state_activities = searched_state_activities
        self.searched_place_id_activities = searched_place_id_activities
        self.searched_country_activities = searched_country_activities

        self.update_bigtable_write_objects = []
        
        self.payana_profile_to_search_places_activities_searched_cities_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_cities_activities
        self.payana_profile_to_search_places_activities_searched_state_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_state_activities
        self.payana_profile_to_search_places_activities_searched_place_id_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_place_id_activities
        self.payana_profile_to_search_places_activities_searched_country_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_country_activities

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_profile_search_places_bigtable(self):

        payana_profile_to_search_cities_activities_table_instance = PayanaBigTable(
            bigtable_constants.payana_profile_to_search_places_activities_table)

        self.create_bigtable_write_objects()

        return payana_profile_to_search_cities_activities_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_searched_cities_activities_write_object()
        self.set_searched_state_activities_write_object()
        self.set_searched_country_activities_write_object()
        self.set_searched_place_id_activities_write_object()

    @payana_generic_exception_handler
    def set_searched_cities_activities_write_object(self):

        # profile_name write object
        for city, timestamp in self.searched_cities_activities.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_profile_to_search_places_activities_searched_cities_activities, city, timestamp))

    @payana_generic_exception_handler
    def set_searched_state_activities_write_object(self):

        # profile_name write object
        for state, timestamp in self.searched_state_activities.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_profile_to_search_places_activities_searched_state_activities, state, timestamp))

    @payana_generic_exception_handler
    def set_searched_country_activities_write_object(self):

        # profile_name write object
        for country, timestamp in self.searched_country_activities.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_profile_to_search_places_activities_searched_country_activities, country, timestamp))

    @payana_generic_exception_handler
    def set_searched_place_id_activities_write_object(self):

        # profile_name write object
        for place_id, timestamp in self.searched_place_id_activities.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.payana_profile_to_search_places_activities_searched_place_id_activities, place_id, timestamp))
