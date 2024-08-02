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
from payana.payana_bl.common_utils.payana_bl_generic_utils import payana_generate_id

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaExcursionTable:

    @payana_generic_exception_handler
    def __init__(self, checkin_id_list, image_id_list, participants_list, activities_list, excursion_metadata, cities_checkin_id_list):

        self.checkin_id_list = checkin_id_list
        self.image_id_list = image_id_list
        self.participants_list = participants_list
        self.excursion_metadata = excursion_metadata
        self.activities_list = activities_list
        self.cities_checkin_id_list = cities_checkin_id_list

        self.column_family_checkin_id_list = bigtable_constants.payana_excursion_column_family_checkin_id_list
        self.payana_excursion_column_family_cities_checkin_id_list = bigtable_constants.payana_excursion_column_family_cities_checkin_id_list
        self.column_family_image_id_list = bigtable_constants.payana_excursion_column_family_image_id_list
        self.column_family_participants_list = bigtable_constants.payana_excursion_column_family_participants_list
        self.column_qualifier_description = bigtable_constants.payana_excursion_column_family_description
        self.column_qualifier_create_timestamp = bigtable_constants.payana_excursion_column_family_create_timestamp
        self.column_qualifier_last_updated_timestamp = bigtable_constants.payana_excursion_column_family_last_updated_timestamp
        self.column_qualifier_excursion_owner_profile_id = bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id
        self.column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
        self.column_qualifier_excursion_place_id = bigtable_constants.payana_excursion_place_id
        self.column_qualifier_excursion_transport_mode = bigtable_constants.payana_excursion_transport_mode
        self.column_qualifier_excursion_place_name = bigtable_constants.payana_excursion_place_name
        self.column_qualifier_excursion_city = bigtable_constants.payana_excursion_city
        self.column_qualifier_excursion_state = bigtable_constants.payana_excursion_state
        self.column_qualifier_excursion_country = bigtable_constants.payana_excursion_country
        self.column_qualifier_excursion_activity_guide = bigtable_constants.payana_excursion_activity_guide
        self.payana_excursion_itinerary_position = bigtable_constants.payana_excursion_itinerary_position

        self.column_qualifier_itinerary_id = bigtable_constants.payana_excursion_itinerary_id
        self.column_qualifier_itinerary_name = bigtable_constants.payana_excursion_itinerary_name
        self.column_family_activities_list = bigtable_constants.payana_excursion_activities_list

        self.column_qualifier_excursion_id = bigtable_constants.payana_excursion_id

        if self.column_qualifier_description in self.excursion_metadata:
            self.description = self.excursion_metadata[self.column_qualifier_description]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_id in self.excursion_metadata:
            self.excursion_id = self.excursion_metadata[self.column_qualifier_excursion_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_create_timestamp in self.excursion_metadata:
            self.create_timestamp = self.excursion_metadata[self.column_qualifier_create_timestamp]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_activity_guide in self.excursion_metadata:
            self.activity_guide = self.excursion_metadata[self.column_qualifier_excursion_activity_guide]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_last_updated_timestamp in self.excursion_metadata:
            self.last_updated_timestamp = self.excursion_metadata[
                self.column_qualifier_last_updated_timestamp]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_owner_profile_id in self.excursion_metadata:
            self.excursion_owner_profile_id = self.excursion_metadata[
                self.column_qualifier_excursion_owner_profile_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_transport_mode in self.excursion_metadata:
            self.excursion_transport_mode = self.excursion_metadata[
                self.column_qualifier_excursion_transport_mode]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_place_name in self.excursion_metadata:
            self.excursion_place_name = self.excursion_metadata[
                self.column_qualifier_excursion_place_name]
        else:
            # raise invalid key error or key missing error
            pass

        if self.payana_excursion_itinerary_position in self.excursion_metadata:
            self.excursion_itinerary_position = self.excursion_metadata[
                self.payana_excursion_itinerary_position]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_city in self.excursion_metadata:
            self.excursion_city = self.excursion_metadata[
                self.column_qualifier_excursion_city]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_state in self.excursion_metadata:
            self.excursion_state = self.excursion_metadata[
                self.column_qualifier_excursion_state]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_country in self.excursion_metadata:
            self.excursion_country = self.excursion_metadata[
                self.column_qualifier_excursion_country]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_place_id in self.excursion_metadata:
            self.excursion_place_id = self.excursion_metadata[
                self.column_qualifier_excursion_place_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_id in self.excursion_metadata:
            self.excursion_itinerary_id = self.excursion_metadata[
                self.column_qualifier_itinerary_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_name in self.excursion_metadata:
            self.excursion_itinerary_name = self.excursion_metadata[
                self.column_qualifier_itinerary_name]
        else:
            # raise invalid key error or key missing error
            pass

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_excursion_id(self):
        excursion_id_terms = [self.excursion_owner_profile_id]
        self.excursion_id = payana_generate_id(excursion_id_terms)

    @payana_generic_exception_handler
    def update_excursion_bigtable(self):

        if self.excursion_id is None or self.excursion_id == "":
            self.generate_excursion_id()

        payana_excursion_table_instance = PayanaBigTable(
            bigtable_constants.payana_excursion_table)

        self.create_bigtable_write_objects()

        return payana_excursion_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_checkin_id_list_write_object()
        self.set_image_id_list_write_object()
        self.set_participants_list_write_object()
        self.set_activities_list_write_object()
        self.set_description_write_object()
        self.set_create_timestamp_write_object()
        self.set_last_updated_timestamp_write_object()
        self.set_excursion_owner_profile_id_write_object()
        self.set_excursion_place_name_write_object()
        self.set_excursion_city_write_object()
        self.set_excursion_state_write_object()
        self.set_excursion_country_write_object()
        self.set_excursion_id_write_object()
        self.set_excursion_transport_mode_write_object()
        self.set_excursion_place_id_write_object()
        self.set_excursion_itinerary_id_write_object()
        self.set_excursion_itinerary_name_write_object()
        self.set_activity_guide_status_write_object()
        self.set_checkin_id_cities_list_write_object()
        self.set_excursion_itinerary_position_write_object()

    @payana_generic_exception_handler
    def set_checkin_id_list_write_object(self):

        # excursion_id_list write object
        for key, checkin_id in self.checkin_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.column_family_checkin_id_list, key, checkin_id))

    @payana_generic_exception_handler
    def set_checkin_id_cities_list_write_object(self):

        # excursion_id_list write object
        for key, city in self.checkin_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.payana_excursion_column_family_cities_checkin_id_list, key, city))

    @payana_generic_exception_handler
    def set_image_id_list_write_object(self):

        # excursion_id_list write object
        for key, image_id in self.image_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.column_family_image_id_list, key, image_id))

    @payana_generic_exception_handler
    def set_participants_list_write_object(self):

        # participants_list write object
        for participant, timestamp in self.participants_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.excursion_id, self.column_family_participants_list, participant, timestamp))

    @payana_generic_exception_handler
    def set_activities_list_write_object(self):

        # participants_list write object
        for activity, number in self.activities_list.items():
            if activity in bigtable_constants.payana_activity_column_family:
                self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                    self.excursion_id, self.column_family_activities_list, activity, number))

    @payana_generic_exception_handler
    def set_description_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_description, self.description))

    @payana_generic_exception_handler
    def set_activity_guide_status_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_activity_guide, self.activity_guide))

    @payana_generic_exception_handler
    def set_create_timestamp_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_create_timestamp, self.create_timestamp))

    @payana_generic_exception_handler
    def set_last_updated_timestamp_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_last_updated_timestamp, self.last_updated_timestamp))

    @payana_generic_exception_handler
    def set_excursion_owner_profile_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_owner_profile_id, self.excursion_owner_profile_id))

    @payana_generic_exception_handler
    def set_excursion_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_id, self.excursion_id))

    @payana_generic_exception_handler
    def set_excursion_transport_mode_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_transport_mode, self.excursion_transport_mode))

    @payana_generic_exception_handler
    def set_excursion_place_name_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_place_name, self.excursion_place_name))

    @payana_generic_exception_handler
    def set_excursion_city_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_city, self.excursion_city))

    @payana_generic_exception_handler
    def set_excursion_state_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_state, self.excursion_state))

    @payana_generic_exception_handler
    def set_excursion_country_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_country, self.excursion_country))

    @payana_generic_exception_handler
    def set_excursion_place_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_excursion_place_id, self.excursion_place_id))

    @payana_generic_exception_handler
    def set_excursion_itinerary_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_itinerary_id, self.excursion_itinerary_id))

    @payana_generic_exception_handler
    def set_excursion_itinerary_name_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.column_qualifier_itinerary_name, self.excursion_itinerary_name))

    @payana_generic_exception_handler
    def set_excursion_itinerary_position_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.excursion_id, self.column_family_excursion_metadata, self.payana_excursion_itinerary_position, self.excursion_itinerary_position))
