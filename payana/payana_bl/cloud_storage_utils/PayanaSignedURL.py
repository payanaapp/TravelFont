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
from payana.payana_bl.cloud_storage_utils.payana_generate_gcs_signed_url import payana_generate_upload_signed_url, payana_generate_upload_resumable_signed_url, payana_generate_download_signed_url


# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaSignedURL:

    @payana_generic_exception_handler
    def __init__(self, payana_bucket_name, payana_object_name):

        self.payana_bucket_name = payana_bucket_name
        self.payana_object_name = payana_object_name

    @payana_generic_exception_handler
    def get_signed_upload_url(self):

        return payana_generate_upload_signed_url(
            self.payana_bucket_name, self.payana_object_name)

    @payana_generic_exception_handler
    def get_signed_resumable_upload_url(self):

        return payana_generate_upload_resumable_signed_url(
            self.payana_bucket_name, self.payana_object_name)

    @payana_generic_exception_handler
    def get_signed_download_url(self):

        return payana_generate_download_signed_url(
            self.payana_bucket_name, self.payana_object_name)
