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

#add a neighboring city obj
neighboring_cities_obj = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "89.24"
    }
}

payana_neighboring_cities_obj = PayanaNeighboringCitiesTable(**neighboring_cities_obj)
payana_neighboring_cities_obj_write_status = payana_neighboring_cities_obj.update_neighboring_city_list_bigtable()

print("payana_neighboring_cities_obj_write_status: " + str(payana_neighboring_cities_obj_write_status))
payana_neighboring_cities_table = bigtable_constants.payana_neighboring_cities_table
city = payana_neighboring_cities_obj.city
payana_neighboring_cities_read_obj = PayanaBigTable(payana_neighboring_cities_table)
payana_neighboring_cities_response_obj = payana_neighboring_cities_read_obj.get_row_dict(city, include_column_family=True)

print("Payana Neighboring Cities Read Object: " + str(payana_neighboring_cities_response_obj is not None))

print(payana_neighboring_cities_response_obj)


from payana.payana_bl.bigtable_utils.PayanaGlobalCityTimestampItineraryTable import PayanaGlobalCityTimestampItineraryTable

global_city_itinerary_objects = [
    {
        "city": "cupertino##california##usa",
        "itinerary_id": {"123456789" : "12345"},
        "excursion_id": {"123456789" : "12345"},
        "checkin_id": {"123456789" : "12345"},
        "activity_guide_id": {"123456789" : "12345"},
        "activities": ["generic", "hiking", "romantic", "exotic"]
    },
    {
        "city": "sanjose##california##usa",
        "itinerary_id": {"123456789" : "12345"},
        "excursion_id": {"123456789" : "12345"},
        "checkin_id": {"123456789" : "12345"},
        "activity_guide_id": {"123456789" : "12345"},
        "activities": ["generic", "hiking", "romantic", "exotic"]
    }
]
            
payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value = bigtable_constants.payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value

for global_city_itinerary_obj in global_city_itinerary_objects:
    
    payana_global_city_itinerary_obj = PayanaGlobalCityTimestampItineraryTable(
        **global_city_itinerary_obj)

    payana_global_city_itinerary_obj_write_status = payana_global_city_itinerary_obj.update_global_city_itinerary_bigtable()
    print("payana_global_city_itinerary_obj write status: " +
        str(payana_global_city_itinerary_obj_write_status))

    payana_global_city_itinerary_table = bigtable_constants.payana_global_city_itinerary_table

    row_id = payana_global_city_itinerary_obj.row_id
    payana_global_city_itinerary_read_obj = PayanaBigTable(
        payana_global_city_itinerary_table)
    payana_global_city_itinerary_read_row_obj = payana_global_city_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)

    print("Status of add global city itinerary: " +
        str(payana_global_city_itinerary_read_row_obj is not None))

    print(payana_global_city_itinerary_read_row_obj)


from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable

excursion_obj = {
    "checkin_id_list": {
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
        "excursion_id": "123456789",
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
        "city": "SanFrancisco##California##USA",
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

print("Addition of a new excursion object: " + str(excursion_obj_read != None))
print(excursion_obj_read)