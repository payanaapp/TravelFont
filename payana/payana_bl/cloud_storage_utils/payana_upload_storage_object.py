#!/usr/bin/env python

"""Demonstrates how to upload a blob object into a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants
from payana.payana_core.cloud_storage_utils.upload_storage_object import upload_storage_object as core_upload_storage_object


@payana_generic_exception_handler
def payana_profile_picture_upload_storage_object(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures
    payana_upload_storage_object(
        bucket_name, source_file_name, destination_blob_name)


@payana_generic_exception_handler
def payana_itinerary_picture_upload_storage_object(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures
    payana_upload_storage_object(
        bucket_name, source_file_name, destination_blob_name)


@payana_generic_exception_handler
def payana_upload_storage_object(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    core_upload_storage_object(
        bucket_name, source_file_name, destination_blob_name)


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

    payana_upload_storage_object(
        args.bucket_name, args.source_file_name, args.destination_blob_name)
