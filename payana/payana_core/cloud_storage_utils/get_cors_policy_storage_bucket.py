#!/usr/bin/env python

"""Demonstrates how to set a CORS policy for a GCS bucket
"""

from google.cloud import storage

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def get_cors_policy_storage_bucket(bucket_name):
    """Get a bucket's CORS policies configuration."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    cors_policy = bucket.cors
    
    return cors_policy


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('cors_policy',
                        help='Your GCS bucket CORS policy.')

    args = parser.parse_args()
    get_cors_policy_storage_bucket(args.bucket_name, args.cors_policy)
