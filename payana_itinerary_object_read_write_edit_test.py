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

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

itinerary_obj = {
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {"hiking": "1.0", "roadtrip": "1.0"},
    "itinerary_metadata": {
        "description": "Abhinandan's SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": "",
        "itinerary_owner_profile_id": "1234567", 
        "place_id": "123456",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    }
}

payana_itinerary_obj = PayanaItineraryTable(**itinerary_obj)

payana_itinerary_obj_write_status = payana_itinerary_obj.update_itinerary_bigtable()
print("payana_itinerary_obj_write_status: " + str(payana_itinerary_obj_write_status))

itinerary_id = payana_itinerary_obj.itinerary_id
payana_itinerary_table = bigtable_constants.payana_itinerary_table
payana_itinerary_read_obj = PayanaBigTable(payana_itinerary_table)
itinerary_obj_read = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
print(itinerary_obj_read)

print("Addition of a new itinerary object: " + str(itinerary_obj_read != None))

# Change place ID
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_itinerary_place_id = bigtable_constants.payana_itinerary_id
new_place_id = "23456789"
itinerary_table_place_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_itinerary_place_id, new_place_id)
payana_itinerary_read_obj.insert_column(itinerary_table_place_write_object)
itinerary_obj_read_place_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_place_id = itinerary_obj_read_place_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_itinerary_place_id]

print("Status of update place ID operation: " + str(new_place_id == updated_place_id))

# Change place name
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_itinerary_place_name = bigtable_constants.payana_itinerary_place_name
new_place_name = "SC"
itinerary_table_place_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_itinerary_place_name, new_place_name)
payana_itinerary_read_obj.insert_column(itinerary_table_place_write_object)
itinerary_obj_read_place_name_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_place_name = itinerary_obj_read_place_name_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_itinerary_place_name]

print("Status of update place name operation: " + str(new_place_name == updated_place_name))

# Change city
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_itinerary_city = bigtable_constants.payana_itinerary_city
new_city = "SC"
itinerary_table_city_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_itinerary_city, new_city)

itinerary_table_city_write_object_status = payana_itinerary_read_obj.insert_column(itinerary_table_city_write_object)
print("itinerary_table_city_write_object_status: " + str(itinerary_table_city_write_object_status))

itinerary_obj_read_city_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_city = itinerary_obj_read_city_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_itinerary_city]

print("Status of update city operation: " + str(new_city == updated_city))

# Change state
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_itinerary_state = bigtable_constants.payana_itinerary_state
new_state = "SC"
itinerary_table_state_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_itinerary_state, new_state)

itinerary_table_state_write_object_status = payana_itinerary_read_obj.insert_column(itinerary_table_state_write_object)
print("itinerary_table_state_write_object_status: " + str(itinerary_table_state_write_object_status))

itinerary_obj_read_state_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_state = itinerary_obj_read_state_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_itinerary_state]

print("Status of update state operation: " + str(new_state == updated_state))

# Change country
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_itinerary_country = bigtable_constants.payana_itinerary_country
new_country = "SC"
itinerary_table_country_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_itinerary_country, new_country)

itinerary_table_country_write_object_status = payana_itinerary_read_obj.insert_column(itinerary_table_country_write_object)
print("itinerary_table_country_write_object_status: " + str(itinerary_table_country_write_object_status))

itinerary_obj_read_country_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_country = itinerary_obj_read_country_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_itinerary_country]

print("Status of update place name operation: " + str(new_country == updated_country))

# Change description
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_description = bigtable_constants.payana_itinerary_column_family_description
new_description = "Totally enjoyed the beach!"
itinerary_table_description_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_description, new_description)
payana_itinerary_read_obj.insert_column(itinerary_table_description_write_object)
itinerary_obj_read_description_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_description = itinerary_obj_read_description_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_description]

print("Status of update description operation: " + str(new_description == updated_description))

# Change visit_timestamp
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_visit_timestamp = bigtable_constants.payana_itinerary_column_family_visit_timestamp
new_visit_timestamp = "678912345"
itinerary_table_visit_timestamp_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_visit_timestamp, new_visit_timestamp)
itinerary_table_visit_timestamp_write_object_status = payana_itinerary_read_obj.insert_column(itinerary_table_visit_timestamp_write_object)
print("itinerary_table_visit_timestamp_write_object_status: " + str(itinerary_table_visit_timestamp_write_object_status))

itinerary_obj_read_visit_timestamp_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_visit_timestamp = itinerary_obj_read_visit_timestamp_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_visit_timestamp]

print("Status of update visit_timestamp operation: " + str(new_visit_timestamp == updated_visit_timestamp))

# Change last_updated_timestamp
column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
column_qualifier_last_updated_timestamp = bigtable_constants.payana_itinerary_column_family_last_updated_timestamp
new_last_updated_timestamp = "1788678912345"
itinerary_table_last_updated_timestamp_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_itinerary_metadata, column_qualifier_last_updated_timestamp, new_last_updated_timestamp)
itinerary_table_last_updated_timestamp_write_object_status = payana_itinerary_read_obj.insert_column(itinerary_table_last_updated_timestamp_write_object)
print("itinerary_table_last_updated_timestamp_write_object_status: " + str(itinerary_table_last_updated_timestamp_write_object_status))

itinerary_obj_read_visit_timestamp_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
updated_visit_timestamp = itinerary_obj_read_visit_timestamp_update[itinerary_id][column_family_itinerary_metadata][column_qualifier_visit_timestamp]

#Add an excursion ID -- no use case to call as an API end point. For debugging or backfilling purpose
column_family_excursion_id_list = bigtable_constants.payana_itinerary_column_family_excursion_id_list
new_excursion_id = {"4" : "12345"}

for column_qualifier_new_excursion_id, column_value_new_excursion_id in new_excursion_id.items():

    itinerary_table_excursion_id_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_excursion_id_list, column_qualifier_new_excursion_id, column_value_new_excursion_id)
    payana_itinerary_read_obj.insert_column(itinerary_table_excursion_id_write_object)
    itinerary_obj_read_excursion_id_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
    updated_excursion_id_list = itinerary_obj_read_excursion_id_update[itinerary_id][column_family_excursion_id_list]

    print("Status of update excursion ID operation: " + str(column_qualifier_new_excursion_id in updated_excursion_id_list))
    print("Status of update excursion ID value operation: " + str(column_value_new_excursion_id in updated_excursion_id_list[column_qualifier_new_excursion_id]))

    # Delete newly added excursion ID
    payana_itinerary_read_obj.delete_bigtable_row_column(itinerary_table_excursion_id_write_object)
    itinerary_obj_read_excursion_id_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)

    updated_excursion_id_list = itinerary_obj_read_excursion_id_update[itinerary_id][column_family_excursion_id_list]

    print("Status of delete excursion ID operation: " + str(column_qualifier_new_excursion_id not in updated_excursion_id_list))


#Add an acivity
column_family_activity_list = bigtable_constants.payana_excursion_activities_list
new_activity = {"date" : "3"}

for column_qualifier_activity, column_value_activity in new_activity.items():

    itinerary_table_activity_write_object = bigtable_write_object_wrapper(itinerary_id, column_family_activity_list, column_qualifier_activity, column_value_activity)
    payana_itinerary_read_obj.insert_column(itinerary_table_activity_write_object)
    itinerary_obj_read_activity_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
    updated_activity_list = itinerary_obj_read_activity_update[itinerary_id][column_family_activity_list]

    print("Status of update activity operation: " + str(column_qualifier_activity in updated_activity_list))
    print("Status of update activity value operation: " + str(column_value_activity in updated_activity_list[column_qualifier_activity]))

    # Delete activity
    payana_itinerary_read_obj.delete_bigtable_row_column(itinerary_table_activity_write_object)
    excursion_obj_read_activity_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)
    updated_activity_list = excursion_obj_read_activity_update[itinerary_id][column_family_activity_list]

    print("Status of update activity operation: " + str(column_qualifier_activity not in updated_activity_list))


#Remove the whole itinerary row
itinerary_row_delete_object = bigtable_write_object_wrapper(itinerary_id, "", "", "")
payana_itinerary_read_obj.delete_bigtable_row(itinerary_row_delete_object)

itinerary_obj_read_activity_update = payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True)

print("Status of itinerary obj delete row:" + str(len(itinerary_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)