#!/usr/bin/env python

"""Demonstrates how to create a bigtable cluster, connect to Cloud Bigtable instance, 
create and write a table, read from the table
"""

import argparse
from payana.payana_core.bigtable_utils.bigtable_client_create import bigtable_client_create
from payana.payana_core.bigtable_utils.bigtable_instance_connect import bigtable_connect
from payana.payana_bl.bigtable_utils.payana_table_creation import payana_table_create
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler

# google cloud bigtable imports
from google.cloud.bigtable import column_family


@payana_generic_exception_handler
def payana_bigtable_init(client_config_path, payana_table_creation_config_file):

    print(__name__)

    # creates bigtable client
    bigtable_client_create(client_config_path)

    # Create an instance for BigTable
    instance = bigtable_connect(client_config_path)

    print("Bigtable instance fetched.")

    payana_table_create(payana_table_creation_config_file, instance)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'client_config_path', help='bigtable client details config path.')

    parser.add_argument(
        'payana_table_creation_config_file', help='bigtable client details config path.')

    args = parser.parse_args()

    payana_bigtable_init(
        args.client_config_path, args.payana_table_creation_config_file)
