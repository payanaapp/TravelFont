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
from payana.payana_bl.bigtable_utils.PayanaUsersAutocompleteTable import PayanaUsersAutocompleteTable
from payana.payana_bl.bigtable_utils.PayanaStateTable import PayanaStateTable
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

# add a autocomplete user obj
autocomplete_users_obj = {
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457"
    }
}

payana_autocomplete_users_obj = PayanaUsersAutocompleteTable(
    **autocomplete_users_obj)
payana_autocomplete_users_obj_write_status = payana_autocomplete_users_obj.update_autocomplete_users_list_bigtable()

print("payana_autocomplete_users_obj_write_status: " +
      str(payana_autocomplete_users_obj_write_status))
payana_autocomplete_users_table = bigtable_constants.payana_users_autocomplete_table
city = payana_autocomplete_users_obj.city
payana_autocomplete_users_read_obj = PayanaBigTable(
    payana_autocomplete_users_table)
print(payana_autocomplete_users_read_obj.get_row_dict(
    city, include_column_family=True))

# Update the rating of an existing user
payana_users_autocomplete_column_family = bigtable_constants.payana_users_autocomplete_column_family
row_key = city
user_to_update = "user_1"
rating_to_update = "7346"
payana_autocomplete_user_write_object = bigtable_write_object_wrapper(
    row_key, payana_users_autocomplete_column_family, user_to_update, rating_to_update)
payana_autocomplete_users_read_obj.insert_column(
    payana_autocomplete_user_write_object)
payana_place_id_metadata_update = payana_autocomplete_users_read_obj.get_row_dict(
    row_key, include_column_family=True)
updated_rating = payana_place_id_metadata_update[row_key][
    payana_users_autocomplete_column_family][user_to_update]

print("Status of update user rating: " + str(updated_rating == rating_to_update))

# Add a new autocomplete user
user_to_add = "user_5"
rating_to_add = "79045"
payana_autocomplete_user_write_object = bigtable_write_object_wrapper(
    row_key, payana_users_autocomplete_column_family, user_to_add, rating_to_add)
payana_autocomplete_users_read_obj.insert_column(
    payana_autocomplete_user_write_object)
payana_place_id_metadata_update = payana_autocomplete_users_read_obj.get_row_dict(
    row_key, include_column_family=True)
added_user = payana_place_id_metadata_update[row_key][payana_users_autocomplete_column_family]

print("Status of add new user: " + str((user_to_add in added_user)
      and added_user[user_to_add] == rating_to_add))

# delete an autocomplete user
payana_autocomplete_user_delete_object = bigtable_write_object_wrapper(
    row_key, payana_users_autocomplete_column_family, user_to_add, "")
payana_autocomplete_users_obj_delete_status = payana_autocomplete_users_read_obj.delete_bigtable_row_column(
    payana_autocomplete_user_delete_object)

print("payana_autocomplete_users_obj_delete_status: " +
      str(payana_autocomplete_users_obj_delete_status))

payana_autocomplete_user_obj_delete = payana_autocomplete_users_read_obj.get_row_dict(
    row_key, include_column_family=True)
present_users = payana_autocomplete_user_obj_delete[row_key][payana_users_autocomplete_column_family]

print("Status of payana_autocomplete_user_obj_delete column: " +
      str(user_to_add not in present_users))

# Delete the whole row
payana_autocomplete_user_delete_object = bigtable_write_object_wrapper(
    row_key, "", "", "")
payana_autocomplete_cities_obj_delete_status = payana_autocomplete_users_read_obj.delete_bigtable_row(
    payana_autocomplete_user_delete_object)

print("payana_autocomplete_users_obj_delete_status: " +
      str(payana_autocomplete_users_obj_delete_status))

payana_autocomplete_user_obj_delete = payana_autocomplete_users_read_obj.get_row_dict(
    row_key, include_column_family=True)

print("Status of payana_autocomplete_user_obj_delete row: " +
      str(len(payana_autocomplete_user_obj_delete) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
