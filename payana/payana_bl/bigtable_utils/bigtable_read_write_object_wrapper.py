#!/usr/bin/env python

"""A schema for BigTableWriteObject
"""

# [START bigtable_write_object_wrapper imports]
import collections
import datetime
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
# [END bigtable_write_object_wrapper imports]


@payana_generic_exception_handler
def bigtable_write_object_wrapper(row_key, column_family_id, column_qualifier_id, column_value):

    BigTableWriteObject = collections.namedtuple(
        'BigTableWriteObject', 'row_key column_family_id column_qualifier_id column_value')

    bigtable_write_object = BigTableWriteObject(row_key=row_key.encode(), column_family_id=column_family_id,
                                                column_qualifier_id=column_qualifier_id.encode(), column_value=column_value.encode())

    return bigtable_write_object


@payana_generic_exception_handler
def bigtable_read_row_key_wrapper(row_key):

    BigTableRowKeyReadObject = collections.namedtuple(
        'BigTableRowKeyReadObject', 'row_key')

    bigtable_read_row_key_object = BigTableRowKeyReadObject(
        row_key=row_key.encode())

    return bigtable_read_row_key_object


@payana_generic_exception_handler
def bigtable_read_column_family_wrapper(row_key, column_family_id):

    BigTableColumnFamilyReadObject = collections.namedtuple(
        'BigTableColumnFamilyReadObject', 'row_key column_family_id')

    bigtable_read_column_family_object = BigTableColumnFamilyReadObject(row_key=row_key.encode(), column_family_id=column_family_id
                                                                        )

    return bigtable_read_column_family_object


@payana_generic_exception_handler
def bigtable_read_column_value_wrapper(row_key, column_family_id, column_qualifier_id):

    BigTableColumnValueReadObject = collections.namedtuple(
        'BigTableColumnValueReadObject', 'row_key column_family_id column_qualifier_id')

    bigtable_read_column_value_object = BigTableColumnValueReadObject(row_key=row_key.encode(), column_family_id=column_family_id,
                                                                      column_qualifier_id=column_qualifier_id.encode())

    return bigtable_read_column_value_object


@payana_generic_exception_handler
def get_test_data():

    column_family_id = "cf1-payana"
    greetings = ['Hello World!', 'Hello Cloud Bigtable!', 'Hello Python!']
    bigtable_rows = []
    column = 'greeting'

    for i, value in enumerate(greetings):
        row_key = 'greeting{}'.format(i)
        bigtable_rows.append(bigtable_write_object_wrapper(
            row_key, column_family_id, column, value))

    return bigtable_rows
