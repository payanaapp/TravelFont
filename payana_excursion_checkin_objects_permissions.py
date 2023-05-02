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
from payana.payana_bl.bigtable_utils.PayanaExcursionCheckinPermissionTable import PayanaExcursionCheckinPermissionTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

excursion_permission_obj = {
    "entity_id": "123456789",
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "edit_participants_list": {"pf_id_2": "1234567", "pf_id_3": "1234567"},
    "admin": {"pf_id_1": "1234567"}
}

payana_excursion_checkin_permission_obj = PayanaExcursionCheckinPermissionTable(**excursion_permission_obj)
payana_excursion_checkin_permission_obj_write_status = payana_excursion_checkin_permission_obj.update_excursion_bigtable()

print("Payana excursion checkin permission object write status: " + str(payana_excursion_checkin_permission_obj_write_status))

excursion_id = payana_excursion_checkin_permission_obj.entity_id
payana_excursion_checkin_permission_table = bigtable_constants.payana_excursion_checkin_permission_table
payana_excursion_checkin_permission_read_obj = PayanaBigTable(payana_excursion_checkin_permission_table)
excursion_checkin_permission_obj_read = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
print(excursion_checkin_permission_obj_read)

print("Addition of a new excursion _checkin_permission object: " + str(excursion_checkin_permission_obj_read != None))

# Change admin
payana_excursion_checkin_permission_participants_column_family = bigtable_constants.payana_excursion_checkin_permission_participants_column_family
payana_excursion_checkin_permission_table_admin_column_family = bigtable_constants.payana_excursion_checkin_permission_table_admin_column_family

new_admin_profile_name = "pf_id_4"
new_admin_profile_id = "123456789"

excursion_checkin_permission_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, payana_excursion_checkin_permission_table_admin_column_family, new_admin_profile_name, new_admin_profile_id)

payana_excursion_checkin_permission_read_obj_write_status = payana_excursion_checkin_permission_read_obj.insert_column(excursion_checkin_permission_table_place_write_object)
print("payana_excursion_checkin_permission_read_obj_write_status status: " + str(payana_excursion_checkin_permission_read_obj_write_status))

excursion_checkin_permission_obj_read_place_update = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_excursion_checkin_permission_obj = excursion_checkin_permission_obj_read_place_update[excursion_id][
    payana_excursion_checkin_permission_table_admin_column_family]

print("Status of update admin operation: " +
      str(new_admin_profile_name in updated_excursion_checkin_permission_obj))

# Add participant
new_participant = "pf_id_9"
new_participant_id = "123456789"

excursion_checkin_permission_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, payana_excursion_checkin_permission_participants_column_family, new_participant, new_participant_id)

payana_excursion_checkin_permission_read_obj_write_status = payana_excursion_checkin_permission_read_obj.insert_column(excursion_checkin_permission_table_place_write_object)
print("payana_excursion_checkin_permission_read_obj_write_status status: " + str(payana_excursion_checkin_permission_read_obj_write_status))

excursion_checkin_permission_obj_read_place_update = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_excursion_checkin_permission_obj = excursion_checkin_permission_obj_read_place_update[excursion_id][
    payana_excursion_checkin_permission_participants_column_family]

print("Status of add participant operation: " +
      str(new_participant in updated_excursion_checkin_permission_obj))

# Delete participant
excursion_checkin_permission_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, payana_excursion_checkin_permission_participants_column_family, new_participant, "")

payana_excursion_checkin_permission_read_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column(excursion_checkin_permission_table_place_write_object)
print("payana_excursion_checkin_permission_read_obj_delete_status status: " + str(payana_excursion_checkin_permission_read_obj_delete_status))

excursion_checkin_permission_obj_read_place_update = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_excursion_checkin_permission_obj = excursion_checkin_permission_obj_read_place_update[excursion_id][
    payana_excursion_checkin_permission_participants_column_family]

print("Status of delete participant operation: " +
      str(new_participant not in updated_excursion_checkin_permission_obj))

# Delete admin
excursion_checkin_permission_table_place_write_object = bigtable_write_object_wrapper(
    excursion_id, payana_excursion_checkin_permission_table_admin_column_family, new_admin_profile_name, "")

payana_excursion_checkin_permission_read_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row_column(excursion_checkin_permission_table_place_write_object)
print("payana_excursion_checkin_permission_read_obj_delete_status status: " + str(payana_excursion_checkin_permission_read_obj_delete_status))

excursion_checkin_permission_obj_read_place_update = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)
updated_excursion_checkin_permission_obj = excursion_checkin_permission_obj_read_place_update[excursion_id][
    payana_excursion_checkin_permission_table_admin_column_family]

print("Status of delete admin operation: " +
      str(new_admin_profile_name not in updated_excursion_checkin_permission_obj))

# Remove the whole excursion row
excursion_row_delete_object = bigtable_write_object_wrapper(
    excursion_id, "", "", "")
payana_excursion_obj_delete_status = payana_excursion_checkin_permission_read_obj.delete_bigtable_row(excursion_row_delete_object)

print("Payana excursion object row delete status: " + str(payana_excursion_obj_delete_status))

excursion_obj_read_activity_update = payana_excursion_checkin_permission_read_obj.get_row_dict(
    excursion_id, include_column_family=True)

print("Status of excursion obj delete row:" +
      str(len(excursion_obj_read_activity_update) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
