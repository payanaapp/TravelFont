#!/usr/bin/env python

"""Contains Big Table Column Filter Read Utils
"""

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_bl.common_utils.bigtable_filter_read_utils import bigtable_cells_column_family_read_filter, bigtable_cells_column_qualifier_read_filter, bigtable_cells_column_range_read_filter, bigtable_cells_value_range_read_filter, bigtable_cells_timestamp_range_read_filter, bigtable_cells_read_column_filter_chain, bigtable_row_regex_read_filter, bigtable_cells_per_column_limit, bigtable_cells_per_row_limit, bigtable_cells_read_value_regex, bigtable_cells_read_column_interleave_filter, bigtable_cells_label_filter, bigtable_cells_value_strip_filter
from google.cloud.bigtable import row_filters

@payana_generic_exception_handler
def get_table_rows_count_filter():

    strip_filter = bigtable_cells_value_strip_filter()

    return strip_filter

@payana_generic_exception_handler
def get_column_family_count_filter(column_family_id):

    strip_filter = bigtable_cells_value_strip_filter()

    column_family_filter = bigtable_cells_column_family_read_filter(column_family_id)

    return [column_family_filter, strip_filter]

@payana_generic_exception_handler
def get_column_qualifier_count_filter(column_qualifier):

    strip_filter = bigtable_cells_value_strip_filter()

    column_qualifier_filter = bigtable_cells_column_qualifier_read_filter(column_qualifier)

    return [column_qualifier_filter, strip_filter]

@payana_generic_exception_handler
def get_row_regex_filter_count_filter(row_regex): #todo

    strip_filter = bigtable_cells_value_strip_filter()

    row_regex_filter = bigtable_row_regex_read_filter(row_regex)

    return [row_regex_filter, strip_filter]

@payana_generic_exception_handler
def get_column_range_count_filter(column_family_id, column_qualifier_start_key=None, column_qualifier_end_key=None):

    strip_filter = bigtable_cells_value_strip_filter()

    column_range_filter = bigtable_cells_column_range_read_filter(column_family_id, column_qualifier_start_key, column_qualifier_end_key)

    return [column_range_filter, strip_filter]

@payana_generic_exception_handler
def get_value_range_count_filter(value_start_key=None, value_end_key=None):

    strip_filter = bigtable_cells_value_strip_filter()

    value_range_filter = bigtable_cells_value_range_read_filter(value_start_key, value_end_key)

    return [value_range_filter, strip_filter]

@payana_generic_exception_handler
def get_timestamp_range_count_filter(start_timestamp=None, end_timestamp=None):

    strip_filter = bigtable_cells_value_strip_filter()

    timestamp_range_filter = bigtable_cells_timestamp_range_read_filter(start_timestamp, end_timestamp)

    return [timestamp_range_filter, strip_filter]

@payana_generic_exception_handler
def get_value_regex_count_filter(value_regex):

    strip_filter = bigtable_cells_value_strip_filter()

    value_regex_filter = bigtable_cells_read_value_regex(value_regex)

    return [value_regex_filter, strip_filter]


@payana_generic_exception_handler
def get_value_regex_on_column_family_filter(column_family_id, value_regex, count=False):

    column_family_filter = bigtable_cells_column_family_read_filter(column_family_id)

    strip_filter = bigtable_cells_value_strip_filter()

    value_regex_filter = bigtable_cells_read_value_regex(value_regex)

    return [column_family_filter, value_regex_filter, strip_filter] if count else [column_family_filter, value_regex_filter]

@payana_generic_exception_handler
def get_value_range_on_column_family_filter(column_family_id, value_start_key=None, value_end_key=None, count=False):

    column_family_filter = bigtable_cells_column_family_read_filter(column_family_id)

    strip_filter = bigtable_cells_value_strip_filter()

    value_range_filter = bigtable_cells_value_range_read_filter(value_start_key, value_end_key)

    return [column_family_filter, value_range_filter, strip_filter] if count else [column_family_filter, value_range_filter]

@payana_generic_exception_handler
def get_timestamp_range_on_column_family_filter(column_family_id, start_timestamp=None, end_timestamp=None, count=False):

    column_family_filter = bigtable_cells_column_family_read_filter(column_family_id)

    strip_filter = bigtable_cells_value_strip_filter()

    timestamp_range_filter = bigtable_cells_timestamp_range_read_filter(start_timestamp, end_timestamp)

    return [column_family_filter, timestamp_range_filter, strip_filter] if count else [column_family_filter, timestamp_range_filter]