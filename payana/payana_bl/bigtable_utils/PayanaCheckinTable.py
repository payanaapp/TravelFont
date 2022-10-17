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


class PayanaCheckinTable:

    @payana_generic_exception_handler
    def __init__(self, image_id_list, activities_list, participants_list, checkin_metadata, instagram_metadata, airbnb_metadata):

        self.image_id_list = image_id_list
        self.participants_list = participants_list
        self.activities_list = activities_list
        self.checkin_metadata = checkin_metadata
        self.instagram_metadata = instagram_metadata
        self.airbnb_metadata = airbnb_metadata

        self.column_family_image_id_list = bigtable_constants.payana_checkin_column_family_image_id_list
        self.column_family_participants_list = bigtable_constants.payana_checkin_column_family_participants_list
        self.column_qualifier_description = bigtable_constants.payana_checkin_column_family_description
        self.column_qualifier_create_timestamp = bigtable_constants.payana_checkin_column_family_create_timestamp
        self.column_qualifier_last_updated_timestamp = bigtable_constants.payana_checkin_column_family_last_updated_timestamp
        self.column_qualifier_checkin_owner_profile_id = bigtable_constants.payana_checkin_column_family_checkin_owner_profile_id
        self.column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata

        self.column_family_instagram_metadata = bigtable_constants.payana_checkin_instagram_metadata
        self.column_family_airbnb_metadata = bigtable_constants.payana_checkin_airbnb_metadata

        self.column_qualifier_itinerary_id = bigtable_constants.payana_checkin_itinerary_id
        self.column_qualifier_excursion_id = bigtable_constants.payana_checkin_excursion_id
        self.column_family_activities_list = bigtable_constants.payana_checkin_activities_list

        self.column_qualifier_checkin_place_id = bigtable_constants.payana_checkin_place_id
        self.column_qualifier_checkin_transport_mode = bigtable_constants.payana_checkin_transport_mode
        self.column_qualifier_checkin_place_name = bigtable_constants.payana_checkin_place_name

        self.column_qualifier_checkin_city = bigtable_constants.payana_checkin_city
        self.column_qualifier_checkin_country = bigtable_constants.payana_checkin_country
        self.column_qualifier_checkin_state = bigtable_constants.payana_checkin_state

        self.column_qualifier_checkin_id = bigtable_constants.payana_checkin_id

        self.payana_checkin_instagram_embed_url = bigtable_constants.payana_checkin_instagram_embed_url
        self.payana_checkin_instagram_post_id = bigtable_constants.payana_checkin_instagram_post_id
        self.payana_checkin_airbnb_embed_url = bigtable_constants.payana_checkin_airbnb_embed_url
        self.payana_checkin_airbnb_post_id = bigtable_constants.payana_checkin_airbnb_post_id

        if self.column_qualifier_description in self.checkin_metadata:
            self.description = self.checkin_metadata[self.column_qualifier_description]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_id in self.checkin_metadata:
            self.checkin_id = self.checkin_metadata[self.column_qualifier_checkin_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_create_timestamp in self.checkin_metadata:
            self.create_timestamp = self.checkin_metadata[self.column_qualifier_create_timestamp]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_last_updated_timestamp in self.checkin_metadata:
            self.last_updated_timestamp = self.checkin_metadata[
                self.column_qualifier_last_updated_timestamp]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_owner_profile_id in self.checkin_metadata:
            self.checkin_owner_profile_id = self.checkin_metadata[
                self.column_qualifier_checkin_owner_profile_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_transport_mode in self.checkin_metadata:
            self.checkin_transport_mode = self.checkin_metadata[
                self.column_qualifier_checkin_transport_mode]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_place_name in self.checkin_metadata:
            self.checkin_place_name = self.checkin_metadata[
                self.column_qualifier_checkin_place_name]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_place_id in self.checkin_metadata:
            self.checkin_place_id = self.checkin_metadata[
                self.column_qualifier_checkin_place_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_city in self.checkin_metadata:
            self.checkin_city = self.checkin_metadata[
                self.column_qualifier_checkin_city]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_country in self.checkin_metadata:
            self.checkin_country = self.checkin_metadata[
                self.column_qualifier_checkin_country]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_checkin_state in self.checkin_metadata:
            self.checkin_state = self.checkin_metadata[
                self.column_qualifier_checkin_state]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_itinerary_id in self.checkin_metadata:
            self.checkin_itinerary_id = self.checkin_metadata[
                self.column_qualifier_itinerary_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.column_qualifier_excursion_id in self.checkin_metadata:
            self.checkin_excursion_id = self.checkin_metadata[
                self.column_qualifier_excursion_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.payana_checkin_instagram_embed_url in self.instagram_metadata:
            self.checkin_instagram_embed_url_value = self.instagram_metadata[
                self.payana_checkin_instagram_embed_url]
        else:
            # raise invalid key error or key missing error
            pass

        if self.payana_checkin_instagram_post_id in self.instagram_metadata:
            self.checkin_instagram_post_id = self.instagram_metadata[
                self.payana_checkin_instagram_post_id]
        else:
            # raise invalid key error or key missing error
            pass

        if self.payana_checkin_airbnb_embed_url in self.airbnb_metadata:
            self.checkin_airbnb_embed_url_value = self.airbnb_metadata[
                self.payana_checkin_airbnb_embed_url]
        else:
            # raise invalid key error or key missing error
            pass

        if self.payana_checkin_airbnb_post_id in self.airbnb_metadata:
            self.checkin_airbnb_post_id = self.airbnb_metadata[self.payana_checkin_airbnb_post_id]
        else:
            # raise invalid key error or key missing error
            pass

        self.update_bigtable_write_objects = []

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_checkin_id(self):

        current_timestamp_unix = str(time.time())
        checkin_id_terms = [current_timestamp_unix,
                            self.checkin_owner_profile_id]

        rand_num = random.randint(0, 1)

        if rand_num == 1:
            checkin_id_terms[0], checkin_id_terms[1] = checkin_id_terms[1], checkin_id_terms[0]

        checkin_id_hash = "".join(checkin_id_terms)

        checkin_id_binary = hashlib.sha256(checkin_id_hash.encode())

        self.checkin_id = checkin_id_binary.hexdigest()

    @payana_generic_exception_handler
    def update_checkin_bigtable(self):

        if self.checkin_id is None or self.checkin_id == "":
            self.generate_checkin_id()

        payana_checkin_table_instance = PayanaBigTable(
            bigtable_constants.payana_checkin_table)

        self.create_bigtable_write_objects()

        return payana_checkin_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def update_checkin_bigtable_column(self):

        payana_checkin_table_instance = PayanaBigTable(
            bigtable_constants.payana_checkin_table)

        payana_checkin_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_image_id_list_write_object()
        self.set_participants_list_write_object()
        self.set_activities_list_write_object()
        self.set_description_write_object()
        self.set_create_timestamp_write_object()
        self.set_last_updated_timestamp_write_object()
        self.set_checkin_owner_profile_id_write_object()
        self.set_checkin_id_write_object()
        self.set_checkin_transport_mode_write_object()
        self.set_checkin_place_name_write_object()
        self.set_checkin_place_id_write_object()
        self.set_checkin_city_write_object()
        self.set_checkin_state_write_object()
        self.set_checkin_country_write_object()
        self.set_checkin_itinerary_id_write_object()
        self.set_checkin_excursion_id_write_object()
        self.set_instagram_metadata_write_object()
        self.set_airbnb_metadata_write_object()

    @payana_generic_exception_handler
    def set_image_id_list_write_object(self):

        # excursion_id_list write object
        for key, image_id in self.image_id_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.checkin_id, self.column_family_image_id_list, key, image_id))

    @payana_generic_exception_handler
    def set_participants_list_write_object(self):

        # participants_list write object
        for participant, timestamp in self.participants_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.checkin_id, self.column_family_participants_list, participant, timestamp))

    @payana_generic_exception_handler
    def set_activities_list_write_object(self):

        # participants_list write object
        for activity, number in self.activities_list.items():
            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.checkin_id, self.column_family_activities_list, activity, number))

    @payana_generic_exception_handler
    def set_instagram_metadata_write_object(self):

        # instagram metadata write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_instagram_metadata, self.payana_checkin_instagram_embed_url, self.checkin_instagram_embed_url_value))

        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_instagram_metadata, self.payana_checkin_instagram_post_id, self.checkin_instagram_post_id))

    @payana_generic_exception_handler
    def set_airbnb_metadata_write_object(self):

        # airbnb metadata  write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_airbnb_metadata, self.payana_checkin_airbnb_embed_url, self.checkin_airbnb_embed_url_value))

        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_airbnb_metadata, self.payana_checkin_airbnb_post_id, self.checkin_airbnb_post_id))

    @payana_generic_exception_handler
    def set_description_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_description, self.description))

    @payana_generic_exception_handler
    def set_create_timestamp_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_create_timestamp, self.create_timestamp))

    @payana_generic_exception_handler
    def set_last_updated_timestamp_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_last_updated_timestamp, self.last_updated_timestamp))

    @payana_generic_exception_handler
    def set_checkin_owner_profile_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_owner_profile_id, self.checkin_owner_profile_id))

    @payana_generic_exception_handler
    def set_checkin_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_id, self.checkin_id))

    @payana_generic_exception_handler
    def set_checkin_transport_mode_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_transport_mode, self.checkin_transport_mode))

    @payana_generic_exception_handler
    def set_checkin_place_name_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_place_name, self.checkin_place_name))

    @payana_generic_exception_handler
    def set_checkin_place_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_place_id, self.checkin_place_id))

    @payana_generic_exception_handler
    def set_checkin_city_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_city, self.checkin_city))

    @payana_generic_exception_handler
    def set_checkin_state_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_state, self.checkin_state))

    @payana_generic_exception_handler
    def set_checkin_country_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_checkin_country, self.checkin_country))

    @payana_generic_exception_handler
    def set_checkin_itinerary_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_itinerary_id, self.checkin_itinerary_id))

    @payana_generic_exception_handler
    def set_checkin_excursion_id_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.checkin_id, self.column_family_checkin_metadata, self.column_qualifier_excursion_id, self.checkin_excursion_id))
