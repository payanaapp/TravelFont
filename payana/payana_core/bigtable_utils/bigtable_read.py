#!/usr/bin/env python

"""Demonstrates how to read from a Cloud Bigtable.
"""

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler
# [START bigtable_table_read_imports]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
from google.cloud.bigtable.row_set import RowSet
# [END bigtable_table_read_imports]


@payana_generic_exception_handler
def bigtable_row_read(table, row_key, cell_version=1):

    # [START bigtable_table_read]

    # Create a filter to only retrieve the most recent version of the cell
    row_filter = row_filters.CellsColumnLimitFilter(cell_version)
    row = table.read_row(row_key, row_filter)
    # [END bigtable_table_read]
    return [row] if row is not None else []

#TO-DO : The calling function returns a PartialRowData object which might not have the full data. Fix the issue.
@payana_generic_exception_handler
def bigtable_rows_read(table, row_set):

    # [START bigtable_rows_read]

    partial_rows = table.read_rows(row_set=row_set)

    # [END bigtable_rows_read]

    return partial_rows if partial_rows is not None else []

#TO-DO : The calling function returns a PartialRowData object which might not have the full data. Fix the issue.

@payana_generic_exception_handler
def bigtable_row_column_filter_read(table, row_key, column_filter):

    row = table.read_row(row_key, filter_=column_filter)

    if row is None:
        return []

    return [row] if row is not None else []

@payana_generic_exception_handler
def bigtable_cells_read_column_filter(table, row_filter):

    rows = table.read_rows(filter_=row_filter)
    
    return rows if rows is not None else []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('table', help='Bigtable instance table')
    parser.add_argument(
        'row_key', help='BigTable row key')

    args = parser.parse_args()
    bigtable_row_read(args.table, args.row_key)
