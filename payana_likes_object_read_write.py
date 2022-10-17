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
from payana.payana_bl.bigtable_utils.PayanaPersonalPlaceIdItineraryTable import PayanaPersonalPlaceIdItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCityItineraryTable import PayanaPersonalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable
from payana.payana_bl.bigtable_utils.PayanaEntityToCommentsTable import PayanaEntityToCommentsTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

# Add a like and read a like
likes_obj = {
    "payana_likes": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "entity_id": "12345"
}

payana_like_column_family = bigtable_constants.payana_likes_table_column_family
payana_likes_obj = PayanaLikesTable(**likes_obj)
payana_likes_obj.update_likes_bigtable()
payana_likes_table = bigtable_constants.payana_likes_table
like_object_id = payana_likes_obj.entity_id
payana_likes_read_obj = PayanaBigTable(payana_likes_table)
likes_obj = payana_likes_read_obj.get_row_dict(
    like_object_id, include_column_family=True)

participant_delete = "pf_id_1"
print("Status of like write operation: " +
      str(participant_delete in likes_obj[like_object_id][payana_like_column_family]))

print("Status of likes count operation: " +
      str(len(likes_obj[like_object_id][payana_like_column_family]) == 3))

# Remove a specific like
payana_like_bigtable_obj = bigtable_write_object_wrapper(
    like_object_id, payana_like_column_family, participant_delete, "")
payana_remove_like_status = payana_likes_read_obj.delete_bigtable_row_column(payana_like_bigtable_obj)

print("Payana like remove status: " + str(payana_remove_like_status))

likes_obj = payana_likes_read_obj.get_row_dict(
    like_object_id, include_column_family=True)

print("Status of like delete operation: " +
      str(participant_delete not in likes_obj[like_object_id][payana_like_column_family]))

# Remove the whole row
payana_like_bigtable_obj = bigtable_write_object_wrapper(
    like_object_id, "", "", "")
payana_remove_like_obj_status = payana_likes_read_obj.delete_bigtable_row(payana_like_bigtable_obj)

print("Payana like obj remove status: " + str(payana_remove_like_obj_status))

likes_obj = payana_likes_read_obj.get_row_dict(
    like_object_id, include_column_family=False)
print("Status of like row delete: " + str(len(likes_obj) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
