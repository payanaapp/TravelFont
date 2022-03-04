#!/usr/bin/env python

"""Demonstrates how to create a GCS bucket
"""

from google.cloud import storage

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def delete_storage_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(
        "Deleted bucket  {}".format(
            bucket.name
        )
    )
    return bucket


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    args = parser.parse_args()
    delete_storage_bucket(args.bucket_name)
