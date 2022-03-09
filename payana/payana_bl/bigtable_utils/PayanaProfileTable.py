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


class PayanaProfileTable:

    @payana_generic_exception_handler
    def __init__(self, personal_information, top_activities):
        
        self.payana_profile_table_profile_name = bigtable_constants.payana_profile_table_profile_name
        self.payana_profile_table_user_name = bigtable_constants.payana_profile_table_user_name
        self.payana_profile_table_blog_url = bigtable_constants.payana_profile_table_blog_url
        self.payana_profile_table_profile_description = bigtable_constants.payana_profile_table_profile_description
        self.payana_profile_table_profile_id = bigtable_constants.payana_profile_table_profile_id
        self.payana_profile_table_email = bigtable_constants.payana_profile_table_email
        self.payana_profile_table_phone = bigtable_constants.payana_profile_table_phone
        self.payana_profile_table_private_account = bigtable_constants.payana_profile_table_private_account
        self.payana_profile_table_gender = bigtable_constants.payana_profile_table_gender
        self.payana_profile_table_date_of_birth = bigtable_constants.payana_profile_table_date_of_birth

        if self.payana_profile_table_profile_name in personal_information:
            self.profile_name = personal_information[self.payana_profile_table_profile_name]
        else:
            pass

        if self.payana_profile_table_user_name in personal_information:
            self.user_name = personal_information[self.payana_profile_table_user_name]
        else:
            pass

        if self.payana_profile_table_blog_url in personal_information:
            self.blog_url = personal_information[self.payana_profile_table_blog_url]
        else:
            pass

        if self.payana_profile_table_profile_description in personal_information:
            self.profile_description = personal_information[self.payana_profile_table_profile_description]
        else:
            pass


        if self.payana_profile_table_profile_id in personal_information:
            self.profile_id = personal_information[self.payana_profile_table_profile_id]
        else:
            pass

        if self.payana_profile_table_email in personal_information:
            self.email = personal_information[self.payana_profile_table_email]
        else:
            pass

        if self.payana_profile_table_phone in personal_information:
            self.phone = personal_information[self.payana_profile_table_phone]
        else:
            pass

        if self.payana_profile_table_private_account in personal_information:
            self.private_account = personal_information[self.payana_profile_table_private_account]
        else:
            pass

        if self.payana_profile_table_gender in personal_information:
            self.gender = personal_information[self.payana_profile_table_gender]
        else:
            pass

        if self.payana_profile_table_date_of_birth in personal_information:
            self.date_of_birth = personal_information[self.payana_profile_table_date_of_birth]
        else:
            pass

        self.top_activities = top_activities

        self.update_bigtable_write_objects = []
        self.column_family_id = bigtable_constants.payana_profile_table_personal_info_column_family
        self.top_activities_column_family_id = bigtable_constants.payana_profile_table_top_activities

    @payana_generic_exception_handler
    def toJSON(self):
        return self.__dict__

    @payana_generic_exception_handler
    def generate_profile_id(self):

        current_timestamp_unix = str(time.time())
        profile_id_terms = [current_timestamp_unix, self.profile_name]

        rand_num = random.randint(0, 1)

        if rand_num == 1:
            profile_id_terms[0], profile_id_terms[1] = profile_id_terms[1], profile_id_terms[0]

        profile_id_hash = "".join(profile_id_terms)

        profile_id_binary = hashlib.sha256(profile_id_hash.encode())

        self.profile_id = profile_id_binary.hexdigest()

    @payana_generic_exception_handler
    def update_profile_info_bigtable(self):

        if self.profile_id is None or self.profile_id == "":
            self.generate_profile_id()

        payana_profile_table_instance = PayanaBigTable(
            bigtable_constants.payana_profile_table)

        self.create_bigtable_write_objects()

        payana_profile_table_instance.insert_columns(
            self.update_bigtable_write_objects)

    @payana_generic_exception_handler
    def create_bigtable_write_objects(self):
        self.set_profile_id_write_object()
        self.set_profile_name_write_object()
        self.set_user_name_write_object()
        self.set_blog_url_write_object()
        self.set_profile_description_write_object()
        self.set_email_write_object()
        self.set_phone_write_object()
        self.set_private_account_write_object()
        self.set_gender_write_object()
        self.set_date_of_birth_write_object()
        self.set_top_activities_write_object()

    @payana_generic_exception_handler
    def set_profile_name_write_object(self):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_profile_name, self.profile_name))

    @payana_generic_exception_handler
    def set_profile_id_write_object(self):

        # profile_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_profile_id, self.profile_id))

    @payana_generic_exception_handler
    def set_user_name_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_user_name, self.user_name))

    @payana_generic_exception_handler
    def set_blog_url_write_object(self):

        # user_name write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_blog_url, self.blog_url))

    @payana_generic_exception_handler
    def set_profile_description_write_object(self):

        # profile_description write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_profile_description, self.profile_description))

    @payana_generic_exception_handler
    def set_email_write_object(self):

        # email write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_email, self.email))

    @payana_generic_exception_handler
    def set_phone_write_object(self):

        # phone write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_phone, self.phone))

    @payana_generic_exception_handler
    def set_private_account_write_object(self):

        # private_account write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_private_account, self.private_account))

    @payana_generic_exception_handler
    def set_gender_write_object(self):

        # gender write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_gender, self.gender))

    @payana_generic_exception_handler
    def set_date_of_birth_write_object(self):

        # date_of_birth write object
        self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
            self.profile_id, self.column_family_id, bigtable_constants.payana_profile_table_date_of_birth, self.date_of_birth))

    @payana_generic_exception_handler
    def set_top_activities_write_object(self):

        # top_activities write object
        for activity, score in self.top_activities.items():

            self.update_bigtable_write_objects.append(bigtable_write_object_wrapper(
                self.profile_id, self.top_activities_column_family_id, activity, score))