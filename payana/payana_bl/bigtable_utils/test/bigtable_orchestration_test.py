#!/usr/bin/env python

"""Demonstrates how to create a bigtable cluster, connect to Cloud Bigtable instance, 
create and write a table, read from the table
"""

import argparse

from payana.payana_core.bigtable_utils.bigtable_client_create import bigtable_client_create
from payana.payana_core.bigtable_utils.bigtable_instance_connect import bigtable_connect
from payana.payana_core.bigtable_utils.bigtable_table_create import bigtable_table_create
from payana.payana_core.bigtable_utils.bigtable_write import bigtable_write
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_column_value_wrapper, bigtable_read_row_key_wrapper, get_test_data
from payana.payana_core.bigtable_utils.bigtable_read import bigtable_row_read, bigtable_rows_read
from payana.payana_core.bigtable_utils.bigtable_table_delete import bigtable_table_delete
from payana.payana_core.bigtable_utils.bigtable_client_delete import bigtable_client_delete
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler

# google cloud bigtable imports
from google.cloud.bigtable import column_family
from google.cloud.bigtable.row_set import RowSet


@payana_generic_exception_handler
def bigtable_orchestration(client_config_path):

    # creates bigtable client
    bigtable_client_create(client_config_path)

    # Create an instance for BigTable
    bigtable_instance = bigtable_connect(client_config_path)

    # create a BigTable table
    table_id = "table-payana"
    max_versions_rule = column_family.MaxVersionsGCRule(1)
    column_family_id = "cf1-payana"
    column_family_dict = {column_family_id: max_versions_rule}

    table = bigtable_table_create(
        bigtable_instance, table_id, column_family_dict)

    # Writing data into the table
    bigtable_write_objects = get_test_data()
    bigtable_write(table, bigtable_write_objects)

    # read one row of data
    row_key = 'greeting0'.encode()
    #row_object = bigtable_read_row_key_wrapper(row_key)
    bigtable_row = bigtable_row_read(table, row_key)
    print(len(bigtable_row))

    # print the data
    column = 'greeting'.encode()
    bigtable_row = bigtable_row[0]
    #bigtable_read_column_value_wrapper(row_key, column_family_id, row_key)
    cell = bigtable_row.cells[column_family_id][column][0]
    print(cell.value.decode('utf-8'))

    row_set = RowSet()

    # read the whole table
    bigtable_rows = bigtable_rows_read(table, row_set)

    for row in bigtable_rows:
        cell = row.cells[column_family_id][column][0]
        print(cell.value.decode('utf-8'))

    # delete the bigtable
    bigtable_table_delete(table)

    # delete the bigtable cluster
    bigtable_client_delete(client_config_path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'client_config_path', help='bigtable client details config path.')

    args = parser.parse_args()
    bigtable_orchestration(args.client_config_path)
