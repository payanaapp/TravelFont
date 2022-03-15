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

#add a neighboring city obj
neighboring_cities_obj = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}

payana_neighboring_cities_obj = PayanaNeighboringCitiesTable(**neighboring_cities_obj)
payana_neighboring_cities_obj.update_neighboring_city_list_bigtable()
payana_neighboring_cities_table = bigtable_constants.payana_neighboring_cities_table
city = payana_neighboring_cities_obj.city
payana_neighboring_cities_read_obj = PayanaBigTable(payana_neighboring_cities_table)
print(payana_neighboring_cities_read_obj.get_row_dict(city, include_column_family=True))

#Update the distance of an existing neighboring city
neighboring_city_list_column_family = bigtable_constants.payana_neighboring_cities_column_family
row_key = payana_neighboring_cities_obj.city
city_to_update = "seattle##washington##usa"
distance_to_update = "73.46"
payana_neighboring_city_write_object = bigtable_write_object_wrapper(row_key, neighboring_city_list_column_family, city_to_update, distance_to_update)
payana_neighboring_cities_read_obj.insert_column(payana_neighboring_city_write_object)
payana_place_id_metadata_update = payana_neighboring_cities_read_obj.get_row_dict(row_key, include_column_family=True)
updated_distance = payana_place_id_metadata_update[row_key][neighboring_city_list_column_family][city_to_update]

print("Status of update city: " + str(updated_distance == distance_to_update))

#Add a new neighboring city
neighboring_city_list_column_family = bigtable_constants.payana_neighboring_cities_column_family
row_key = payana_neighboring_cities_obj.city
city_to_add = "phoenix##arizona##usa"
distance_to_add = "79.80"
payana_neighboring_city_write_object = bigtable_write_object_wrapper(row_key, neighboring_city_list_column_family, city_to_add, distance_to_add)
payana_neighboring_cities_read_obj.insert_column(payana_neighboring_city_write_object)
payana_place_id_metadata_update = payana_neighboring_cities_read_obj.get_row_dict(row_key, include_column_family=True)
added_city = payana_place_id_metadata_update[row_key][neighboring_city_list_column_family]

print("Status of add new city: " + str((city_to_add in added_city) and added_city[city_to_add] == distance_to_add))

#delete a neighboring city
payana_neighboring_city_delete_object = bigtable_write_object_wrapper(row_key, neighboring_city_list_column_family, city_to_add, "")
payana_neighboring_cities_read_obj.delete_bigtable_row_column(payana_neighboring_city_delete_object)

payana_neighboring_city_obj_delete = payana_neighboring_cities_read_obj.get_row_dict(row_key, include_column_family=True)
deleted_city = payana_neighboring_city_obj_delete[row_key][neighboring_city_list_column_family]

print("Status of payana_neighboring_city_obj_delete column: " + str(city_to_add not in deleted_city))

#Delete the whole row
payana_neighboring_city_delete_object = bigtable_write_object_wrapper(row_key, "", "", "")
payana_neighboring_cities_read_obj.delete_bigtable_row(payana_neighboring_city_delete_object)

payana_neighboring_city_obj_delete = payana_neighboring_cities_read_obj.get_row_dict(row_key, include_column_family=True)

print("Status of payana_neighboring_city_obj_delete row: " + str(len(payana_neighboring_city_obj_delete) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)