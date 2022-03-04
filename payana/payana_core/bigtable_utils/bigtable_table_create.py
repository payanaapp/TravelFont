#!/usr/bin/env python

"""Demonstrates how to connect to Cloud Bigtable and create a table.
"""

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler
# [START bigtable_imports]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_imports]


@payana_generic_exception_handler
def bigtable_table_create(instance, table_id, column_family_dict):

    # [START bigtable_create_table]
    table = instance.table(table_id)

    if not table.exists():
        table.create(column_families=column_family_dict)
    else:
        print("Table already exists")

    # [END bigtable_create_table]

    return table


@payana_generic_exception_handler
def bigtable_table_get(instance, table_id):

    # [START bigtable_create_table]
    table = instance.table(table_id)

    if not table.exists():
        return None

    # [END bigtable_create_table]
    return table


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'instance', help='instance of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        '--table',
        help='Table to create and destroy.')
    parser.add_argument(
        'column_families', help='a dict object of column families and versions.')

    args = parser.parse_args()
    bigtable_table_create(args.instance, args.table, args.column_families)
