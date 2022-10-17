#!/usr/bin/env python

"""Demonstrates how to read from a Cloud Bigtable.
"""

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_boolean_exception_handler
from payana.payana_core.common_utils.payana_core_bigtable_write_utils import payana_bigtable_write_status_handler, payana_bigtable_delete_status_handler
# [START bigtable_table_read_imports]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_table_read_imports]


@payana_boolean_exception_handler
def bigtable_row_delete(table, row_key):

    # [START bigtable_row_delete]

    bigtable_row_obj = table.row(row_key)

    bigtable_row_obj.delete()
    delete_status = bigtable_row_obj.commit()

    return payana_bigtable_delete_status_handler(delete_status)
    # [END bigtable_row_delete]


@payana_boolean_exception_handler
def bigtable_rows_delete(table, row_keys):

    # [START bigtable_rows_delete]

    for row_key in row_keys:
        bigtable_row_delete(table, row_key)

    # [END bigtable_rows_delete]


@payana_boolean_exception_handler
def bigtable_row_cell_delete(table, row_key, column_family_id, column_name):

    # [START bigtable_row_cell_delete]

    bigtable_row_obj = table.row(row_key)

    bigtable_row_obj.delete_cell(column_family_id, column_name)
    delete_status = bigtable_row_obj.commit()

    return payana_bigtable_delete_status_handler(delete_status)
    # [END bigtable_row_cell_delete]


@payana_boolean_exception_handler
def bigtable_row_cells_delete(table, row_key, column_family_id, column_names):

    # [START bigtable_row_cells_delete]

    bigtable_row_obj = table.row(row_key)

    bigtable_row_obj.delete_cells(column_family_id, column_names)
    bigtable_row_obj.commit()
    # [END bigtable_row_cells_delete]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('table', help='Bigtable instance table')
    parser.add_argument(
        'row_key', help='BigTable row key')

    args = parser.parse_args()
    #bigtable_row_read(args.table, args.row_key)
