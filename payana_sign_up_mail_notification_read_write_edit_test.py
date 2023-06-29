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
from payana.payana_bl.bigtable_utils.PayanaCitiesAutocompleteTable import PayanaCitiesAutocompleteTable
from payana.payana_bl.bigtable_utils.PayanaStateTable import PayanaStateTable
from payana.payana_bl.bigtable_utils.PayanaSignUpMailNotificationTable import PayanaSignUpMailNotificationTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

# add an payana sign up mail notification object
sign_up_mail_notification_obj = {
    "profile_id": "123456789",
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}

payana_sign_up_mail_notification_obj = PayanaSignUpMailNotificationTable(**sign_up_mail_notification_obj)
payana_sign_up_mail_notification_obj_write_status = payana_sign_up_mail_notification_obj.update_mail_sign_up_notification_bigtable()

print("payana_sign_up_mail_notification_obj_write_status: " + str(payana_sign_up_mail_notification_obj_write_status))
payana_sign_up_mail_notification_table = bigtable_constants.payana_mail_sign_up_notification_table
profile_id = bigtable_constants.payana_sign_up_mail_id_list_profile_id
payana_sign_up_mail_id_list_column_family = bigtable_constants.payana_sign_up_mail_id_list_column_family
row_key = payana_sign_up_mail_notification_obj.profile_id
payana_sign_up_mail_notification_read_obj = PayanaBigTable(payana_sign_up_mail_notification_table)
print(payana_sign_up_mail_notification_read_obj.get_row_dict(row_key, include_column_family=True))

#Add a new mail ID
new_mail_id_to_add = "bharathi.hv1992@gmail.com"
new_timestamp = "12345678"
payana_sign_up_mail_notification_write_object = bigtable_write_object_wrapper(row_key, payana_sign_up_mail_id_list_column_family, new_mail_id_to_add, new_timestamp)
payana_sign_up_mail_notification_read_obj.insert_column(payana_sign_up_mail_notification_write_object)
payana_sign_up_mail_notification_update = payana_sign_up_mail_notification_read_obj.get_row_dict(row_key, include_column_family=True)
added_mail_id = payana_sign_up_mail_notification_update[row_key][payana_sign_up_mail_id_list_column_family]

print("Status of add new mail ID: " + str(new_mail_id_to_add in added_mail_id))

#delete a mail ID
payana_sign_up_mail_notification_delete_object = bigtable_write_object_wrapper(row_key, payana_sign_up_mail_id_list_column_family, new_mail_id_to_add, "")
payana_sign_up_mail_notification_obj_delete_status = payana_sign_up_mail_notification_read_obj.delete_bigtable_row_column(payana_sign_up_mail_notification_delete_object)

print("payana_sign_up_mail_notification_obj_delete_status: " + str(payana_sign_up_mail_notification_obj_delete_status))

payana_sign_up_mail_notification_obj_delete = payana_sign_up_mail_notification_read_obj.get_row_dict(row_key, include_column_family=True)
added_mail_id = payana_sign_up_mail_notification_obj_delete[row_key][payana_sign_up_mail_id_list_column_family]

print("Status of delete new mail ID: " + str(new_mail_id_to_add not in added_mail_id))

#Delete the whole row
payana_sign_up_mail_notification_delete_object = bigtable_write_object_wrapper(row_key, "", "", "")
payana_sign_up_mail_notification_obj_delete_status = payana_sign_up_mail_notification_read_obj.delete_bigtable_row(payana_sign_up_mail_notification_delete_object)

print("payana_sign_up_mail_notification_obj_delete_status: " + str(payana_sign_up_mail_notification_obj_delete_status))

payana_sign_up_mail_notification_obj_delete = payana_sign_up_mail_notification_read_obj.get_row_dict(row_key, include_column_family=True)

print("Status of payana_sign_up_mail_notification_delete row: " + str(len(payana_sign_up_mail_notification_obj_delete) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)