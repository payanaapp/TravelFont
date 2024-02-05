from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaAuthProfileTable import PayanaAuthProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable


client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_auth_information = bigtable_constants.payana_auth_information
payana_auth_mail_id = bigtable_constants.payana_auth_mail_id
payana_auth_profile_name = bigtable_constants.payana_auth_profile_name
payana_auth_profile_picture_id = bigtable_constants.payana_auth_profile_picture_id

auth_profile_obj = {
    payana_auth_information:
    {
        payana_auth_profile_name: "abkr",
        payana_auth_mail_id: "abkr@gmail.com",
        payana_auth_profile_picture_id: "123456789"
    }
}

payana_profile_obj = PayanaAuthProfileTable(**auth_profile_obj)
payana_profile_obj_write_status = payana_profile_obj.update_auth_profile_info_bigtable()

print("payana_profile_obj_write_status: " +
      str(payana_profile_obj_write_status))

mail_id = payana_profile_obj.mail_id
payana_auth_profile_table = bigtable_constants.payana_profile_auth_table
payana_profile_read_obj = PayanaBigTable(payana_auth_profile_table)
payana_profile_obj_read = payana_profile_read_obj.get_row_dict(
    mail_id, include_column_family=True)
print(payana_profile_obj_read)

print("Addition of a new profile object: " +
      str(payana_profile_obj_read != None))

# Change profile name
column_family_profile_table_metadata = payana_auth_information
new_profile_name = "abhinandankr"
profile_table_profile_name_write_object = bigtable_write_object_wrapper(
    mail_id, column_family_profile_table_metadata, payana_auth_profile_name, new_profile_name)
payana_profile_read_obj.insert_column(profile_table_profile_name_write_object)
profile_table_profile_name_update = payana_profile_read_obj.get_row_dict(
    mail_id, include_column_family=True)
updated_profile_name = profile_table_profile_name_update[mail_id][
    column_family_profile_table_metadata][payana_auth_profile_name]

print("Status of update profile name operation: " +
      str(new_profile_name == updated_profile_name))

# Add a new profile picture
new_profile_picture_id = "profile_picture_id_2"
profile_table_profile_picture_write_object = bigtable_write_object_wrapper(
    mail_id, column_family_profile_table_metadata, payana_auth_profile_picture_id, new_profile_picture_id)
payana_profile_read_obj.insert_column(
    profile_table_profile_picture_write_object)
profile_table_profile_picture_update = payana_profile_read_obj.get_row_dict(
    mail_id, include_column_family=True)
updated_profile_picture_obj = profile_table_profile_picture_update[mail_id][
    column_family_profile_table_metadata][payana_auth_profile_picture_id]

print("Status of update profile picture operation: " +
      str(updated_profile_picture_obj == new_profile_picture_id))

# Delete a profile picture
payana_profile_obj_delete_profile_picture_id_status = payana_profile_read_obj.delete_bigtable_row_column(
    profile_table_profile_picture_write_object)

print("payana_profile_obj_delete_profile_picture_id_status: " +
      str(payana_profile_obj_delete_profile_picture_id_status))

profile_table_profile_picture_delete = payana_profile_read_obj.get_row_dict(
    mail_id, include_column_family=True)

updated_profile_picture_obj = profile_table_profile_picture_delete[mail_id][
    column_family_profile_table_metadata]

print("Status of delete profile picture operation: " +
      str(payana_auth_profile_picture_id not in updated_profile_picture_obj))

# Remove the whole profile ID row
profile_row_delete_object = bigtable_write_object_wrapper(
    mail_id, "", "", "")
payana_profile_read_obj.delete_bigtable_row(profile_row_delete_object)

profile_obj_read_activity_update = payana_profile_read_obj.get_row_dict(
    mail_id, include_column_family=True)

print("Status of profile obj delete row:" +
      str(len(profile_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
