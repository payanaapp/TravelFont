from datetime import datetime
from os import truncate

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaCommentsTable import PayanaCommentsTable
from payana.payana_bl.common_utils.big_table_read_utils import get_big_table_rows_cell_count
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaCheckinTable import PayanaCheckinTable
from payana.payana_bl.bigtable_utils.PayanaLikesTable import PayanaLikesTable
from payana.payana_bl.bigtable_utils.PayanaTravelBuddyTable import PayanaTravelBuddyTable
from payana.payana_bl.bigtable_utils.PayanaPlaceIdMetadataTable import PayanaPlaceIdMetadataTable
from payana.payana_bl.bigtable_utils.PayanaNeighboringCitiesTable import PayanaNeighboringCitiesTable
from payana.payana_bl.bigtable_utils.PayanaStateTable import PayanaStateTable
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable
from payana.payana_bl.common_utils.bigtable_custom_filters import *
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

comment_obj = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

comment_obj_dup = {
    "comment_timestamp": "1234567890",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "13",
    "comment_id": "",
    "entity_id": "image_456"
}

comment_obj_dup_one = {
    "comment_timestamp": "1234567891",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "image_789"
}

comment_obj_dup_two = {
    "comment_timestamp": "1234567892",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "image_101112"
}

payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj.update_comment_bigtable()
entity_id = payana_comment_obj.entity_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj.get_row_dict("imagee", include_column_family=False))


payana_comment_obj_dup = PayanaCommentsTable(**comment_obj_dup)
payana_comment_obj_dup.update_comment_bigtable()
entity_id_dup = payana_comment_obj_dup.entity_id
payana_comment_read_obj_dup = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj_dup.get_row_dict("image_456", include_column_family=False))

payana_comment_obj_dup_one = PayanaCommentsTable(**comment_obj_dup_one)
payana_comment_obj_dup_one.update_comment_bigtable()
entity_id_dup_one = payana_comment_obj_dup_one.entity_id
payana_comment_read_obj_dup_one = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj_dup_one.get_row_dict("image_789", include_column_family=False))

payana_comment_obj_dup_two = PayanaCommentsTable(**comment_obj_dup_two)
payana_comment_obj_dup_two.update_comment_bigtable()
entity_id = payana_comment_obj_dup_two.entity_id
comment_id = payana_comment_obj_dup_two.comment_id
payana_comment_read_obj_dup_two = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj_dup_two.get_row_dict("image_101112", include_column_family=False))

row_keys = ["image_101112", "image_789", "image_456", "imagee"]

print("Fetching multiple row keys")

print(payana_comment_read_obj_dup_two.get_table_rows(row_keys))

print("Printing rows range")
print(payana_comment_read_obj_dup_two.get_table_rows_range("image_456", None, False))

print("Printing column family")
print(payana_comment_read_obj_dup_two.get_cells_column_family("payana_comments", False))

print("Printing column family of a specific row")
print(payana_comment_read_obj_dup_two.get_row_cells_column_family("image_789", "payana_comments", False))

comment_id_one = payana_comment_obj_dup_one.comment_id
comment_id_two = payana_comment_obj_dup_two.comment_id

print("Printing column qualifier")
print(payana_comment_read_obj_dup_two.get_cells_column_qualifier(comment_id_one, False))

print("Printing column qualifier cells of a specific row")
print(payana_comment_read_obj_dup_two.get_row_cells_column_qualifier("image_789", comment_id_one, False))

print("Printing column range")
print(payana_comment_read_obj_dup_two.get_cells_column_range("payana_comments", None, comment_id_one, False))

print("Printing column range for a specific row")
print(payana_comment_read_obj_dup_two.get_row_cells_column_range("image_789", "payana_comments", None, comment_id_one, False))


#### NOTE ::: Some issue with timestamp filtering. Doesn't behave as specified in the documentation - https://cloud.google.com/bigtable/docs/using-filters#timestamp-range
print("Testing column timestamp filter")
start_timestamp = datetime(2021, 12, 31)
end_timestamp = datetime.now()
print(payana_comment_read_obj_dup_two.get_cells_timestamp_range(None, end_timestamp, False))
print(payana_comment_read_obj_dup_two.get_cells_timestamp_range(start_timestamp, None, False))
print(payana_comment_read_obj_dup_two.get_cells_timestamp_range(start_timestamp, end_timestamp, False))

print("Testing column timestamp filter for a specific row")
print(payana_comment_read_obj_dup_two.get_row_cells_timestamp_range("image_789", None, end_timestamp, False))
print(payana_comment_read_obj_dup_two.get_row_cells_timestamp_range("image_789", start_timestamp, None, False))
print(payana_comment_read_obj_dup_two.get_row_cells_timestamp_range("image_789", start_timestamp, end_timestamp, False))

print("Testing for row key regex")
print(payana_comment_read_obj_dup_two.get_table_rows_rowkey_regex("image*", False))

print("Get 2 cells from row based cell limit per row")
print(payana_comment_read_obj_dup_one.get_row_cell_count_row_limit("image_789", 2))

print("Get 1 cell from row based cell limit per row")
print(payana_comment_read_obj_dup_one.get_row_cell_count_row_limit("image_789", 1))

print("Get 2 cells from row based cell limit per column -- different edited versions of a column qualifier")
print(payana_comment_read_obj_dup_one.get_row_cell_count_column_limit("image_789", 2))

print("Get 1 cell from row based cell limit per column -- different edited versions of a column qualifier")
print(payana_comment_read_obj_dup_one.get_row_cell_count_column_limit("image_789", 1))


comment_id = payana_comment_obj_dup_two.comment_id
comment_obj_dup_two["comment_id"] = comment_id

print("Value regex - cells from the whole table")
print(payana_comment_read_obj_dup_one.get_cells_value_regex(str(comment_obj_dup_two)+"*" , False))

print("Value regex - cells from a specific row")
print(payana_comment_read_obj_dup_one.get_row_cell_value_regex("image_101112", str(comment_obj_dup_two)+"*" , False))

print("Rows count of a table")
custom_filter = get_table_rows_count_filter()
custom_filter_rows = payana_comment_read_obj_dup_one.get_cells_filter(custom_filter, False)
print(custom_filter_rows)
custom_filter_rows_count = len(custom_filter_rows)
print("The number of rows:")
print(custom_filter_rows_count)

print("The number of cells:")
print(get_big_table_rows_cell_count(custom_filter_rows, False))

print("Verifying 1 row count")
custom_filter_row = payana_comment_read_obj_dup_one.get_row_cells_filter("image_101112", custom_filter, False)
custom_filter_row_count = len(custom_filter_row)
print(custom_filter_row_count)

print("Verifying row count for column family in the whole table")
column_family_custom_filter = get_column_family_count_filter("payana_comments")
custom_column_family_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(column_family_custom_filter, False)
print(custom_column_family_filters)
custom_column_family_filters_count = len(custom_column_family_filters)
print(custom_column_family_filters_count)

print("The number of cells from column family custom filter")
print(get_big_table_rows_cell_count(custom_column_family_filters, False))


print("Verifying column family row count and cell count for a single row")
custom_column_family_filter_row = payana_comment_read_obj_dup_one.get_row_cells_chain_filter("image_101112", column_family_custom_filter, False)
print(custom_column_family_filter_row)
custom_column_family_filter_row_count = len(custom_column_family_filter_row)
print("Row count: ")
print(custom_column_family_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(custom_column_family_filter_row, False))


print("Verifying row count for column qualifier in the whole table")
column_qualifier_custom_filter = get_column_qualifier_count_filter(comment_id_one)
custom_column_qualifier_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(column_qualifier_custom_filter, False)
print(custom_column_qualifier_filters)
custom_column_qualifier_filters_count = len(custom_column_qualifier_filters)
print(custom_column_qualifier_filters_count)

print("The number of cells from column qualifier custom filter")
print(get_big_table_rows_cell_count(custom_column_qualifier_filters, False))


print("Verifying column qualifier row count and cell count for a single row")
custom_column_qualifier_filter_row = payana_comment_read_obj_dup_one.get_row_cells_chain_filter("image_789", column_qualifier_custom_filter, False)
print(custom_column_qualifier_filter_row)
custom_column_qualifier_filter_row_count = len(custom_column_qualifier_filter_row)
print("Row count: ")
print(custom_column_qualifier_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(custom_column_qualifier_filter_row, False))


print("Verifying row count for column range in the whole table")
column_range_custom_filter = get_column_range_count_filter("payana_comments", comment_id_one, comment_id_two)
custom_column_range_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(column_range_custom_filter, False)
print(custom_column_range_filters)
custom_column_range_filters_count = len(custom_column_range_filters)
print(custom_column_range_filters_count)

print("The number of cells from column range custom filter")
print(get_big_table_rows_cell_count(custom_column_range_filters, False))


print("Verifying column range row count and cell count for a single row")
column_range_custom_filter_row = payana_comment_read_obj_dup_one.get_row_cells_chain_filter("image_789", column_range_custom_filter, False)
print(column_range_custom_filter_row)
column_range_custom_filter_row_count = len(column_range_custom_filter_row)
print("Row count: ")
print(column_range_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(column_range_custom_filter_row, False))



print("Verifying row count for timestamp range in the whole table")
timestamp_range_custom_filter = get_timestamp_range_count_filter(start_timestamp, end_timestamp)
custom_timestamp_range_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(timestamp_range_custom_filter, False)
print(custom_timestamp_range_filters)
custom_timestamp_range_filters_count = len(custom_timestamp_range_filters)
print(custom_timestamp_range_filters_count)

print("The number of cells from timestamp range custom filter")
print(get_big_table_rows_cell_count(custom_timestamp_range_filters, False))


print("Verifying timestamp range row count and cell count for a single row")
timestamp_range_custom_filter_row = payana_comment_read_obj_dup_one.get_row_cells_chain_filter("image_789", timestamp_range_custom_filter, False)
print(timestamp_range_custom_filter_row)
timestamp_range_custom_filter_row_count = len(timestamp_range_custom_filter_row)
print("Row count: ")
print(timestamp_range_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(timestamp_range_custom_filter_row, False))



print("Verifying row count for value regex in the whole table")
value_regex_custom_filter = get_value_regex_count_filter(str(comment_obj_dup_two)+"*")
custom_value_regex_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(value_regex_custom_filter, False)
print(custom_value_regex_filters)
custom_value_regex_filters_count = len(custom_value_regex_filters)
print(custom_value_regex_filters_count)

print("The number of cells from value regex range custom filter")
print(get_big_table_rows_cell_count(custom_value_regex_filters, False))


print("Verifying value regex row count and cell count for a single row")
value_regex_custom_filter_row = payana_comment_read_obj_dup_one.get_row_cells_chain_filter("image_101112", value_regex_custom_filter, False)
print(value_regex_custom_filter_row)
value_regex_custom_filter_row_count = len(value_regex_custom_filter_row)
print("Row count: ")
print(value_regex_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(value_regex_custom_filter_row, False))


print("Verifying row count for row regex in the whole table")
row_regex_custom_filter = get_row_regex_filter_count_filter("image*")
custom_row_regex_filters = payana_comment_read_obj_dup_one.get_cells_chain_filter(row_regex_custom_filter, False)
print(custom_row_regex_filters)
custom_row_regex_filters_count = len(custom_row_regex_filters)
print(custom_row_regex_filters_count)

print("The number of cells from row regex range custom filter")
print(get_big_table_rows_cell_count(custom_row_regex_filters, False))


itinerary_obj = {
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {"hiking": "1", "roadtrip": "1"},
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "itinerary_metadata": {
        "description": "Summer trip to Montana",
        "visit_timestamp": "123456789",
        "itinerary_id": "",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "SF"
    }
}

itinerary_obj_dup = {
    "excursion_id_list": {
        "1": "45678",
        "2": "56789",
        "3": "67891"
    },
    "activities_list": {"hiking": "1", "roadtrip": "1"},
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "itinerary_metadata": {
        "description": "Summer trip to Montana",
        "visit_timestamp": "123456789",
        "itinerary_id": "",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "SF"
    }
}

payana_itinerary_obj = PayanaItineraryTable(**itinerary_obj)
payana_itinerary_obj.update_itinerary_bigtable()
itinerary_id = payana_itinerary_obj.itinerary_id
payana_itinerary_table = bigtable_constants.payana_itinerary_table
payana_itinerary_read_obj = PayanaBigTable(payana_itinerary_table)
print(payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=False))

payana_itinerary_obj_dup = PayanaItineraryTable(**itinerary_obj_dup)
payana_itinerary_obj_dup.update_itinerary_bigtable()
itinerary_id_dup = payana_itinerary_obj_dup.itinerary_id
payana_itinerary_table = bigtable_constants.payana_itinerary_table
payana_itinerary_read_obj_dup = PayanaBigTable(payana_itinerary_table)
print(payana_itinerary_read_obj_dup.get_row_dict(itinerary_id_dup, include_column_family=False))

print("Printing column range")
print(payana_itinerary_read_obj_dup.get_cells_column_range("excursion_id_list", "1", "3", False))
print(payana_itinerary_read_obj_dup.get_cells_column_range("excursion_id_list", "1", "2", False))



print("Verifying row count for column range in the whole table")
column_range_custom_filter = get_column_range_count_filter("excursion_id_list", "1", "3")
custom_column_range_filters = payana_itinerary_read_obj_dup.get_cells_chain_filter(column_range_custom_filter, False)
print(custom_column_range_filters)
custom_column_range_filters_count = len(custom_column_range_filters)
print(custom_column_range_filters_count)

print("The number of cells from column range custom filter")
print(get_big_table_rows_cell_count(custom_column_range_filters, False))


print("Verifying column range row count and cell count for a single row")
column_range_custom_filter_row = payana_itinerary_read_obj_dup.get_row_cells_chain_filter(itinerary_id, column_range_custom_filter, False)
print(column_range_custom_filter_row)
column_range_custom_filter_row_count = len(column_range_custom_filter_row)
print("Row count: ")
print(column_range_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(column_range_custom_filter_row, False))




print("Printing Value range for the whole table")
print(payana_itinerary_read_obj.get_cells_value_range("12345", "45678", False))
print(payana_itinerary_read_obj.get_cells_value_range("12345", None, False))
print(payana_itinerary_read_obj.get_cells_value_range(None, "45678", False))


print("Printing Value range for the given row")
print(payana_itinerary_read_obj.get_row_cells_value_range(itinerary_id, "12345", "45678", False))
print(payana_itinerary_read_obj.get_row_cells_value_range(itinerary_id, "12345", None, False))
print(payana_itinerary_read_obj.get_row_cells_value_range(itinerary_id, None, "45678", False))



print("Verifying row count for value range in the whole table")
value_range_custom_filter = get_value_range_count_filter("12345", "45678")
custom_value_range_filters = payana_itinerary_read_obj.get_cells_chain_filter(value_range_custom_filter, False)
print(custom_value_range_filters)
custom_value_range_filters_count = len(custom_value_range_filters)
print(custom_value_range_filters_count)

print("The number of cells from value range custom filter")
print(get_big_table_rows_cell_count(custom_value_range_filters, False))


print("Verifying value range row count and cell count for a single row")
value_range_custom_filter_row = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, value_range_custom_filter, False)
print(value_range_custom_filter_row)
value_range_custom_filter_row_count = len(value_range_custom_filter_row)
print("Row count: ")
print(value_range_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(value_range_custom_filter_row, False))



print("Verifying row count for value range on a column family in the whole table")
value_range_column_family_custom_filter = get_value_range_on_column_family_filter("excursion_id_list", "12345", "45678", True)
custom_value_range_column_family_filters = payana_itinerary_read_obj.get_cells_chain_filter(value_range_column_family_custom_filter, False)
print(custom_value_range_column_family_filters)
custom_value_range_column_family_filters_count = len(custom_value_range_column_family_filters)
print(custom_value_range_column_family_filters_count)

print("The number of cells from value range on a column family custom filter")
print(get_big_table_rows_cell_count(custom_value_range_column_family_filters, False))


print("Verifying value range on a column family row count and cell count for a single row")
value_range_column_family_custom_filter_row = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, value_range_column_family_custom_filter, False)
print(value_range_column_family_custom_filter_row)
value_range_column_family_custom_filter_row_count = len(value_range_column_family_custom_filter_row)
print("Row count: ")
print(value_range_column_family_custom_filter_row_count)

print("Cell count: ")
print(get_big_table_rows_cell_count(value_range_column_family_custom_filter_row, False))


print("Verifying value range on a column family in the whole table")
value_range_column_family_custom_filter = get_value_range_on_column_family_filter("excursion_id_list", "12345", "45678")
custom_value_range_column_family_filters = payana_itinerary_read_obj.get_cells_chain_filter(value_range_column_family_custom_filter, False)
print(custom_value_range_column_family_filters)


print("Verifying value range row values on a column family a single row")
value_range_column_family_custom_filter_row = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, value_range_column_family_custom_filter, False)
print(value_range_column_family_custom_filter_row)


print("Verifying value regex filter on column family on the whole table")
value_regex_string = "12345*"
custom_value_regex_column_family_filter = get_value_regex_on_column_family_filter("excursion_id_list", value_regex_string)
custom_value_regex_column_family_filter_count = get_value_regex_on_column_family_filter("excursion_id_list", value_regex_string, True)

custom_value_regex_column_family_filters = payana_itinerary_read_obj.get_cells_chain_filter(custom_value_regex_column_family_filter)
print(custom_value_regex_column_family_filters)

custom_value_regex_column_family_filters_count = payana_itinerary_read_obj.get_cells_chain_filter(custom_value_regex_column_family_filter_count)
print(custom_value_regex_column_family_filters_count)

print("Verifying value regex filter on column family on the specific row")
custom_value_regex_column_family_row_filters = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, custom_value_regex_column_family_filter)
print(custom_value_regex_column_family_row_filters)

custom_value_regex_column_family_row_filters_count = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, custom_value_regex_column_family_filter_count)
print(custom_value_regex_column_family_row_filters_count)


print("Timestamp on a column family on the whole table")
start_timestamp = datetime(2021, 12, 31)
end_timestamp = datetime.now()

custom_timestamp_column_family_filter = get_timestamp_range_on_column_family_filter("excursion_id_list", start_timestamp, None)
custom_timestamp_column_family_filter_count = get_timestamp_range_on_column_family_filter("excursion_id_list", start_timestamp, None, True)

custom_timestamp_column_family_filter_cells = payana_itinerary_read_obj.get_cells_chain_filter(custom_timestamp_column_family_filter)
print(custom_timestamp_column_family_filter_cells)

custom_timestamp_column_family_filter_cells_count = payana_itinerary_read_obj.get_cells_chain_filter(custom_timestamp_column_family_filter_count)
print(custom_timestamp_column_family_filter_cells_count)

print("Timestamp on a column family on the specific row")
custom_timestamp_column_family_filter_row_filters = payana_itinerary_read_obj.get_row_cells_chain_filter(itinerary_id, custom_timestamp_column_family_filter)
print(custom_timestamp_column_family_filter_row_filters)


print("Verifying value range or a column family in the whole table -- interleave filter")
value_range_column_family_custom_filter = get_value_range_on_column_family_filter("excursion_id_list", "12345", "45678")
custom_value_range_column_family_filters = payana_itinerary_read_obj.get_cells_interleave_filter(value_range_column_family_custom_filter, False)
print(custom_value_range_column_family_filters)

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
