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
from payana.payana_bl.bigtable_utils.PayanaPersonalPlaceIdItineraryTable import PayanaPersonalPlaceIdItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCityItineraryTable import PayanaPersonalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

place_id_metadata_obj = {
    "place_id": "1234567",
    "city": "cupertino##california##usa",
    "state": "california##usa",
    "country": "usa",
    "zipcode": "95014"
}

payana_place_id_metadata_obj = PayanaPlaceIdMetadataTable(**place_id_metadata_obj)
payana_place_id_metadata_obj_write_status = payana_place_id_metadata_obj.update_place_metadata_bigtable()

print("payana_place_id_metadata_obj_write_status: " + str(payana_place_id_metadata_obj_write_status))

payana_place_id_metadata_table = bigtable_constants.payana_place_metadata_table
place_id = payana_place_id_metadata_obj.place_id
payana_place_id_metadata_read_obj = PayanaBigTable(payana_place_id_metadata_table)
payana_place_id_metadata_read_update = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=False)

print("Place ID metadata read operation: " + str(payana_place_id_metadata_read_update is not None))

payana_column_family_place_metadata_column_family_id = bigtable_constants.payana_column_family_place_metadata
quantifier_place_id = bigtable_constants.payana_quantifier_place_id
quantifier_city = bigtable_constants.payana_quantifier_city
quantifier_state = bigtable_constants.payana_quantifier_state
quantifier_country = bigtable_constants.payana_quantifier_country
quantifier_zipcode = bigtable_constants.payana_quantifier_zipcode

#Update city
old_city = payana_place_id_metadata_obj.city
new_city = "seattle##washington##usa"
payana_place_id_metadata_city_write_object = bigtable_write_object_wrapper(place_id, payana_column_family_place_metadata_column_family_id, quantifier_city, new_city)
payana_place_id_metadata_read_obj.insert_column(payana_place_id_metadata_city_write_object)
payana_place_id_metadata_update = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=True)
updated_city = payana_place_id_metadata_update[place_id][payana_column_family_place_metadata_column_family_id][quantifier_city]

print("Status of update city: " + str(updated_city == new_city))

#Update state
old_state = payana_place_id_metadata_obj.state
new_state = "washington##usa"
payana_place_id_metadata_state_write_object = bigtable_write_object_wrapper(place_id, payana_column_family_place_metadata_column_family_id, quantifier_state, new_state)
payana_place_id_metadata_read_obj.insert_column(payana_place_id_metadata_state_write_object)
payana_place_id_metadata_update = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=True)
updated_state = payana_place_id_metadata_update[place_id][payana_column_family_place_metadata_column_family_id][quantifier_state]

print("Status of update state: " + str(updated_state == new_state))

#Update country
old_country = payana_place_id_metadata_obj.country
new_country = "usa"
payana_place_id_metadata_country_write_object = bigtable_write_object_wrapper(place_id, payana_column_family_place_metadata_column_family_id, quantifier_country, new_country)
payana_place_id_metadata_read_obj.insert_column(payana_place_id_metadata_country_write_object)
payana_place_id_metadata_update = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=True)
updated_country = payana_place_id_metadata_update[place_id][payana_column_family_place_metadata_column_family_id][quantifier_country]

print("Status of update country: " + str(updated_country == new_country))

#Update zip code
old_zipcode = payana_place_id_metadata_obj.zipcode
new_zipcode = "95054"
payana_place_id_metadata_zipcode_write_object = bigtable_write_object_wrapper(place_id, payana_column_family_place_metadata_column_family_id, quantifier_zipcode, new_zipcode)
payana_place_id_metadata_read_obj.insert_column(payana_place_id_metadata_zipcode_write_object)
payana_place_id_metadata_update = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=True)
updated_zipcode = payana_place_id_metadata_update[place_id][payana_column_family_place_metadata_column_family_id][quantifier_zipcode]

print("Status of update zipcode: " + str(updated_zipcode == new_zipcode))

#delete a place ID metadata object
payana_place_id_metadata_row_delete_object = bigtable_write_object_wrapper(place_id, "", "", "")
payana_place_id_metadata_obj_delete_status = payana_place_id_metadata_read_obj.delete_bigtable_row(payana_place_id_metadata_row_delete_object)

print("payana_place_id_metadata_obj_delete_status: " + str(payana_place_id_metadata_obj_delete_status))

payana_place_id_metadata_delete = payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=True)

print("Status of payana_place_id_metadata delete row:" + str(len(payana_place_id_metadata_delete) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)