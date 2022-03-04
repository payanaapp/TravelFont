#!/usr/bin/env python

"""Demonstrates how to get a blob object metadata in a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.cloud_storage_utils.get_metadata_storage_object import get_metadata_storage_object as core_get_metadata_storage_object
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants


@payana_generic_exception_handler
def payana_profile_picture_get_metadata_gcs_object(blob_name):
    """Set a blob's metadata."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures

    return payana_get_metadata_gcs_object(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_itinerary_picture_get_metadata_gcs_object(blob_name):
    """Set a blob's metadata."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures

    return payana_get_metadata_gcs_object(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_get_metadata_gcs_object(bucket_name, blob_name):
    """Get a blob's metadata."""

    return core_get_metadata_storage_object(bucket_name, blob_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('blob_name',
                        help='Your GCS object destination name.')

    parser.add_argument('metadata',
                        help='Your GCS object destination name.')

    args = parser.parse_args()

    payana_get_metadata_gcs_object(
        args.bucket_name, args.blob_name)
