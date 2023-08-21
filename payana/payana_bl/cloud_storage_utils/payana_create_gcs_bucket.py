#!/usr/bin/env python

"""Demonstrates how to create a gcs bucket
"""

import argparse
import json

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.cloud_storage_utils.create_storage_bucket import create_storage_bucket
from payana.payana_bl.cloud_storage_utils.payana_set_cors_policy_gcs_bucket import payana_set_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants

# google cloud storage imports
from google.cloud import storage


@payana_generic_exception_handler
def payana_create_gcs_bucket(payana_bucket_creation_config_file):

    # creates gcs buckets
    # read the bucket names and column families
    with open(payana_bucket_creation_config_file) as json_data_file:
        payana_bucket_creation_dict = json.load(json_data_file)

    gcs_location_term = gcs_constants.payana_bucket_location
    gcs_storage_term = gcs_constants.payana_bucket_storage_class

    for bucket_name, bucket_details in payana_bucket_creation_dict.items():

        if gcs_location_term in bucket_details and gcs_storage_term in bucket_details:

            location = bucket_details[gcs_location_term]
            storage_class = bucket_details[gcs_storage_term]

            create_storage_bucket(bucket_name, location, storage_class)
            payana_set_cors_policy_storage_bucket(bucket_name)
            
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'payana_bucket_creation_config_file', help='Payana GCS bucket details config path.')

    args = parser.parse_args()

    payana_create_gcs_bucket(args.payana_table_creation_config_file)
