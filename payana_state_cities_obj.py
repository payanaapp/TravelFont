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

column_family_id = bigtable_constants.payana_state_table_column_family_city_list

state_obj = {
    "state": "california##usa",
    column_family_id: {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}

payana_state_obj = PayanaStateTable(**state_obj)
payana_state_obj_write_status = payana_state_obj.update_state_bigtable()
print("payana_state_obj_write_status: " + str(payana_state_obj_write_status))

payana_state_table = bigtable_constants.payana_place_state_table
state = payana_state_obj.state
payana_state_read_obj = PayanaBigTable(payana_state_table)
payana_state_update = payana_state_read_obj.get_row_dict(state, include_column_family=True)

#Add another city
city_to_add = "phoenix##arizona##usa"
rating_to_add = "0.80"
payana_state_write_object = bigtable_write_object_wrapper(state, column_family_id, city_to_add, rating_to_add)
payana_state_read_obj.insert_column(payana_state_write_object)
payana_state_obj_update = payana_state_read_obj.get_row_dict(state, include_column_family=True)
added_city = payana_state_obj_update[state][column_family_id]

print("Status of add new city: " + str((city_to_add in added_city) and added_city[city_to_add] == rating_to_add))

#Update the score
city_to_update = "phoenix##arizona##usa"
rating_to_add = "0.85"
payana_state_write_object = bigtable_write_object_wrapper(state, column_family_id, city_to_add, rating_to_add)
payana_state_read_obj.insert_column(payana_state_write_object)
payana_state_obj_update = payana_state_read_obj.get_row_dict(state, include_column_family=True)
added_city = payana_state_obj_update[state][column_family_id]

print("Status of update city rating: " + str((city_to_add in added_city) and added_city[city_to_add] == rating_to_add))

#Delete a city
city_to_delete = "phoenix##arizona##usa"
payana_state_delete_object = bigtable_write_object_wrapper(state, column_family_id, city_to_delete, "")
payana_state_read_obj.delete_bigtable_row_column(payana_state_delete_object)

payana_state_obj_delete = payana_state_read_obj.get_row_dict(state, include_column_family=True)
deleted_city = payana_state_obj_delete[state][column_family_id]

print("Status of payana_state_obj_delete city column: " + str(city_to_delete not in deleted_city))

#Delete the whole row
payana_state_delete_object = bigtable_write_object_wrapper(state, column_family_id, "", "")
payana_state_obj_delete_status = payana_state_read_obj.delete_bigtable_row(payana_state_delete_object)
print("payana_state_obj_delete_status: " + str(payana_state_obj_delete_status))

payana_state_obj_delete = payana_state_read_obj.get_row_dict(state, include_column_family=True)

print("Status of payana_state_obj_delete city row: " + str(len(payana_state_obj_delete) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)