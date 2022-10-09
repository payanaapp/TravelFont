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

column_family_id = bigtable_constants.payana_country_table_column_family_city_list

country_obj = {
    "country": "usa",
    column_family_id: {
        "cupertino##california##usa" : "1.2", #rating is to sort the top cities
        "seattle##washington##usa" : "1.78"
        }
}

payana_country_obj = PayanaCountryTable(**country_obj)
payana_country_obj.update_country_bigtable()
payana_country_table = bigtable_constants.payana_place_country_table
country = payana_country_obj.country
payana_country_read_obj = PayanaBigTable(payana_country_table)
payana_country_obj_update = payana_country_read_obj.get_row_dict(country, include_column_family=True)

print("Status of write country obj: " + str(payana_country_obj_update is not None))

#Add another city
city_to_add = "phoenix##arizona##usa"
rating_to_add = "0.80"
payana_country_write_object = bigtable_write_object_wrapper(country, column_family_id, city_to_add, rating_to_add)
payana_country_read_obj.insert_column(payana_country_write_object)
payana_country_obj_update = payana_country_read_obj.get_row_dict(country, include_column_family=True)
added_city = payana_country_obj_update[country][column_family_id]

print("Status of add new city: " + str((city_to_add in added_city) and added_city[city_to_add] == rating_to_add))

#Update the score
city_to_update = "phoenix##arizona##usa"
rating_to_add = "0.85"
payana_country_write_object = bigtable_write_object_wrapper(country, column_family_id, city_to_add, rating_to_add)
payana_country_read_obj.insert_column(payana_country_write_object)
payana_country_obj_update = payana_country_read_obj.get_row_dict(country, include_column_family=True)
added_city = payana_country_obj_update[country][column_family_id]

print("Status of update city rating: " + str((city_to_add in added_city) and added_city[city_to_add] == rating_to_add))

#Delete a city
city_to_delete = "phoenix##arizona##usa"
payana_country_delete_object = bigtable_write_object_wrapper(country, column_family_id, city_to_delete, "")
payana_country_read_obj.delete_bigtable_row_column(payana_country_delete_object)

payana_country_obj_delete = payana_country_read_obj.get_row_dict(country, include_column_family=True)
deleted_city = payana_country_obj_delete[country][column_family_id]

print("Status of payana_country_obj_delete city column: " + str(city_to_delete not in deleted_city))

#Delete the whole row
payana_country_delete_object = bigtable_write_object_wrapper(country, column_family_id, "", "")
payana_country_read_obj.delete_bigtable_row(payana_country_delete_object)

payana_country_obj_delete = payana_country_read_obj.get_row_dict(country, include_column_family=True)

print("Status of payana_country_obj_delete city row: " + str(len(payana_country_obj_delete) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)