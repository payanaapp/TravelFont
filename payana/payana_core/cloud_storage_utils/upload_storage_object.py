#!/usr/bin/env python

"""Demonstrates how to upload a blob object into a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def upload_storage_object(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('source_file_name',
                        help='Your GCS object source filename.')

    parser.add_argument('destination_blob_name',
                        help='Your GCS object destination name.')

    args = parser.parse_args()

    upload_storage_object(
        args.bucket_name, args.source_file_name, args.destination_blob_name)
