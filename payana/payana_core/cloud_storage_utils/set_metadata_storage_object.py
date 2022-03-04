#!/usr/bin/env python

"""Demonstrates how to update a blob object metadata in a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def set_metadata_storage_object(bucket_name, blob_name, blob_metadata):
    """Set a blob's metadata."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    blob.metadata = blob_metadata
    blob.patch()

    print("The metadata for the blob {} is {}".format(blob.name, blob.metadata))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('blob_name',
                        help='Your GCS object destination name.')

    parser.add_argument('blob_metadata',
                        help='Your GCS object metadata.')

    args = parser.parse_args()

    set_metadata_storage_object(
        args.bucket_name, args.blob_name, args.blob_metadata)
