#!/usr/bin/env python

"""Demonstrates how to create a gcs bucket
"""

import argparse

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_bl.cloud_storage_utils.payana_create_gcs_bucket import payana_create_gcs_bucket

# google cloud storage imports
from google.cloud import storage


@payana_generic_exception_handler
def payana_cloud_storage_init(payana_bucket_creation_config_file):

    # creates gcs buckets
    return payana_create_gcs_bucket(payana_bucket_creation_config_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'payana_bucket_creation_config_file', help='Payana GCS bucket details config path.')

    args = parser.parse_args()

    payana_cloud_storage_init(args.payana_table_creation_config_file)
