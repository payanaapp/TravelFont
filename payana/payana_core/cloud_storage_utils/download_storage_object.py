#!/usr/bin/env python

"""Demonstrates how to upload a blob object into a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def download_storage_object(bucket_name, blob_name, destination_file_name):
    """Downloads a file from the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            blob_name, destination_file_name
        )
    )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('blob_name',
                        help='Your GCS object name.')

    parser.add_argument('destination_file_name',
                        help='Your GCS object destination name.')

    args = parser.parse_args()

    download_storage_object(
        args.bucket_name, args.blob_name, args.destination_file_name)
