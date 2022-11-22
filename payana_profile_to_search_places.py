from datetime import datetime

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
from payana.payana_bl.bigtable_utils.PayanaProfileToSearchPlacesTable import PayanaProfileToSearchPlacesTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_profile_to_search_places_activities_searched_cities_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_cities_activities
payana_profile_to_search_places_activities_searched_state_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_state_activities
payana_profile_to_search_places_activities_searched_place_id_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_place_id_activities
payana_profile_to_search_places_activities_searched_country_activities = bigtable_constants.payana_profile_to_search_places_activities_searched_country_activities

profile_to_search_places = {
    "profile_id": "123456789",
    "searched_cities_activities": {"seattle##washington##usa####hiking": "3456789012"},
    "searched_state_activities": {"washington##usa####hiking": "3456789012"},
    "searched_place_id_activities": {"12345##washington##usa####hiking": "3456789012"},
    "searched_country_activities": {"usa####hiking": "3456789012"}
}

profile_to_search_places_obj = PayanaProfileToSearchPlacesTable(
    **profile_to_search_places)
profile_to_search_places_obj_write_status = profile_to_search_places_obj.update_profile_search_places_bigtable()

print("profile_to_search_places_obj_write_status: " +
      str(profile_to_search_places_obj_write_status))

profile_id = profile_to_search_places_obj.profile_id
payana_profile_to_search_cities_activities_table = bigtable_constants.payana_profile_to_search_places_activities_table
payana_profile_to_search_cities_activities_read_obj = PayanaBigTable(
    payana_profile_to_search_cities_activities_table)
payana_profile_to_search_cities_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)
print(payana_profile_to_search_cities_activities_obj_read)

print("Addition of a new profile to search places object: " +
      str(payana_profile_to_search_cities_activities_obj_read != None))

# Update searched city activity column family
updated_searched_cities_activities = "seattle##washington##usa####hiking"
updated_timestamp = "123456789"

payana_profile_to_search_cities_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_cities_activities, updated_searched_cities_activities, updated_timestamp)

payana_profile_to_search_cities_activities_read_obj_update_status = payana_profile_to_search_cities_activities_read_obj.insert_column(
    payana_profile_to_search_cities_activities_write_object)

print("payana_profile_to_search_cities_activities_read_obj_update_status: " +
      str(payana_profile_to_search_cities_activities_read_obj_update_status))

payana_profile_to_search_cities_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched cities update operation: " + str(updated_timestamp ==
      payana_profile_to_search_cities_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_cities_activities][updated_searched_cities_activities]))

# Update searched state activity column family
updated_searched_state_activities = "washington##usa####hiking"
updated_timestamp = "123456789"

payana_profile_to_search_state_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_state_activities, updated_searched_state_activities, updated_timestamp)

payana_profile_to_search_state_activities_read_obj_update_status = payana_profile_to_search_cities_activities_read_obj.insert_column(
    payana_profile_to_search_cities_activities_write_object)

print("payana_profile_to_search_state_activities_read_obj_update_status: " +
      str(payana_profile_to_search_state_activities_read_obj_update_status))

payana_profile_to_search_state_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched state update operation: " + str(updated_timestamp ==
      payana_profile_to_search_state_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_state_activities][updated_searched_state_activities]))

# Update searched country activity column family
updated_searched_country_activities = "usa####hiking"
updated_timestamp = "123456789"

payana_profile_to_search_country_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_country_activities, updated_searched_country_activities, updated_timestamp)

payana_profile_to_search_country_activities_read_obj_update_status = payana_profile_to_search_cities_activities_read_obj.insert_column(
    payana_profile_to_search_country_activities_write_object)

print("payana_profile_to_search_country_activities_read_obj_update_status: " +
      str(payana_profile_to_search_country_activities_read_obj_update_status))

payana_profile_to_search_country_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched country update operation: " + str(updated_timestamp ==
      payana_profile_to_search_country_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_country_activities][updated_searched_country_activities]))

# Update searched place id activity column family
updated_searched_place_id_activities = "12345##washington##usa####hiking"
updated_timestamp = "123456789"

payana_profile_to_search_place_id_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_place_id_activities, updated_searched_place_id_activities, updated_timestamp)

payana_profile_to_search_place_id_activities_read_obj_update_status = payana_profile_to_search_cities_activities_read_obj.insert_column(
    payana_profile_to_search_place_id_activities_write_object)

print("payana_profile_to_search_place_id_activities_read_obj_update_status: " +
      str(payana_profile_to_search_place_id_activities_read_obj_update_status))

payana_profile_to_search_place_id_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched place_id update operation: " + str(updated_timestamp ==
      payana_profile_to_search_place_id_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_place_id_activities][updated_searched_place_id_activities]))

# Add new searched city activity column family
updated_searched_cities_activities = "seattle##washington##usa####romantic"
updated_timestamp = "123456789"

payana_profile_to_search_cities_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_cities_activities, updated_searched_cities_activities, updated_timestamp)

payana_profile_to_search_cities_activities_read_obj_update_status = payana_profile_to_search_cities_activities_read_obj.insert_column(
    payana_profile_to_search_cities_activities_write_object)

print("payana_profile_to_search_cities_activities_read_obj_update_status: " +
      str(payana_profile_to_search_cities_activities_read_obj_update_status))

payana_profile_to_search_cities_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched cities update operation: " + str(updated_timestamp ==
      payana_profile_to_search_cities_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_cities_activities][updated_searched_cities_activities]))

# Delete a new searched city activity column family
updated_searched_cities_activities = "seattle##washington##usa####romantic"
updated_timestamp = "123456789"

payana_profile_to_search_cities_activities_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_to_search_places_activities_searched_cities_activities, updated_searched_cities_activities, "")

payana_profile_to_search_cities_activities_read_obj_delete_status = payana_profile_to_search_cities_activities_read_obj.delete_bigtable_row_column(
    payana_profile_to_search_cities_activities_write_object)

print("payana_profile_to_search_cities_activities_read_obj_delete_status: " +
      str(payana_profile_to_search_cities_activities_read_obj_delete_status))

payana_profile_to_search_cities_activities_obj_read = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Payana searched cities delete operation: " + str(updated_searched_cities_activities not in
      payana_profile_to_search_cities_activities_obj_read[profile_id][payana_profile_to_search_places_activities_searched_cities_activities]))


# Remove the whole profile ID row
payana_profile_to_search_cities_activities_row_delete_object = bigtable_write_object_wrapper(
    profile_id, "", "", "")
payana_profile_to_search_cities_activities_read_obj.delete_bigtable_row(payana_profile_to_search_cities_activities_row_delete_object)

payana_profile_to_search_cities_activities_update = payana_profile_to_search_cities_activities_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Status of payana_profile_to_search_cities_activities_update delete row:" +
      str(len(payana_profile_to_search_cities_activities_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
