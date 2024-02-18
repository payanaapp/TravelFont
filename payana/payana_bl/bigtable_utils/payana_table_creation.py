#!/usr/bin/env python

"""Demonstrates how to create the tables for payana.
"""

import argparse
import datetime
import json
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_core.bigtable_utils.bigtable_table_create import bigtable_table_create
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler

# [START bigtable_imports]
from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END bigtable_imports]


@payana_generic_exception_handler
def payana_table_create(payana_table_creation_config_file, instance):

    # [START bigtable_create_table]
    # read the table names and column families
    with open(payana_table_creation_config_file) as json_data_file:
        payana_table_creation_dict = json.load(json_data_file)

    column_family_id = bigtable_constants.bigtable_schema_column_family_id
    max_versions = bigtable_constants.bigtable_schema_max_versions

    for table_id, table_details in payana_table_creation_dict.items():

        if column_family_id in table_details:
            table_column_family_id_list = table_details[column_family_id]
        else:
            raise Exception("Invalid table schema")

        if max_versions in table_details:
            table_max_version = table_details[max_versions]
        else:
            raise Exception("Invalid table schema")

        # create the table in bigtable cluster
        max_versions_rule = column_family.MaxVersionsGCRule(
            table_max_version)

        column_family_dict = {}

        for table_column_family_id in table_column_family_id_list:
            column_family_dict[table_column_family_id] = max_versions_rule
            
        print("Created table: " + table_id)

        bigtable_table_create(
            instance, table_id, column_family_dict)

    print("All tables created")

    # [END bigtable_create_table]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'payana_table_creation_config_file', help='List of all the tables to create for payana')
    parser.add_argument(
        'instance', help='BigTable instance to create the table')

    args = parser.parse_args()

    payana_table_create(args.payana_table_creation_config_file, args.instance)
