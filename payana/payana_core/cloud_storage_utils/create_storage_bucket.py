#!/usr/bin/env python

"""Demonstrates how to create a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def create_storage_bucket(bucket_name, location, storage_class):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    print(__name__)
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = storage_class
    new_bucket = storage_client.create_bucket(bucket, location=location)

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('location',
                        help='Your GCS bucket location.')

    parser.add_argument('storage_class',
                        help='Your GCS storage location.')

    args = parser.parse_args()
    create_storage_bucket(args.bucket_name, args.location, args.storage_class)
