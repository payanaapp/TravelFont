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


class PayanaProfilePageItineraryTable:

    @payana_generic_exception_handler
    def __init__(self, profile_id, saved_activity_guide_id_list, created_activity_guide_id_list,
                 saved_itinerary_id_list, saved_excursion_id_list, created_itinerary_id_list,
                 created_excursion_id_list, activities):

        self.profile_id = profile_id
        self.saved_itinerary_id_list = saved_itinerary_id_list
        self.saved_excursion_id_list = saved_excursion_id_list
        self.created_itinerary_id_list = created_itinerary_id_list
        self.created_excursion_id_list = created_excursion_id_list
        self.activities = activities
        self.saved_activity_guide_id_list = saved_activity_guide_id_list
        self.created_activity_guide_id_list = created_activity_guide_id_list
        
        self.row_id = None

        self.update_bigtable_write_objects = []

        self.activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family
        self.payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value
        self.payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value
        self.payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value
        self.payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value
        self.payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value
        self.payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value

        self.current_ts = str(int(datetime.utcnow().timestamp()))

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_row_id(self):

        self.row_id = self.profile_id

    @payana_generic_exception_handler
    def update_payana_profile_page_itinerary_bigtable(self):

        if self.row_id is None:
            self.generate_row_id()

        payana_profile_page_itinerary_instance = PayanaBigTable(
            bigtable_constants.payana_profile_page_itinerary_table)

        self.create_bigtable_write_objects()

        return payana_profile_page_itinerary_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_activities_write_object()

    @payana_generic_exception_handler
    def set_activities_write_object(self):

        # all activities write objects

        for activity in self.activities:
            if activity in bigtable_constants.payana_activity_column_family:

                saved_itinerary_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value])

                saved_excursion_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value])
                
                saved_activity_guide_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value])

                created_itinerary_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value])

                created_excursion_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value])
                
                created_activity_guide_id_list_activity_column_family_id = "_".join(
                    [activity, self.payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value])

                for itinerary in self.saved_itinerary_id_list:
                    # itinerary id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, saved_itinerary_id_list_activity_column_family_id, self.current_ts, itinerary))

                for excursion in self.saved_excursion_id_list:
                    # excursion id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, saved_excursion_id_list_activity_column_family_id, self.current_ts, excursion))
                    
                for activity_guide in self.saved_activity_guide_id_list:
                    # excursion id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, saved_activity_guide_id_list_activity_column_family_id, self.current_ts, activity_guide))
            
                for itinerary in self.created_itinerary_id_list:
                    # itinerary id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, created_itinerary_id_list_activity_column_family_id, self.current_ts, itinerary))

                for excursion in self.created_excursion_id_list:
                    # excursion id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, created_excursion_id_list_activity_column_family_id, self.current_ts, excursion))
                    
                for activity_guide in self.created_activity_guide_id_list:
                    # excursion id write object
                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.row_id, created_activity_guide_id_list_activity_column_family_id, self.current_ts, activity_guide))

            else:
                # to-do : raise exception that it is an invalid activity
                print("Invalid activity")
                pass
