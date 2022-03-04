#!/usr/bin/env python

"""Contains Big Table Read Utils
"""

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_none_exception_handler

@payana_none_exception_handler
def convert_big_table_row_without_family_dict(bigtable_row):

    row_dict = {}

    for col_family_id in bigtable_row.cells:

        for column_qualifier_id in bigtable_row.cells[col_family_id]:
            column_qualifier_value = column_qualifier_id.decode("utf-8")
            column_value = bigtable_row.cells[col_family_id][column_qualifier_id][0]

            row_dict[column_qualifier_value] = column_value.value.decode(
                "utf-8")

    return row_dict

@payana_none_exception_handler
def convert_big_table_row_with_family_dict(bigtable_row):
    
    row_dict = {}

    for col_family_id in bigtable_row.cells:

        row_dict[col_family_id] = {}

        for column_qualifier_id in bigtable_row.cells[col_family_id]:
            column_qualifier_value = column_qualifier_id.decode("utf-8")
            column_value = bigtable_row.cells[col_family_id][column_qualifier_id][0]

            row_dict[col_family_id][column_qualifier_value] = column_value.value.decode(
                "utf-8")

    return row_dict


@payana_none_exception_handler
def convert_big_table_rows_to_dict(bigtable_rows, include_column_family=True):

    bigtable_rows_dict = {}

    for bigtable_row in bigtable_rows:
                    
        bigtable_row_key = bigtable_row.row_key.decode("utf-8")

        if include_column_family:
            bigtable_rows_dict[bigtable_row_key] = convert_big_table_row_with_family_dict(bigtable_row)
        else:
            bigtable_rows_dict[bigtable_row_key] = convert_big_table_row_without_family_dict(bigtable_row)

    return bigtable_rows_dict

@payana_none_exception_handler
def get_big_table_rows_cell_count(bigtable_rows, column_family_present=True):

    cells_count = 0

    for bigtable_row_key in bigtable_rows:

        if column_family_present:

            for col_family_id in bigtable_rows[bigtable_row_key]:
                cells_count += len(bigtable_rows[bigtable_row_key][col_family_id])

        else:
            cells_count += len(bigtable_rows[bigtable_row_key])

    return cells_count