#!/usr/bin/env python

"""Demonstrates how to generate a signed URL for upload/download into a GCS bucket
"""
from google.cloud import storage
import argparse


from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.cloud_storage_utils.create_signed_url_gcs import create_upload_signed_url, create_download_signed_url, create_upload_resumable_signed_url
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants


@payana_generic_exception_handler
def payana_profile_picture_upload_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures

    return payana_generate_upload_signed_url(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_itinerary_picture_upload_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures

    return payana_generate_upload_signed_url(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_profile_picture_resumable_upload_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures

    return payana_generate_upload_resumable_signed_url(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_itinerary_picture_resumable_upload_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures

    return payana_generate_upload_resumable_signed_url(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_profile_picture_download_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_profile_pictures

    return payana_generate_download_signed_url(
        bucket_name, blob_name)


@payana_generic_exception_handler
def payana_itinerary_picture_download_signed_url(blob_name):
    """Deletes a file to the bucket."""

    bucket_name = gcs_constants.payana_bucket_itinerary_pictures

    return payana_generate_download_signed_url(
        bucket_name, blob_name)


@ payana_generic_exception_handler
def payana_generate_upload_signed_url(bucket_name, blob_name):
    """Deletes a file in the bucket."""

    payana_upload_signed_url_expiration_time = gcs_constants.payana_upload_signed_url_expiration_time

    return create_upload_signed_url(bucket_name, blob_name,
                                    payana_upload_signed_url_expiration_time)


@ payana_generic_exception_handler
def payana_generate_upload_resumable_signed_url(bucket_name, blob_name):
    """Deletes a file in the bucket."""

    payana_upload_signed_url_expiration_time = gcs_constants.payana_upload_signed_url_expiration_time

    return create_upload_resumable_signed_url(bucket_name, blob_name,
                                              payana_upload_signed_url_expiration_time)


@ payana_generic_exception_handler
def payana_generate_download_signed_url(bucket_name, blob_name):
    """Deletes a file in the bucket."""

    payana_download_signed_url_expiration_time = gcs_constants.payana_download_signed_url_expiration_time

    return create_download_signed_url(
        bucket_name, blob_name, payana_download_signed_url_expiration_time)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    parser.add_argument('blob_name',
                        help='Your GCS object destination name.')

    args = parser.parse_args()

    payana_generate_upload_signed_url(
        args.bucket_name, args.blob_name)
