import re
from datetime import datetime
import json
from os import link

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
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
from payana.payana_bl.bigtable_utils.PayanaEntityToCommentsTable import PayanaEntityToCommentsTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_comments_table_entity_id = bigtable_constants.payana_comments_table_entity_id
payana_entity_to_comments_table_comment_id_list = bigtable_constants.payana_entity_to_comments_table_comment_id_list

# Add a comment
comment_obj = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

# Part one and Part two below are transactional operators
# If part one or two, the other should be reverted, to be handled in business logic layer


# Part one - Add the comment object into Comments table
payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj_write_status = payana_comment_obj.update_comment_bigtable()
print("Payana comment object write status: " + str(payana_comment_obj_write_status))

entity_id = payana_comment_obj.entity_id
comment_id = payana_comment_obj.comment_id
comment_id_one = comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(
    comment_id, include_column_family=False)

print("Comment added: " +
      str(payana_comment_obj is not None and len(payana_comment_obj) > 0))

# Part 2 - Update entity to comments table - only if above operation into comments table succeeds, else revert
if payana_comment_obj_write_status: # If comments table write operation above succeeds
    payana_entity_comments_table_comment_obj = {
        payana_comments_table_entity_id: entity_id,
        payana_entity_to_comments_table_comment_id_list: {comment_id: "1234567"}}

    payana_entity_to_comment_id_list_obj = PayanaEntityToCommentsTable(
        **payana_entity_comments_table_comment_obj)
    payana_entity_to_comment_id_list_obj_write_status = payana_entity_to_comment_id_list_obj.update_entity_to_comments_bigtable()
    print("Payana entity comment ID list write status: " + str(payana_entity_to_comment_id_list_obj_write_status))
    
    payana_entity_comment_table = bigtable_constants.payana_entity_to_comments_table
    payana_entity_comment_read_obj = PayanaBigTable(payana_entity_comment_table)
    payana_entity_comment_obj = payana_entity_comment_read_obj.get_row_dict(
        entity_id, include_column_family=False)

    print("Comment ID added to enity table: " +
          str(payana_entity_comment_obj is not None and len(payana_entity_comment_obj) > 0))

    if not payana_entity_to_comment_id_list_obj_write_status: #revert the above operation into comments table
        # Delete the comment row in the Comments table
        payana_comment_bigtable_obj = bigtable_write_object_wrapper(
            comment_id, "", "", "")
    
        payana_comment_read_obj.delete_bigtable_row(payana_comment_bigtable_obj)

        comment_obj = payana_comment_read_obj.get_row_dict(
            comment_id, include_column_family=False)

        print("Status of comment row delete as a part of transaction: " + str(len(comment_obj) == 0))

# Edit a comment
comment_obj = {
    "comment_timestamp": "678910234",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful\/ \"pic!\"",  # edge case with "" in description
    "likes_count": "13",
    "comment_id": comment_id,
    "entity_id": "imagee"  # Could be a checkin ID or image ID or itinerary ID
}

payana_comments_table_timestamp = bigtable_constants.payana_comments_table_timestamp
payana_comments_table_likes_count = bigtable_constants.payana_comments_table_likes_count
new_timestamp = comment_obj[payana_comments_table_timestamp]
new_likes_count = comment_obj[payana_comments_table_likes_count]

payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj_write_status = payana_comment_obj.update_comment_bigtable()

print("Payana comments edit operation status: " + str(payana_comment_obj_write_status))

entity_id = payana_comment_obj.entity_id
comment_id = payana_comment_obj.comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(
    comment_id, include_column_family=False)

print("Comment timestamp edited: " +
      str(payana_comment_obj[comment_id][payana_comments_table_timestamp] == new_timestamp))
print("Comment likes count edited: " +
      str(payana_comment_obj[comment_id][payana_comments_table_likes_count] == new_likes_count))

# Add another comment
comment_obj_dup = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

payana_comment_obj_dup = PayanaCommentsTable(**comment_obj_dup)
payana_new_comment_obj_write_status = payana_comment_obj_dup.update_comment_bigtable()

print("Payana new comment write operation: " + str(payana_new_comment_obj_write_status))

entity_id = payana_comment_obj_dup.entity_id
comment_id = payana_comment_obj_dup.comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(
    comment_id, include_column_family=False)

print("Status of new comment write: " +
      str(payana_comment_obj is not None and len(payana_comment_obj) > 0))

# Part 2 - Update entity to comments table - only if above operation into comments table succeeds, else revert
if payana_new_comment_obj_write_status: # If comments table write operation above succeeds
    payana_entity_comments_table_comment_obj = {
        payana_comments_table_entity_id: entity_id,
        payana_entity_to_comments_table_comment_id_list: {comment_id: "1234567"}}

    payana_entity_to_comment_id_list_obj = PayanaEntityToCommentsTable(
        **payana_entity_comments_table_comment_obj)
    payana_entity_to_comment_id_list_obj_write_status = payana_entity_to_comment_id_list_obj.update_entity_to_comments_bigtable()
    print("Payana entity comment ID list write status: " + str(payana_entity_to_comment_id_list_obj_write_status))
    
    payana_entity_comment_table = bigtable_constants.payana_entity_to_comments_table
    payana_entity_comment_read_obj = PayanaBigTable(payana_entity_comment_table)
    payana_entity_comment_obj = payana_entity_comment_read_obj.get_row_dict(
        entity_id, include_column_family=False)

    print("New Comment ID added to enity table: " +
      str(payana_entity_comment_obj is not None and len(payana_entity_comment_obj) > 0))

    if not payana_entity_to_comment_id_list_obj_write_status: #revert the above operation into comments table
        # Delete the comment row in the Comments table
        payana_comment_bigtable_obj = bigtable_write_object_wrapper(
            comment_id, "", "", "")
    
        payana_comment_read_obj.delete_bigtable_row(payana_comment_bigtable_obj)

        comment_obj = payana_comment_read_obj.get_row_dict(
            comment_id, include_column_family=False)

        print("Status of comment row delete as a part of transaction: " + str(len(comment_obj) == 0))

# Delete the comment row
payana_comment_bigtable_obj = bigtable_write_object_wrapper(
    comment_id, "", "", "")
payana_comment_delete_obj_status = payana_comment_read_obj.delete_bigtable_row(payana_comment_bigtable_obj)

print("Payana comment delete object status: " + str(payana_comment_delete_obj_status))

comment_obj = payana_comment_read_obj.get_row_dict(
    comment_id, include_column_family=False)

print("Status of comment row delete: " + str(len(comment_obj) == 0))

# Delete one comment ID in the entity to comment ID list table
payana_entity_comment_bigtable_obj = bigtable_write_object_wrapper(
    entity_id, bigtable_constants.payana_entity_to_comments_table_comment_id_list, comment_id_one, "")
payana_entity_comment_delete_column_status = payana_entity_comment_read_obj.delete_bigtable_row_column(
    payana_entity_comment_bigtable_obj)

print("Payana Entity to comments table delete column status: " + str(payana_entity_comment_delete_column_status))

entity_to_comment_obj = payana_entity_comment_read_obj.get_row_dict(
    entity_id, include_column_family=False)

print("Status of comment ID one delete in Entity to Comments table: " +
      str(comment_id_one not in entity_to_comment_obj))

# Delete the comment to entity table row
payana_entity_comment_bigtable_obj = bigtable_write_object_wrapper(
    entity_id, "", "", "")
payana_entity_comment_delete_obj_status = payana_entity_comment_read_obj.delete_bigtable_row(payana_entity_comment_bigtable_obj)

print("Payana Entity to comments table delete obj status: " + str(payana_entity_comment_delete_obj_status))

entity_to_comment_obj = payana_entity_comment_read_obj.get_row_dict(
    entity_id, include_column_family=False)

print("Status of comment row delete in Entity to Comments table: " + str(entity_to_comment_obj is None or len(entity_to_comment_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
