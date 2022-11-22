from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaCommentsTable import PayanaCommentsTable
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaCheckinTable import PayanaCheckinTable
from payana.payana_bl.bigtable_utils.PayanaLikesTable import PayanaLikesTable
from payana.payana_bl.bigtable_utils.PayanaTravelBuddyTable import PayanaTravelBuddyTable
from payana.payana_bl.bigtable_utils.PayanaPlaceIdMetadataTable import PayanaPlaceIdMetadataTable
from payana.payana_bl.bigtable_utils.PayanaNeighboringCitiesTable import PayanaNeighboringCitiesTable
from payana.payana_bl.bigtable_utils.PayanaStateTable import PayanaStateTable
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable
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
    "entity_id": "image_123"
}

comment_obj_dup = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "image_456"
}

comment_obj_dup_one = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "image_789"
}

comment_obj_dup_two = {
    "comment_timestamp": "123456789",
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
print(payana_comment_read_obj.get_row_dict("image_123", include_column_family=False))
#Deleting one row
print("Deleting first object")
payana_comment_bigtable_obj = bigtable_write_object_wrapper(entity_id, "", "", "")
payana_comment_read_obj.delete_bigtable_row(payana_comment_bigtable_obj)
#print(payana_comment_read_obj.get_row_dict("image_123", include_column_family=False))

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
#Deleting two rows
print("Deleting dup objects")
payana_comment_bigtable_obj_dup = bigtable_write_object_wrapper(entity_id_dup, "", "", "")
payana_comment_bigtable_obj_dup_one = bigtable_write_object_wrapper(entity_id_dup_one, "", "", "")

payana_comment_read_obj_dup_one.delete_bigtable_rows([payana_comment_bigtable_obj_dup, payana_comment_bigtable_obj_dup_one])
#print(payana_comment_read_obj_dup.get_row_dict("image_456", include_column_family=False))
#print(payana_comment_read_obj_dup_one.get_row_dict("image_789", include_column_family=False))

payana_comment_obj_dup_two = PayanaCommentsTable(**comment_obj_dup_two)
payana_comment_obj_dup_two.update_comment_bigtable()
entity_id = payana_comment_obj_dup_two.entity_id
comment_id = payana_comment_obj_dup_two.comment_id
payana_comment_read_obj_dup_two = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj_dup_two.get_row_dict("image_101112", include_column_family=False))
print("Deleting dup object two column")
#Deleting a column
payana_comment_bigtable_obj = bigtable_write_object_wrapper(entity_id, "payana_comments", comment_id, "")
payana_comment_read_obj_dup_two.delete_bigtable_row_column(payana_comment_bigtable_obj)
#print(payana_comment_read_obj_dup_two.get_row_dict("image_101112", include_column_family=False))

#deleting two columns
# print("Deleting dup object two columns")
# payana_comment_bigtable_obj_one = bigtable_write_object_wrapper(entity_id, "payana_comments", "comment", "")
# payana_comment_bigtable_obj_two = bigtable_write_object_wrapper(entity_id, "payana_comments", "profile_name", "")
# payana_comment_read_obj_dup_two.delete_bigtable_row_columns([payana_comment_bigtable_obj_one, payana_comment_bigtable_obj_two])
# print(payana_comment_read_obj_dup_two.get_row_dict("image_101112", include_column_family=False))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
