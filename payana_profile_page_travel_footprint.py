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
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable
from payana.payana_bl.bigtable_utils.PayanaProfileTravelFootPrintTable import PayanaProfileTravelFootPrintTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_profile_page_travel_footprint_profile_id = bigtable_constants.payana_profile_page_travel_footprint_profile_id
payana_profile_page_travel_footprint_place_id = bigtable_constants.payana_profile_page_travel_footprint_place_id
payana_profile_page_travel_footprint_excursion_id = bigtable_constants.payana_profile_page_travel_footprint_excursion_id
payana_profile_page_travel_footprint_latitude = bigtable_constants.payana_profile_page_travel_footprint_latitude
payana_profile_page_travel_footprint_longitude = bigtable_constants.payana_profile_page_travel_footprint_longitude
payana_profile_page_travel_footprint_column_family = bigtable_constants.payana_profile_page_travel_footprint_column_family
payana_profile_travel_footprint_obj_list = bigtable_constants.payana_profile_travel_footprint_obj_list

profile_travel_footprint_obj = {
    "profile_id": "123456789",
    "travelfont_obj_list": [
        {
            "excursion_id": "678910",
            "latitude": "1.234",
            "longitude": "2.3456",
            "place_id": "12345"
        }
    ]
}

payana_profile_travel_footprint_obj = PayanaProfileTravelFootPrintTable(
    **profile_travel_footprint_obj)
payana_profile_travel_footprint_obj_write_status = payana_profile_travel_footprint_obj.update_profile_travel_footprint_bigtable()

print("payana_profile_travel_footprint_obj_write_status: " +
      str(payana_profile_travel_footprint_obj_write_status))

profile_id = payana_profile_travel_footprint_obj.profile_id
payana_profile_travel_footprint_table = bigtable_constants.payana_profile_travel_footprint_table
payana_profile_travel_footprint_read_obj = PayanaBigTable(
    payana_profile_travel_footprint_table)
payana_profile_travel_footprint_obj_read = payana_profile_travel_footprint_read_obj.get_row_dict(
    profile_id, include_column_family=True)
print(payana_profile_travel_footprint_obj_read)

print("Addition of a new travel footprint profile object: " +
      str(payana_profile_travel_footprint_obj_read != None))

# Change latitude
new_latitude = "56789.870"

place_id = profile_travel_footprint_obj[payana_profile_travel_footprint_obj_list][0]["place_id"]
excursion_id = profile_travel_footprint_obj[payana_profile_travel_footprint_obj_list][0]["excursion_id"]
latitude = profile_travel_footprint_obj[payana_profile_travel_footprint_obj_list][0]["latitude"]
longitude = profile_travel_footprint_obj[payana_profile_travel_footprint_obj_list][0]["longitude"]

payana_profile_page_travel_footprint_column_qualifier = "##".join(
    [str(place_id), str(excursion_id)])

payana_profile_page_travel_footprint_column_value = "##".join(
    [str(new_latitude), str(longitude)])

profile_table_profile_name_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_page_travel_footprint_column_family, payana_profile_page_travel_footprint_column_qualifier, payana_profile_page_travel_footprint_column_value)

payana_profile_travel_footprint_obj_update_status = payana_profile_travel_footprint_read_obj.insert_column(
    profile_table_profile_name_write_object)

print("payana_profile_travel_footprint_obj_update_status: " +
      str(payana_profile_travel_footprint_obj_update_status))

profile_table_profile_travel_footprint_update = payana_profile_travel_footprint_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_profile_travel_footprint_obj = profile_table_profile_travel_footprint_update[profile_id][
    payana_profile_page_travel_footprint_column_family][payana_profile_page_travel_footprint_column_qualifier]

updated_latitude, updated_longitude = updated_profile_travel_footprint_obj.split(
    "##")

print("Status of update profile travel footprint operation: " +
      str(new_latitude == updated_latitude))

# Add a new place obj
place_id = "919931"
excursion_id = "09876"
latitude = "890.01"
longitude = "6415.01"

payana_profile_page_travel_footprint_column_qualifier = "##".join(
    [str(place_id), str(excursion_id)])

payana_profile_page_travel_footprint_column_value = "##".join(
    [str(latitude), str(longitude)])

profile_table_profile_name_write_object_updated = bigtable_write_object_wrapper(
    profile_id, payana_profile_page_travel_footprint_column_family, payana_profile_page_travel_footprint_column_qualifier, payana_profile_page_travel_footprint_column_value)
payana_profile_travel_footprint_obj_update_status = payana_profile_travel_footprint_read_obj.insert_column(
    profile_table_profile_name_write_object_updated)

print("payana_profile_travel_footprint_obj_update_status: " +
      str(payana_profile_travel_footprint_obj_update_status))

profile_table_profile_travel_footprint_update = payana_profile_travel_footprint_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_profile_travel_footprint_obj = profile_table_profile_travel_footprint_update[profile_id][
    payana_profile_page_travel_footprint_column_family][payana_profile_page_travel_footprint_column_qualifier]

updated_latitude, updated_longitude = updated_profile_travel_footprint_obj.split(
    "##")

print("Status of update profile travel footprint operation: " +
      str(latitude == updated_latitude))

# Delete a travel footprint column
payana_profile_obj_delete_footprint_status = payana_profile_travel_footprint_read_obj.delete_bigtable_row_column(
    profile_table_profile_name_write_object_updated)

print("payana_profile_obj_delete_footprint_status: " +
      str(payana_profile_obj_delete_footprint_status))

profile_table_travel_footprint_delete = payana_profile_travel_footprint_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_profile_travel_footprint_obj = profile_table_travel_footprint_delete[profile_id][
    payana_profile_page_travel_footprint_column_family]

print("Status of delete travel footprint operation: " +
      str(payana_profile_page_travel_footprint_column_qualifier not in updated_profile_travel_footprint_obj))

# Remove the whole row
profile_travel_footprint_row_delete_object = bigtable_write_object_wrapper(
    profile_id, "", "", "")
profile_travel_footprint_row_delete_status = payana_profile_travel_footprint_read_obj.delete_bigtable_row(
    profile_travel_footprint_row_delete_object)

print("profile_travel_footprint_row_delete_status: " +
      str(profile_travel_footprint_row_delete_status))

profile_obj_read_travel_footprint_update = payana_profile_travel_footprint_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Status of profile travel footprint delete row:" +
      str(len(profile_obj_read_travel_footprint_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
