#!/usr/bin/env python

"""Demonstrates how to update a blob object metadata in a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.cloud_storage_utils.set_metadata_storage_object import set_metadata_storage_object as core_set_metadata_storage_object
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants


@payana_generic_exception_handler
def payana_profile_picture_set_metadata_gcs_object(blob_name, metadata):
    """Set a blob's metadata."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures

    payana_set_metadata_gcs_object(
        bucket_name, blob_name, metadata)


@payana_generic_exception_handler
def payana_itinerary_picture_set_metadata_gcs_object(blob_name, metadata):
    """Set a blob's metadata."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures

    payana_set_metadata_gcs_object(
        bucket_name, blob_name, metadata)


@payana_generic_exception_handler
def payana_set_metadata_gcs_object(bucket_name, blob_name, metadata):
    """Set a blob's metadata."""

    core_set_metadata_storage_object(bucket_name, blob_name, metadata)


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

    payana_set_metadata_gcs_object(
        args.bucket_name, args.blob_name, args.metadata)
