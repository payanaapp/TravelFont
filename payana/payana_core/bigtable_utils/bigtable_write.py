#!/usr/bin/env python

"""Demonstrates how to write to a Cloud Bigtable.
"""

import argparse
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_boolean_exception_handler
# [START bigtable_write imports]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_write imports]


@payana_boolean_exception_handler
def bigtable_write(table, bigtable_write_objects):

    # [START bigtable_write]

    rows = []

    for _, bigtable_write_object in enumerate(bigtable_write_objects):

        row_key = bigtable_write_object.row_key
        row = table.direct_row(row_key)

        column_family_id = bigtable_write_object.column_family_id
        column_qualifier_id = bigtable_write_object.column_qualifier_id
        column_value = bigtable_write_object.column_value

        row.set_cell(column_family_id,
                     column_qualifier_id,
                     column_value,
                     timestamp=datetime.datetime.utcnow())

        rows.append(row)

    table.mutate_rows(rows)

    # [END bigtable_write]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('table', help='Bigtable instance table')
    parser.add_argument(
        'bigtable_write_objects', help='List of BigTable write objects')

    args = parser.parse_args()
    bigtable_write(args.table, args.bigtable_write_objects)
