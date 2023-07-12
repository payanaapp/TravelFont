#!/usr/bin/env python

"""Demonstrates how to write comments into BigTable
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
from payana.payana_core.gmail_utils.payana_invitation_send_mail import payana_send_invitation_mail

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaSignUpMailNotificationTable:

    @payana_generic_exception_handler
    def __init__(self, profile_name, sign_up_mail_id_list, itinerary_id, itinerary_name):

        self.sign_up_mail_id_list = sign_up_mail_id_list
        self.profile_name = profile_name
        self.itinerary_id = itinerary_id
        self.itinerary_name = itinerary_name


    @payana_generic_exception_handler
    def update_mail_sign_up_notification_bigtable(self):
        return payana_send_invitation_mail(self.profile_name, self.itinerary_id, self.itinerary_name, self.sign_up_mail_id_list[0])
