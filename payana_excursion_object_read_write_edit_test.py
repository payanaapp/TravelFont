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
 
excursion_obj = {
    "checkin_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "cities_checkin_id_list":{
        "1": "cupertino##california##usa",
        "2": "sunnyvale##california##usa",
        "3": "santaclara##california##usa"       
    },
    "image_id_list":{
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "34567",
        "3A": "23456",
        "3B": "34567" 
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "roadtrip": "6"},
    "excursion_metadata": {
        "excursion_id": "",
        "activity_guide": "False",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "description": "My excursion",
        "itinerary_id": "1234",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}

payana_excursion_obj = PayanaExcursionTable(**excursion_obj)
payana_excursion_obj_write_status = payana_excursion_obj.update_excursion_bigtable()

print("Payana excursion object write status: " + str(payana_excursion_obj_write_status))

excursion_id = payana_excursion_obj.excursion_id
payana_excursion_table = bigtable_constants.payana_excursion_table
payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)
excursion_obj_read = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
print(excursion_obj_read)

print("Addition of a new excursion object: " + str(excursion_obj_read != None))

# Change place ID
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_place_id = bigtable_constants.payana_excursion_id
new_place_id = "23456789"
excursion_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_place_id, new_place_id)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_place_id = excursion_obj_read_place_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_place_id]

print("Status of update place ID operation: " +
      str(new_place_id == updated_place_id))

# Change city
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_city = bigtable_constants.payana_excursion_id
new_city = "Seattle"
excursion_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_city, new_city)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_city = excursion_obj_read_place_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_city]

print("Status of update City operation: " +
      str(new_city == updated_city))

# Change state
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_state = bigtable_constants.payana_excursion_id
new_state = "Washington"
excursion_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_state, new_state)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_state = excursion_obj_read_place_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_state]

print("Status of update State operation: " +
      str(new_state == updated_state))

# Change Country
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_country = bigtable_constants.payana_excursion_id
new_country = "Canada"
excursion_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_country, new_country)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_country = excursion_obj_read_place_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_country]

print("Status of update Country operation: " +
      str(new_country == updated_country))

# Change place name
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_place_name = bigtable_constants.payana_excursion_place_name
new_place_name = "SC"
excursion_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_place_name, new_place_name)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_name_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_place_name = excursion_obj_read_place_name_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_place_name]

print("Status of update place name operation: " +
      str(new_place_name == updated_place_name))

# Change city
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_city = bigtable_constants.payana_excursion_city
new_city = "SJ"
excursion_table_city_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_excursion_city, new_city)
payana_excursion_read_obj.insert_column(excursion_table_city_write_object)
excursion_obj_read_city_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_city = excursion_obj_read_city_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_excursion_city]

print("Status of update city operation: " +
      str(new_city == updated_city))

# Change description
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_description = bigtable_constants.payana_excursion_column_family_description
new_description = "Totally enjoyed the beach!"
excursion_table_description_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_description, new_description)
payana_excursion_read_obj.insert_column(
    excursion_table_description_write_object)
excursion_obj_read_description_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_description = excursion_obj_read_description_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_description]

print("Status of update description operation: " +
      str(new_description == updated_description))

# Change transport mode
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_transport_mode = bigtable_constants.payana_excursion_transport_mode
new_transport_mode = "Cruise"
excursion_table_transport_mode_write_object = bigtable_write_object_wrapper(
    excursion_id, column_family_excursion_metadata, column_qualifier_transport_mode, new_transport_mode)
payana_excursion_read_obj.insert_column(
    excursion_table_transport_mode_write_object)
excursion_obj_read_transport_mode_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_transport_mode = excursion_obj_read_transport_mode_update[excursion_id][
    column_family_excursion_metadata][column_qualifier_transport_mode]

print("Status of update transport mode operation: " +
      str(new_transport_mode == updated_transport_mode))

# Add a new participant
column_family_participants_list = bigtable_constants.payana_excursion_column_family_participants_list
new_participant = {"pf_id_new": "1234567"}

for column_qualifier_new_participant, column_value_new_participant in new_participant.items():

    excursion_table_participant_write_object = bigtable_write_object_wrapper(
        excursion_id, column_family_participants_list, column_qualifier_new_participant, column_value_new_participant)
    payana_excursion_read_obj.insert_column(
        excursion_table_participant_write_object)
    excursion_obj_read_participant_mode_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)
    updated_participant_list = excursion_obj_read_participant_mode_update[
        excursion_id][column_family_participants_list]

    print("Status of update participant operation: " +
          str(column_qualifier_new_participant in updated_participant_list))
    print("Status of update participant value operation: " +
          str(column_value_new_participant in updated_participant_list[column_qualifier_new_participant]))

    # Delete the new participant added
    payana_excursion_read_obj.delete_bigtable_row_column(
        excursion_table_participant_write_object)
    excursion_obj_read_participant_mode_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)

    updated_participant_list = excursion_obj_read_participant_mode_update[
        excursion_id][column_family_participants_list]

    print("Status of update participant operation: " +
          str(column_qualifier_new_participant not in updated_participant_list))


# Add a check in ID
column_family_checkin_id_list = bigtable_constants.payana_excursion_column_family_checkin_id_list
new_checkin_id = {"4": "12345"}

for column_qualifier_new_checkin_id, column_value_new_checkin_id in new_checkin_id.items():

    excursion_table_checkin_id_write_object = bigtable_write_object_wrapper(
        excursion_id, column_family_checkin_id_list, column_qualifier_new_checkin_id, column_value_new_checkin_id)
    payana_excursion_read_obj.insert_column(
        excursion_table_checkin_id_write_object)
    excursion_obj_read_checkin_id_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)
    updated_checkin_id_list = excursion_obj_read_checkin_id_update[
        excursion_id][column_family_checkin_id_list]

    print("Status of update check in ID operation: " +
          str(column_qualifier_new_checkin_id in updated_checkin_id_list))
    print("Status of update check in ID value operation: " +
          str(column_value_new_checkin_id in updated_checkin_id_list[column_qualifier_new_checkin_id]))

    # Delete newly added checkin ID
    payana_excursion_read_obj.delete_bigtable_row_column(
        excursion_table_checkin_id_write_object)
    excursion_obj_read_checkin_id_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)

    updated_checkin_id_list = excursion_obj_read_checkin_id_update[
        excursion_id][column_family_checkin_id_list]

    print("Status of delete checkin ID operation: " +
          str(column_qualifier_new_checkin_id not in updated_checkin_id_list))


# Add an acivity
column_family_activity_list = bigtable_constants.payana_excursion_activities_list
new_activity = {"date": "3"}

for column_qualifier_activity, column_value_activity in new_activity.items():

    excursion_table_activity_write_object = bigtable_write_object_wrapper(
        excursion_id, column_family_activity_list, column_qualifier_activity, column_value_activity)
    payana_excursion_read_obj.insert_column(
        excursion_table_activity_write_object)
    excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)
    updated_activity_list = excursion_obj_read_activity_update[
        excursion_id][column_family_activity_list]

    print("Status of update activity operation: " +
          str(column_qualifier_activity in updated_activity_list))
    print("Status of update activity value operation: " +
          str(column_value_activity in updated_activity_list[column_qualifier_activity]))

    # Delete activity
    payana_excursion_read_obj.delete_bigtable_row_column(
        excursion_table_activity_write_object)
    excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)
    updated_activity_list = excursion_obj_read_activity_update[
        excursion_id][column_family_activity_list]

    print("Status of update activity operation: " +
          str(column_qualifier_activity not in updated_activity_list))

# Remove the whole excursion row
excursion_row_delete_object = bigtable_write_object_wrapper(
    excursion_id, "", "", "")
payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row(excursion_row_delete_object)

print("Payana excursion object delete status: " + str(payana_excursion_obj_delete_status))

excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(
    excursion_id, include_column_family=True)

print("Status of excursion obj delete row:" +
      str(len(excursion_obj_read_activity_update) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
