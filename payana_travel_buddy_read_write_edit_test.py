
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

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_travel_buddy_table_column_family_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_travel_buddy_list
payana_travel_buddy_table_column_family_favorite_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_favorite_travel_buddy_list
payana_travel_buddy_table_column_family_top_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_top_travel_buddy_list
payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list
payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list
payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list

payana_travel_buddy_table_column_family_profile_id = bigtable_constants.payana_travel_buddy_table_column_family_profile_id
payana_travel_buddy_table_column_family_travel_buddy_profile_id = bigtable_constants.payana_travel_buddy_table_column_family_travel_buddy_profile_id
payana_travel_buddy_table_column_family_global_influencer = bigtable_constants.payana_travel_buddy_table_column_family_global_influencer
payana_travel_buddy_table_column_family_favorite = bigtable_constants.payana_travel_buddy_table_column_family_favorite
payana_travel_buddy_table_column_family_sent_pending_request = bigtable_constants.payana_travel_buddy_table_column_family_sent_pending_request
payana_travel_buddy_table_column_family_received_pending_request = bigtable_constants.payana_travel_buddy_table_column_family_received_pending_request

travel_buddy_obj = {
    "profile_id": "1234567",
    "profile_name": "abkr",
    "travel_buddy_profile_name": "abhinandankr",    
    "travel_buddy_profile_id": "456789",
    "global_influencer": True, # flag for global influencer or not
    "favorite": True, # a flag to mark a travel buddy favorite
    "sent_pending_request": True, # adding into your pending approval requests for the requests that you sent
    "received_pending_request": True, # adding into your received approval requests for the requests that you sent
    "new_friend_request": True # marking whether a new friend request is sent out or not
}

#Adding a travel buddy
payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj)

payana_travel_buddy_obj_write_status = payana_travel_buddy_obj.update_travel_buddy_bigtable()
print("payana_travel_buddy_obj_write_status: " + str(payana_travel_buddy_obj_write_status))

payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
profile_id = payana_travel_buddy_obj.profile_id
travel_buddy_profile_id = payana_travel_buddy_obj.travel_buddy_profile_id
profile_name = payana_travel_buddy_obj.profile_name
travel_buddy_profile_name = payana_travel_buddy_obj.travel_buddy_profile_name
payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)

payana_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=True)
print(payana_profile_id_travel_buddy_obj)
print("Status of adding a profile ID into the travel_buddy profile ID: " + str(travel_buddy_profile_name in payana_profile_id_travel_buddy_obj[profile_id][payana_travel_buddy_table_column_family_travel_buddy_list]))

print("Status of marking a global influencer travel_buddy profile ID: " + str(travel_buddy_profile_name in payana_profile_id_travel_buddy_obj[profile_id][payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list]))

print("Status of marking a favorite travel_buddy profile ID: " + str(travel_buddy_profile_name in payana_profile_id_travel_buddy_obj[profile_id][payana_travel_buddy_table_column_family_favorite_travel_buddy_list]))

print("Status of adding travel_buddy into your pending sent requests: " + str(travel_buddy_profile_name in payana_profile_id_travel_buddy_obj[profile_id][payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list]))

payana_friend_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(travel_buddy_profile_id, include_column_family=True)
print(payana_friend_profile_id_travel_buddy_obj)
print("Status of adding a travel_buddy_profile_id profile ID into the profile ID: " + str(profile_name in payana_friend_profile_id_travel_buddy_obj[travel_buddy_profile_id][payana_travel_buddy_table_column_family_travel_buddy_list]))

print("Status of adding your request into travel buddy's received pending requests: " + str(profile_name in payana_friend_profile_id_travel_buddy_obj[travel_buddy_profile_id][payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list]))


#Adding another travel buddy
travel_buddy_obj_duplicate = {
    "profile_id": "1234567",
    "profile_name": "abkr",
    "travel_buddy_profile_id": "987654",
    "travel_buddy_profile_name": "abhinandankr1",
    "global_influencer": False, # flag for global influencer or not
    "favorite": False, # a flag to mark a travel buddy favorite
    "sent_pending_request": True, # adding into your pending approval requests for the requests that you sent
    "received_pending_request": False, # adding into your received approval requests for the requests that you sent
    "new_friend_request": True # marking whether a new friend request is sent out or not
}

#Adding another travel buddy
payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj_duplicate)

payana_travel_buddy_obj_write_status = payana_travel_buddy_obj.update_travel_buddy_bigtable()
print("payana_travel_buddy_obj_write_status: " + str(payana_travel_buddy_obj_write_status))

payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
profile_id_duplicate = payana_travel_buddy_obj.profile_id
travel_buddy_profile_id_duplicate = payana_travel_buddy_obj.travel_buddy_profile_id
profile_name_duplicate = payana_travel_buddy_obj.profile_name
travel_buddy_profile_name_duplicate = payana_travel_buddy_obj.travel_buddy_profile_name
payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)

payana_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(profile_id_duplicate, include_column_family=True)

print("Status of adding a profile ID into the travel_buddy profile ID: " + str(travel_buddy_profile_name_duplicate in payana_profile_id_travel_buddy_obj[profile_id_duplicate][payana_travel_buddy_table_column_family_travel_buddy_list]))

print("Status of marking a global influencer travel_buddy profile ID: " + str(travel_buddy_profile_name_duplicate not in payana_profile_id_travel_buddy_obj[profile_id_duplicate][payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list]))

print("Status of marking a favorite travel_buddy profile ID: " + str(travel_buddy_profile_name_duplicate not in payana_profile_id_travel_buddy_obj[profile_id_duplicate][payana_travel_buddy_table_column_family_favorite_travel_buddy_list]))

print("Status of adding travel_buddy into your pending sent requests: " + str(travel_buddy_profile_name_duplicate in payana_profile_id_travel_buddy_obj[profile_id_duplicate][payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list]))

payana_friend_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(travel_buddy_profile_id_duplicate, include_column_family=True)

print("Status of adding a travel_buddy_profile_id profile ID into the profile ID: " + str(profile_name_duplicate in payana_friend_profile_id_travel_buddy_obj[travel_buddy_profile_id_duplicate][payana_travel_buddy_table_column_family_travel_buddy_list]))

try:
    print("Status of adding your request into travel buddy's received pending requests: " + str(profile_name_duplicate not in payana_friend_profile_id_travel_buddy_obj[travel_buddy_profile_id_duplicate][payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list]))
except KeyError as exc:
    print("Status of remove friend profile travel buddy operation: " + str(True))
    
#Removing the duplicate obj travel buddy from a profile ID
payana_travel_buddy_delete_object = bigtable_write_object_wrapper(profile_id_duplicate, payana_travel_buddy_table_column_family_travel_buddy_list, travel_buddy_profile_name_duplicate, "")
payana_travel_buddy_friend_delete_object = bigtable_write_object_wrapper(travel_buddy_profile_id_duplicate, payana_travel_buddy_table_column_family_travel_buddy_list, profile_name_duplicate, "")

payana_travel_buddy_delete_object_status = payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_delete_object)
print("payana_travel_buddy_delete_object_status: " + str(payana_travel_buddy_delete_object_status))

payana_travel_buddy_friend_delete_object_status = payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_friend_delete_object)
print("payana_travel_buddy_friend_delete_object_status: " + str(payana_travel_buddy_friend_delete_object_status))

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id_duplicate, include_column_family=True)
payana_friend_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(travel_buddy_profile_id_duplicate, include_column_family=True)

updated_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id_duplicate][payana_travel_buddy_table_column_family_travel_buddy_list]

print("Status of remove travel buddy operation: " + str(travel_buddy_profile_name_duplicate not in updated_travel_buddy_list))

try:
    updated_friend_profile_travel_buddy_list = payana_friend_profile_id_travel_buddy_obj_update[travel_buddy_profile_id_duplicate][payana_travel_buddy_table_column_family_travel_buddy_list]
except KeyError as exc:
    print("Status of remove friend profile travel buddy operation: " + str(len(payana_friend_profile_id_travel_buddy_obj_update) == 0))
    
# Remove favorite status on a profile ID
payana_travel_buddy_delete_object = bigtable_write_object_wrapper(profile_id, payana_travel_buddy_table_column_family_favorite_travel_buddy_list, travel_buddy_profile_name, "")

payana_travel_buddy_delete_object_status = payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_delete_object)

print("payana_travel_buddy_delete_object_favorite_status: " + str(payana_travel_buddy_delete_object_status))

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=True)

try:
    updated_favorite_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id][payana_travel_buddy_table_column_family_favorite_travel_buddy_list]
except KeyError as exc:
    print("Status of remove favorite travel buddy operation: " + str(True))


# Remove profile ID from pending and received requests 
payana_travel_buddy_delete_object = bigtable_write_object_wrapper(profile_id, payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list, travel_buddy_profile_name, "")
payana_travel_buddy_friend_delete_object = bigtable_write_object_wrapper(travel_buddy_profile_id, payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list, profile_name, "")

payana_travel_buddy_delete_object_status = payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_delete_object)
print("payana_travel_buddy_delete_object_status: " + str(payana_travel_buddy_delete_object_status))

payana_travel_buddy_friend_delete_object_status = payana_travel_buddy_read_obj.delete_bigtable_row_column(payana_travel_buddy_friend_delete_object)
print("payana_travel_buddy_friend_delete_object_status: " + str(payana_travel_buddy_friend_delete_object_status))

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=True)
payana_friend_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(travel_buddy_profile_id, include_column_family=True)

updated_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id][payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list]

print("Status of remove travel buddy pending sent requests operation: " + str(travel_buddy_profile_name not in updated_travel_buddy_list))

try:
    updated_friend_profile_travel_buddy_list = payana_friend_profile_id_travel_buddy_obj_update[travel_buddy_profile_id]
except KeyError as exc:
    print("Status of remove travel buddy pending received requests operation: " + str(len(payana_friend_profile_id_travel_buddy_obj_update) == 0))


#Remove the whole row
payana_travel_buddy_write_object = bigtable_write_object_wrapper(profile_id, "", "", "")
payana_travel_buddy_read_obj.delete_bigtable_row(payana_travel_buddy_write_object)

payana_profile_id_travel_buddy_obj_update = payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=True)

try:
    updated_profile_travel_buddy_list = payana_profile_id_travel_buddy_obj_update[profile_id]
except KeyError as exc:
    print("Status of remove profile travel buddy operation: " + str(len(payana_profile_id_travel_buddy_obj_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)