#!/usr/bin/env python

"""Demonstrates how to set a CORS policy for a GCS bucket
"""

from google.cloud import storage

import argparse
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.cloud_storage_utils.set_cors_policy_storage_bucket import set_cors_policy_storage_bucket as core_set_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.constants import gcs_constants


@payana_generic_exception_handler
def payana_set_cors_policy_storage_bucket(bucket_name, payana_cors_policy=gcs_constants.payana_cors_policy):
    """Set a bucket's CORS policies configuration."""

    return core_set_cors_policy_storage_bucket(bucket_name, payana_cors_policy)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bucket_name',
                        help='Your GCS bucket name.')

    args = parser.parse_args()
    payana_set_cors_policy_storage_bucket(args.bucket_name)
