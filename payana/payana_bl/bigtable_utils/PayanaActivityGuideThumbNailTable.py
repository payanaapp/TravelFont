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


class PayanaActivityGuideThumbNailTable:

    @payana_generic_exception_handler
    def __init__(self, payana_activity_thumbnail, city):

        self.payana_activity_thumbnail = payana_activity_thumbnail
        self.city = city

        self.update_bigtable_write_objects = []

        self.column_family_id = bigtable_constants.payana_activity_thumbnail

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def update_activity_guide_thumbnail_bigtable(self):

        payana_activity_guide_thumbnail_table_instance = PayanaBigTable(
            bigtable_constants.payana_activity_guide_thumbnail_table)

        self.create_bigtable_write_objects()

        return payana_activity_guide_thumbnail_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_payana_profile_pictures_write_object()

    @payana_generic_exception_handler
    def set_payana_profile_pictures_write_object(self):

        # top_friends write object
        for activity, thumbnail_dict in self.payana_activity_thumbnail.items():
            
            if activity in bigtable_constants.payana_activity_column_family:
            
                for image_id, timestamp in thumbnail_dict.items():
                    
                    self.activity_thumbnail_column_family_id = "_".join([activity, self.column_family_id])

                    self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                        self.city, self.activity_thumbnail_column_family_id, image_id, timestamp))
