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
from payana.payana_bl.cloud_storage_utils.payana_set_metadata_gcs_object import payana_set_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.payana_get_metadata_gcs_object import payana_get_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.payana_set_cors_policy_gcs_bucket import payana_set_cors_policy_storage_bucket, payana_get_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.payana_delete_storage_object import payana_delete_storage_object

# google cloud bigtable imports
from google.cloud.bigtable import column_family


class PayanaGCSObjectMetadata:

    @payana_generic_exception_handler
    def __init__(self, payana_bucket_name, payana_object_name=None, metadata_object=None, cors_policy=None):

        self.payana_bucket_name = payana_bucket_name
        self.payana_object_name = payana_object_name
        self.metadata_object = metadata_object
        self.cors_policy = cors_policy

    @payana_generic_exception_handler
    def get_metadata(self):

        return payana_get_metadata_gcs_object(self.payana_bucket_name, self.payana_object_name)

    @payana_generic_exception_handler
    def set_metadata(self):

        return payana_set_metadata_gcs_object(self.payana_bucket_name, self.payana_object_name, self.metadata_object)

    @payana_generic_exception_handler
    def set_object_cors_policy(self):

        return payana_set_cors_policy_storage_bucket(self.payana_bucket_name, self.cors_policy)
    
    @payana_generic_exception_handler
    def get_object_cors_policy(self):

        return payana_get_cors_policy_storage_bucket(self.payana_bucket_name)
    
    @payana_generic_exception_handler
    def delete_gcs_object(self):

        return payana_delete_storage_object(self.payana_bucket_name, self.payana_object_name)