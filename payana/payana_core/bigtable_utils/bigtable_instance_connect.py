#!/usr/bin/env python

"""Demonstrates how to connect to Cloud Bigtable instance

Prerequisites:

- Create a Cloud Bigtable cluster.
  https://cloud.google.com/bigtable/docs/creating-cluster
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials
"""

import argparse
# [START bigtable_imports]
import datetime
import yaml
from payana.payana_core.bigtable_utils.constants import bigtable_constants
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_imports]


@payana_generic_exception_handler
def bigtable_connect(cluster_config_file):
    # [START bigtable_connect]
    # The client must be created with admin=True because it will create a
    # table.

    # read config file for cluster
    with open(cluster_config_file, "r") as ymlfile:
        cluster_config = yaml.safe_load(ymlfile)

    instance_id = cluster_config[bigtable_constants.bigtable_instance_id]
    project_id = cluster_config[bigtable_constants.bigtable_project_id]

    bigtable_client = bigtable.Client(project=project_id, admin=True)
    bigtable_instance = bigtable_client.instance(instance_id)

    return bigtable_instance


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('cluster_config_file',
                        help='Your BigTable cluster config file.')

    args = parser.parse_args()
    bigtable_connect(args.cluster_config_file)
