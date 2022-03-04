#!/usr/bin/env python

"""Demonstrates how to upload a blob object into a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def delete_storage_object(bucket_name, blob_name):
    """Deletes a file in the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print("Blob {} deleted.".format(blob_name))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('blob_name',
                        help='Your GCS object destination name.')

    args = parser.parse_args()

    delete_storage_object(
        args.bucket_name, args.blob_name)
