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


class PayanaItineraryTable:

    @payana_generic_exception_handler
    def __init__(self, excursion_id_list, participants_list, activities_list, itinerary_metadata):

        self.excursion_id_list = excursion_id_list
        self.participants_list = participants_list
        self.activities_list = activities_list
        self.itinerary_metadata = itinerary_metadata

        self.column_family_excursion_id_list = bigtable_constants.payana_itinerary_column_family_excursion_id_list
        self.column_family_participants_list = bigtable_constants.payana_itinerary_column_family_participants_list
        self.column_qualifier_description = bigtable_constants.payana_itinerary_column_family_description
        self.column_qualifier_visit_timestamp = bigtable_constants.payana_itinerary_column_family_visit_timestamp
        self.column_qualifier_itinerary_owner_profile_id = bigtable_constants.payana_itinerary_column_family_itinerary_owner_profile_id
        self.column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
        self.column_qualifier_itinerary_id = bigtable_constants.payana_itinerary_id
        self.column_qualifier_itinerary_place_id = bigtable_constants.payana_itinerary_place_id
        self.column_qualifier_itinerary_place_name = bigtable_constants.payana_itinerary_place_name

        self.column_family_activities_list = bigtable_constants.payana_itinerary_activities_list

        if self.column_qualifier_description in self.itinerary_metadata:
            self.description = self.itinerary_metadata[self.column_qualifier_description]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_id in self.itinerary_metadata:
            self.itinerary_id = self.itinerary_metadata[self.column_qualifier_itinerary_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_visit_timestamp in self.itinerary_metadata:
            self.visit_timestamp = self.itinerary_metadata[self.column_qualifier_visit_timestamp]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_place_name in self.itinerary_metadata:
            self.itinerary_place_name = self.itinerary_metadata[
            self.column_qualifier_itinerary_place_name]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_place_id in self.itinerary_metadata:
            self.itinerary_place_id = self.itinerary_metadata[
                self.column_qualifier_itinerary_place_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_owner_profile_id in self.itinerary_metadata:
            self.itinerary_owner_profile_id = self.itinerary_metadata[
                self.column_qualifier_itinerary_owner_profile_id]
        else:
            # raise invalid key error or key missing error
            pass

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_itinerary_id(self):

        current_timestamp_unix = str(time.time())
        itinerary_id_terms = [current_timestamp_unix,
                              self.itinerary_owner_profile_id]

        rand_num = random.randint(0, 1)

        if rand_num == 1:
            itinerary_id_terms[0], itinerary_id_terms[1] = itinerary_id_terms[1], itinerary_id_terms[0]

        itinerary_id_hash = "".join(itinerary_id_terms)

        itinerary_id_binary = hashlib.sha256(itinerary_id_hash.encode())

        self.itinerary_id = itinerary_id_binary.hexdigest()

    @payana_generic_exception_handler
    def update_itinerary_bigtable(self):

        if self.itinerary_id is None or self.itinerary_id == "":
            self.generate_itinerary_id()

        payana_itinerary_table_instance = PayanaBigTable(
            bigtable_constants.payana_itinerary_table)

        self.create_bigtable_write_objects()

        payana_itinerary_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_excursion_id_list_write_object()
        self.set_participants_list_write_object()
        self.set_activities_list_write_object()
        self.set_description_write_object()
        self.set_visit_timestamp_write_object()
        self.set_itinerary_owner_profile_id_write_object()
        self.set_itinerary_id_write_object()
        self.set_itinerary_place_id_write_object()
        self.set_itinerary_place_name_write_object()

    @payana_generic_exception_handler
    def set_excursion_id_list_write_object(self):

        # excursion_id_list write object
        for key, excursion_id in self.excursion_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.itinerary_id, self.column_family_excursion_id_list, key, excursion_id))

    @payana_generic_exception_handler
    def set_participants_list_write_object(self):

        # participants_list write object
        for participant, timestamp in self.participants_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.itinerary_id, self.column_family_participants_list, participant, timestamp))

    @payana_generic_exception_handler
    def set_activities_list_write_object(self):

        # participants_list write object
        for activity, number in self.activities_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.itinerary_id, self.column_family_activities_list, activity, number))

    @payana_generic_exception_handler
    def set_description_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_description, self.description))

    @payana_generic_exception_handler
    def set_visit_timestamp_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_visit_timestamp, self.visit_timestamp))

    @payana_generic_exception_handler 
    def set_itinerary_place_name_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_itinerary_place_name, self.itinerary_place_name))

    @payana_generic_exception_handler
    def set_itinerary_place_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_itinerary_place_id, self.itinerary_place_id))

    @payana_generic_exception_handler
    def set_itinerary_owner_profile_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_itinerary_owner_profile_id, self.itinerary_owner_profile_id))

    @payana_generic_exception_handler
    def set_itinerary_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.itinerary_id, self.column_family_itinerary_metadata, self.column_qualifier_itinerary_id, self.itinerary_id))
