#!/usr/bin/env python

"""Demonstrates how to create the tables for payana.
"""

import argparse
import datetime
import json
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_core.bigtable_utils.bigtable_table_create import bigtable_table_get
from payana.payana_core.bigtable_utils.bigtable_table_delete import bigtable_table_delete
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler

# [START bigtable_imports]
from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_imports]


@payana_generic_exception_handler
def payana_tables_delete(payana_table_creation_config_file, instance):

    print(__name__)

    # [START bigtable_create_table]
    # read the table names and column families
    with open(payana_table_creation_config_file) as json_data_file:
        payana_tables_dict = json.load(json_data_file)

    for table_id in payana_tables_dict.keys():

        table = bigtable_table_get(instance, table_id)

        bigtable_table_delete(table)
        print("Deleted table: " + table_id)

    # [END bigtable_create_table]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'payana_table_creation_config_file', help='List of all the tables to create for payana')
    parser.add_argument(
        'instance', help='BigTable instance to create the table')

    args = parser.parse_args()

    payana_tables_delete(args.payana_table_creation_config_file, args.instance)
