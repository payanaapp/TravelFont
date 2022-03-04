#!/usr/bin/env python

"""Contains Big Table Column Filter Read Utils
"""

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from google.cloud.bigtable import row_filters


@payana_generic_exception_handler
def bigtable_cells_column_family_read_filter(column_family_id):

    row_filter = row_filters.FamilyNameRegexFilter(column_family_id)

    return row_filter

@payana_generic_exception_handler
def bigtable_cells_per_column_limit(cells_column_count):

    row_filter = row_filters.CellsColumnLimitFilter(cells_column_count)

    return row_filter

@payana_generic_exception_handler
def bigtable_cells_per_row_limit(cells_row_count):

    row_filter = row_filters.CellsRowLimitFilter(cells_row_count)

    return row_filter

@payana_generic_exception_handler
def bigtable_cells_column_qualifier_read_filter(column_qualifier):

    row_filter = row_filters.ColumnQualifierRegexFilter(column_qualifier)

    return row_filter

@payana_generic_exception_handler
def bigtable_row_regex_read_filter(row_regex):

    row_filter = row_filters.RowKeyRegexFilter(row_regex)

    return row_filter

@payana_generic_exception_handler
def bigtable_cells_column_range_read_filter(column_family_id, column_qualifier_start_key=None, column_qualifier_end_key=None, inclusive_start=True, inclusive_end=True):

    row_filter = None

    if column_qualifier_start_key is None:
        row_filter = row_filters.ColumnRangeFilter(column_family_id=column_family_id, end_column=column_qualifier_end_key, inclusive_end=inclusive_end)
    elif column_qualifier_end_key is None:
        row_filter = row_filters.ColumnRangeFilter(column_family_id=column_family_id, start_column=column_qualifier_start_key, inclusive_start=inclusive_start)
    else:
        row_filter = row_filters.ColumnRangeFilter(column_family_id=column_family_id, start_column=column_qualifier_start_key, end_column=column_qualifier_end_key, inclusive_start=inclusive_start, inclusive_end=inclusive_end)

    return row_filter

@payana_generic_exception_handler
def bigtable_cells_value_range_read_filter(value_start_key=None, value_end_key=None, inclusive_start=True, inclusive_end=True):

    row_filter = None

    if value_start_key is None:
        row_filter = row_filters.ValueRangeFilter(end_value=value_end_key, inclusive_end=inclusive_end)
    elif value_end_key is None:
        row_filter = row_filters.ValueRangeFilter(start_value=value_start_key, inclusive_start=inclusive_start)
    else:
        row_filter = row_filters.ValueRangeFilter(start_value=value_start_key, end_value=value_end_key, inclusive_start=inclusive_start, inclusive_end=inclusive_end)
    
    return row_filter

@payana_generic_exception_handler
def bigtable_cells_timestamp_range_read_filter(start_timestamp=None, end_timestamp=None):

    row_filter = None

    if start_timestamp is None:
        row_filter = row_filters.TimestampRangeFilter(row_filters.TimestampRange(end=end_timestamp))
    elif end_timestamp is None:
        row_filter = row_filters.TimestampRangeFilter(row_filters.TimestampRange(start=start_timestamp))
    else:
        row_filter = row_filters.TimestampRangeFilter(row_filters.TimestampRange(start=start_timestamp,end=end_timestamp))
    
    return row_filter

@payana_generic_exception_handler
def bigtable_cells_read_column_filter_chain(row_chain_filters):

    row_filter_chain = row_filters.RowFilterChain(filters=row_chain_filters)
    
    return row_filter_chain

@payana_generic_exception_handler
def bigtable_cells_read_column_interleave_filter(row_interleave_filters):

    row_filter_interleave = row_filters.RowFilterUnion(filters=row_interleave_filters)
    
    return row_filter_interleave

@payana_generic_exception_handler
def bigtable_cells_read_value_regex(value_regex):

    value_regex_filter = row_filters.ValueRegexFilter(value_regex)
    
    return value_regex_filter

@payana_generic_exception_handler
def bigtable_cells_label_filter(filter_label):

    label_filter = row_filters.ApplyLabelFilter(label=filter_label)
    
    return label_filter

@payana_generic_exception_handler
def bigtable_cells_value_strip_filter():

    strip_filter = row_filters.StripValueTransformerFilter(True)
    
    return strip_filter