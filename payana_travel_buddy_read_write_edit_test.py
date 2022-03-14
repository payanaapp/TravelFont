
from datetime import datetime
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

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
from payana.payana_bl.bigtable_utils.PayanaPersonalPlaceIdItineraryTable import PayanaPersonalPlaceIdItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCityItineraryTable import PayanaPersonalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

travel_buddy_obj = {
    "profile_id": "1234567",
    "friend_profile_id": "456789"
}

#Adding a travel buddy
payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj)
payana_travel_buddy_obj.update_travel_buddy_bigtable()
payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
profile_id = payana_travel_buddy_obj.profile_id
friend_profile_id = payana_travel_buddy_obj.friend_profile_id
payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)

payana_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=False)

print("Status of adding a friend profile ID into the profile ID: " + str(friend_profile_id in payana_profile_id_travel_buddy_obj[profile_id]))

payana_friend_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(friend_profile_id, include_column_family=False)

print("Status of adding a friend profile ID into the profile ID: " + str(profile_id in payana_friend_profile_id_travel_buddy_obj[friend_profile_id]))

#Adding another travel buddy
travel_buddy_obj_duplicate = {
    "profile_id": "1234567",
    "friend_profile_id": "67890"
}

payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj_duplicate)
payana_travel_buddy_obj.update_travel_buddy_bigtable()
payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
profile_id = payana_travel_buddy_obj.profile_id
friend_profile_id = payana_travel_buddy_obj.friend_profile_id
payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)

payana_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=False)

print("Status of adding second friend profile ID into the profile ID: " + str(friend_profile_id in payana_profile_id_travel_buddy_obj[profile_id]))

payana_friend_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(friend_profile_id, include_column_family=False)

print("Status of adding profile ID into second friend's profile ID: " + str(profile_id in payana_friend_profile_id_travel_buddy_obj[friend_profile_id]))

#Removing a travel buddy from a profile ID
travel_buddy_list_column_family_id = bigtable_constants.payana_travel_buddy_table_column_family
payana_travel_buddy_write_object = bigtable_write_object_wrapper(profile_id, travel_buddy_list_column_family_id, friend_profile_id, "")
payana_travel_buddy_friend_write_object = bigtable_write_object_wrapper(friend_profile_id, travel_buddy_list_column_family_id, profile_id, "")

payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_write_object)
payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_friend_write_object)

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=False)
payana_friend_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(friend_profile_id, include_column_family=False)

updated_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id]
print(payana_profile_id_travel_buddy_obj_update)

print("Status of remove travel buddy operation: " + str(friend_profile_id not in updated_travel_buddy_list))

try:
    updated_friend_profile_travel_buddy_list = payana_friend_profile_id_travel_buddy_obj_update[friend_profile_id]
except KeyError as exc:
    print("Status of remove friend profile travel buddy operation: " + str(len(payana_friend_profile_id_travel_buddy_obj_update) == 0))

#Remove the whole row
payana_travel_buddy_write_object = bigtable_write_object_wrapper(profile_id, "", "", "")
payana_travel_buddy_read_obj.delete_bigtable_row(payana_travel_buddy_write_object)

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=False)

try:
    updated_profile_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id]
except KeyError as exc:
    print("Status of remove profile travel buddy operation: " + str(len(payana_profile_id_travel_buddy_obj_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)