#!/usr/bin/env python

"""Demonstrates how to create a bigtable cluster, connect to Cloud Bigtable instance, 
create and write a table, read from the table
"""

import argparse

from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_core.bigtable_utils.bigtable_instance_connect import bigtable_connect
from payana.payana_core.bigtable_utils.bigtable_table_create import bigtable_table_get
from payana.payana_core.bigtable_utils.bigtable_write import bigtable_write
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_core.bigtable_utils.bigtable_read import bigtable_row_read, bigtable_rows_read, bigtable_cells_read_column_filter, bigtable_row_column_filter_read
from payana.payana_core.bigtable_utils.bigtable_row_delete import bigtable_row_delete, bigtable_rows_delete, bigtable_row_cells_delete, bigtable_row_cell_delete, bigtable_column_family_cells_delete
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler, payana_service_layer_return_exception_handler
from payana.payana_bl.common_utils.big_table_read_utils import convert_big_table_rows_to_dict
from payana.payana_bl.common_utils.bigtable_filter_read_utils import bigtable_cells_column_family_read_filter, bigtable_cells_column_qualifier_read_filter, bigtable_cells_column_range_read_filter, bigtable_cells_value_range_read_filter, bigtable_cells_timestamp_range_read_filter, bigtable_cells_read_column_filter_chain, bigtable_row_regex_read_filter, bigtable_cells_per_column_limit, bigtable_cells_per_row_limit, bigtable_cells_read_value_regex, bigtable_cells_read_column_interleave_filter, bigtable_cells_label_filter, bigtable_cells_value_strip_filter

# google cloud bigtable imports
from google.cloud.bigtable import column_family
from google.cloud.bigtable.row_set import RowSet

payana_big_table_does_not_exist_exception = bigtable_constants.payana_big_table_does_not_exist_exception
payana_big_table_exception = bigtable_constants.payana_big_table_exception


class PayanaBigTable:

    @payana_generic_exception_handler
    def __init__(self, table_id):
        # fetch the table_id
        self.table_id = table_id

        self.client_config_path = bigtable_constants.bigtable_client_config_path

        # Create an instance for BigTable
        self.instance = bigtable_connect(self.client_config_path)

        # get a table instance
        self.table = bigtable_table_get(self.instance, self.table_id)

    @payana_generic_exception_handler
    def insert_column(self, bigtable_write_object):

        if self.table is not None:
            return bigtable_write(self.table, [bigtable_write_object])
        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def insert_columns(self, bigtable_write_objects):

        if self.table is not None:
            return bigtable_write(self.table, bigtable_write_objects)
        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def insert_columns_column_family(self, entity_id, column_family_obj):

        bigtable_write_objects = []

        for column_family_key, column_family_value_obj in column_family_obj.items():
            
            for column_quantifier_key, column_quantifier_value in column_family_value_obj.items():            

                bigtable_write_object = bigtable_write_object_wrapper(
                    entity_id, column_family_key, column_quantifier_key, column_quantifier_value)

                bigtable_write_objects.append(bigtable_write_object)

        if self.table is not None:
            return bigtable_write(self.table, bigtable_write_objects)
        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    @payana_generic_exception_handler
    def insert_columns_list_column_family(self, entity_id, column_family_obj):

        bigtable_write_objects = []

        for column_family_key, column_family_value_list in column_family_obj.items():
            
            for _, column_family_value_obj in enumerate(column_family_value_list):
            
                for column_quantifier_key, column_quantifier_value in column_family_value_obj.items():            

                    bigtable_write_object = bigtable_write_object_wrapper(
                        entity_id, column_family_key, column_quantifier_key, column_quantifier_value)

                    bigtable_write_objects.append(bigtable_write_object)

        if self.table is not None:
            return bigtable_write(self.table, bigtable_write_objects)
        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def get_row_dict(self, row_key, include_column_family=True):

        bigtable_row = self.get_row(row_key)

        bigtable_rows_dict = convert_big_table_rows_to_dict(
            bigtable_row, include_column_family=include_column_family)

        return bigtable_rows_dict

    @payana_generic_exception_handler
    def get_row(self, row_key):

        if self.table is not None:
            return bigtable_row_read(self.table, row_key)
        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # TO-DO : The calling function returns a PartialRowData object which might not have the full data. Fix the issue.
    @payana_generic_exception_handler
    def get_table_rows(self, row_keys, include_column_family=True):

        if self.table is not None:

            row_set = RowSet()

            for row_key in row_keys:
                row_set.add_row_key(row_key)

            bigtable_rows = bigtable_rows_read(self.table, row_set)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Get rows based on row key regex
    @payana_generic_exception_handler
    def get_table_rows_rowkey_regex(self, row_key_regex, include_column_family=True):

        if self.table is not None:

            row_key_regex_filter = bigtable_row_regex_read_filter(
                row_key_regex)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, row_key_regex_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    # Get rows based on row key regex
    @payana_generic_exception_handler
    def get_table_rows_rowkey_regex_column_qualifier_regex_chain(self, row_key_regex, column_qualifier_regex, include_column_family=True):

        if self.table is not None:

            row_key_regex_filter = bigtable_row_regex_read_filter(
                row_key_regex)
            
            column_qualifier_filter = bigtable_cells_column_qualifier_read_filter(
                column_qualifier_regex)
            
            combined_filter =  bigtable_cells_read_column_filter_chain([row_key_regex_filter, column_qualifier_filter])

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, combined_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # TO-DO : The calling function returns a PartialRowData object which might not have the full data. Fix the issue.
    @payana_generic_exception_handler
    def get_table_rows_range(self, start_row_key=None, end_row_key=None, include_column_family=True, start_inclusive=True, end_inclusive=True):

        if self.table is not None:

            row_set = RowSet()

            if start_row_key is None:
                row_set.add_row_range_from_keys(
                    end_key=end_row_key,
                    end_inclusive=end_inclusive)
            elif end_row_key is None:
                row_set.add_row_range_from_keys(
                    start_key=start_row_key,
                    start_inclusive=start_inclusive)
            else:
                row_set.add_row_range_from_keys(
                    start_key=start_row_key,
                    end_key=end_row_key,
                    start_inclusive=start_inclusive,
                    end_inclusive=end_inclusive)

            bigtable_rows = bigtable_rows_read(self.table, row_set)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Get cells from a row with matching column family

    @payana_generic_exception_handler
    def get_row_cells_column_family(self, row_key, column_family_id, include_column_family=True):

        if self.table is not None:

            column_family_filter = bigtable_cells_column_family_read_filter(
                column_family_id)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, column_family_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Get cells from a row with matching column qualifier
    @payana_generic_exception_handler
    def get_row_cells_column_qualifier(self, row_key, column_qualifier, include_column_family=True):

        if self.table is not None:

            column_qualifier_filter = bigtable_cells_column_qualifier_read_filter(
                column_qualifier)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, column_qualifier_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets the cells from a row with matching column family and column qualifier range
    @payana_generic_exception_handler
    def get_row_cells_column_range(self, row_key, column_family_id, column_qualifier_start_key=None, column_qualifier_end_key=None, include_column_family=True):

        if self.table is not None:

            column_range_filter = bigtable_cells_column_range_read_filter(
                column_family_id, column_qualifier_start_key, column_qualifier_end_key)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, column_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with matching column cell values
    @payana_generic_exception_handler
    def get_row_cells_value_range(self, row_key, value_start_key=None, value_end_key=None, include_column_family=True):

        if self.table is not None:

            value_range_filter = bigtable_cells_value_range_read_filter(
                value_start_key, value_end_key)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, value_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row across the table with matching timestamps
    @payana_generic_exception_handler
    def get_row_cells_timestamp_range(self, row_key, start_timestamp=None, end_timestamp=None, include_column_family=True):

        if self.table is not None:

            timestamp_range_filter = bigtable_cells_timestamp_range_read_filter(
                start_timestamp, end_timestamp)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, timestamp_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with cell count limit per row
    @payana_generic_exception_handler
    def get_row_cell_count_row_limit(self, row_key, row_cell_limit, include_column_family=True):

        if self.table is not None:

            row_cell_limit_filter = bigtable_cells_per_row_limit(
                row_cell_limit)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, row_cell_limit_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with cell count limit per column -- different edited versions of a column qualifier
    @payana_generic_exception_handler
    def get_row_cell_count_column_limit(self, row_key, column_cell_limit, include_column_family=True):

        if self.table is not None:

            column_cell_limit_filter = bigtable_cells_per_column_limit(
                column_cell_limit)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, column_cell_limit_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def get_row_cell_value_regex(self, row_key, value_regex, include_column_family=True):

        if self.table is not None:

            value_regex_filter = bigtable_cells_read_value_regex(value_regex)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, value_regex_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with the application of chained filters
    @payana_generic_exception_handler
    def get_row_cells_filter(self, row_key, filter, include_column_family=True):

        if self.table is not None:

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with the application of chained filters
    @payana_generic_exception_handler
    def get_row_cells_chain_filter(self, row_key, chain_filters, include_column_family=True):

        if self.table is not None:

            cells_chain_filter = bigtable_cells_read_column_filter_chain(
                chain_filters)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, cells_chain_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets cells from a row with the application of interleaved filters
    @payana_generic_exception_handler
    def get_row_cells_interleave_filter(self, row_key, interleave_filters, include_column_family=True):

        if self.table is not None:

            cells_interleave_filter = bigtable_cells_read_column_interleave_filter(
                interleave_filters)

            bigtable_rows = bigtable_row_column_filter_read(
                self.table, row_key, cells_interleave_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with matching column family
    @payana_generic_exception_handler
    def get_cells_column_family(self, column_family_id, include_column_family=True):

        if self.table is not None:

            column_family_filter = bigtable_cells_column_family_read_filter(
                column_family_id)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, column_family_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with matching column qualifier
    @payana_generic_exception_handler
    def get_cells_column_qualifier(self, column_qualifier, include_column_family=True):

        if self.table is not None:

            column_qualifier_filter = bigtable_cells_column_qualifier_read_filter(
                column_qualifier)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, column_qualifier_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with the application of the specified filter
    @payana_generic_exception_handler
    def get_cells_filter(self, filter, include_column_family=True):

        if self.table is not None:

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with the application of chained filters
    @payana_generic_exception_handler
    def get_cells_chain_filter(self, chain_filters, include_column_family=True):

        if self.table is not None:

            cells_chain_filter = bigtable_cells_read_column_filter_chain(
                chain_filters)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, cells_chain_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with the application of interleaved filters
    @payana_generic_exception_handler
    def get_cells_interleave_filter(self, interleave_filters, include_column_family=True):

        if self.table is not None:

            cells_interleave_filter = bigtable_cells_read_column_interleave_filter(
                interleave_filters)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, cells_interleave_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with matching column family and column qualifier range
    @payana_generic_exception_handler
    def get_cells_column_range(self, column_family_id, column_qualifier_start_key=None, column_qualifier_end_key=None, include_column_family=True):

        if self.table is not None:

            column_range_filter = bigtable_cells_column_range_read_filter(
                column_family_id, column_qualifier_start_key, column_qualifier_end_key)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, column_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with matching column cell values
    @payana_generic_exception_handler
    def get_cells_value_range(self, value_start_key=None, value_end_key=None, include_column_family=True):

        if self.table is not None:

            value_range_filter = bigtable_cells_value_range_read_filter(
                value_start_key, value_end_key)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, value_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def get_cells_value_regex(self, value_regex, include_column_family=True):

        if self.table is not None:

            value_regex_filter = bigtable_cells_read_value_regex(value_regex)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, value_regex_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    # Gets all cells across the table with matching timestamps

    @payana_generic_exception_handler
    def get_cells_timestamp_range(self, start_timestamp=None, end_timestamp=None, include_column_family=True):

        if self.table is not None:

            timestamp_range_filter = bigtable_cells_timestamp_range_read_filter(
                start_timestamp, end_timestamp)

            bigtable_rows = bigtable_cells_read_column_filter(
                self.table, timestamp_range_filter)

            bigtable_rows_dict = convert_big_table_rows_to_dict(
                bigtable_rows, include_column_family=include_column_family)

            return bigtable_rows_dict

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def delete_bigtable_row(self, bigtable_delete_row_object):

        if self.table is not None:

            row_key = bigtable_delete_row_object.row_key

            return bigtable_row_delete(self.table, row_key)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    @payana_generic_exception_handler
    def delete_bigtable_row_with_row_key(self, row_key):

        if self.table is not None:
            return bigtable_row_delete(self.table, row_key)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def delete_bigtable_rows(self, bigtable_delete_row_objects):

        if self.table is not None:

            row_keys = []

            for bigtable_delete_row_object in bigtable_delete_row_objects:

                row_key = bigtable_delete_row_object.row_key
                row_keys.append(row_key)
            # column_family_id = bigtable_read_column_value_object.column_family_id
            # column_qualifier_id = bigtable_read_column_value_object.column_qualifier_id

            return bigtable_rows_delete(self.table, row_keys)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def delete_bigtable_row_column(self, bigtable_delete_row_object):

        if self.table is not None:

            row_key = bigtable_delete_row_object.row_key
            column_family_id = bigtable_delete_row_object.column_family_id
            column_qualifier_id = bigtable_delete_row_object.column_qualifier_id

            return bigtable_row_cell_delete(self.table, row_key, column_family_id, column_qualifier_id)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    @payana_generic_exception_handler
    def delete_bigtable_row_column_family_object(self, bigtable_delete_row_objects):

        if self.table is not None:
            
            for bigtable_delete_row_object in bigtable_delete_row_objects:

                if not self.delete_bigtable_row_column_family_cells(bigtable_delete_row_object):
                    return False
                
            return True

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    @payana_generic_exception_handler
    def delete_bigtable_row_column_family_cells(self, bigtable_delete_row_object):

        if self.table is not None:

            row_key = bigtable_delete_row_object.row_key
            column_family_id = bigtable_delete_row_object.column_family_id

            return bigtable_column_family_cells_delete(self.table, row_key, column_family_id)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
        
    @payana_generic_exception_handler
    def delete_bigtable_row_column_family_list(self, bigtable_delete_row_objects):

        if self.table is not None:

            row_key = bigtable_delete_row_object.row_key
            column_family_id = bigtable_delete_row_object.column_family_id

            return bigtable_column_family_cells_delete(self.table, row_key, column_family_id)

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def delete_bigtable_row_columns(self, bigtable_delete_row_objects):

        if self.table is not None:

            for bigtable_delete_row_object in bigtable_delete_row_objects:
                
                column_qualifier_ids = []

                row_key = bigtable_delete_row_object.row_key

                column_family_id = bigtable_delete_row_object.column_family_id

                column_qualifier_id = bigtable_delete_row_object.column_qualifier_id
                column_qualifier_ids.append(column_qualifier_id)

                bigtable_row_cells_delete_status = bigtable_row_cells_delete(
                    self.table, row_key, column_family_id, column_qualifier_ids)
                
                if not bigtable_row_cells_delete_status:
                    return bigtable_row_cells_delete_status
                
            return bigtable_row_cells_delete_status

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)

    @payana_generic_exception_handler
    def delete_bigtable_row_column_list(self, row_key, bigtable_delete_row_objects_dict):

        if self.table is not None:

            for column_family_id, column_qualifier_id_list in bigtable_delete_row_objects_dict.items():

                bigtable_row_cells_delete_status = bigtable_row_cells_delete(
                    self.table, row_key, column_family_id, column_qualifier_id_list)
                
                if not bigtable_row_cells_delete_status:
                    return bigtable_row_cells_delete_status
                
            return bigtable_row_cells_delete_status

        else:
            print(payana_big_table_does_not_exist_exception)
            raise Exception(payana_big_table_exception)
