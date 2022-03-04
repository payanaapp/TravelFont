#!/usr/bin/env python

"""Demonstrates how to delete a Cloud Bigtable and run some basic operations.
"""

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler


@payana_generic_exception_handler
def bigtable_table_delete(table):
    # [START bigtable_table_delete]

    table.delete()

    # [END bigtable_table_delete]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('table', help='Your Cloud BigTable table.')

    args = parser.parse_args()
    bigtable_table_delete(args.table)
