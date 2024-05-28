from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaActivityGuideThumbNailTable import PayanaActivityGuideThumbNailTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_activity_thumbnail = bigtable_constants.payana_activity_thumbnail
payana_activity_guide_thumbnail_table = bigtable_constants.payana_activity_guide_thumbnail_table
payana_activity_thumbnail_city = bigtable_constants.payana_activity_thumbnail_city

payana_activity_thumbnail_obj = {
    payana_activity_thumbnail: {
        "hiking": {
            "12345": "123456789" # image ID: timestamp
        },
        "romantic": {
            "12345": "123456789"
        }   
    },
    payana_activity_thumbnail_city: "cupertina##california##usa"
}

city = payana_activity_thumbnail_obj[payana_activity_thumbnail_city]

payana_activity_thumbnail_obj = PayanaActivityGuideThumbNailTable(**payana_activity_thumbnail_obj)
payana_activity_thumbnail_obj_write_status = payana_activity_thumbnail_obj.update_activity_guide_thumbnail_bigtable()

print("payana_activity_thumbnail_obj_write_status: " +
      str(payana_activity_thumbnail_obj_write_status))

activity_one = "_".join(["hiking", payana_activity_thumbnail])
activity_two = "_".join(["romantic", payana_activity_thumbnail])

payana_activity_thumbnail_obj = PayanaBigTable(payana_activity_guide_thumbnail_table)

payana_activity_thumbnail_obj_read = payana_activity_thumbnail_obj.get_row_dict(
    city, include_column_family=True)
print(payana_activity_thumbnail_obj_read)

print("Addition of a new activity thumbnail object: " +
      str(payana_activity_thumbnail_obj_read != None))

# Update a row by adding a column quantifier
new_activity_obj_image_id = "123456"
new_activity_obj_timestamp = "123456789"

payana_activity_thumbnail_write_object = bigtable_write_object_wrapper(
    city, activity_one, new_activity_obj_image_id, new_activity_obj_timestamp)
payana_activity_thumbnail_obj.insert_column(
    payana_activity_thumbnail_write_object)
payana_activity_thumbnail_update = payana_activity_thumbnail_obj.get_row_dict(
    city, include_column_family=True)
updated_payana_activity_thumbnail_obj = payana_activity_thumbnail_update[city][
    activity_one]

print("Status of add activity image ID operation: " +
      str(new_activity_obj_image_id in updated_payana_activity_thumbnail_obj))

# Delete an image ID
payana_activity_thumbnail_obj_delete_image_id_status = payana_activity_thumbnail_obj.delete_bigtable_row_column(
    payana_activity_thumbnail_write_object)

print("payana_activity_thumbnail_obj_delete_image_id_status: " +
      str(payana_activity_thumbnail_obj_delete_image_id_status))

payana_activity_thumbnail_update = payana_activity_thumbnail_obj.get_row_dict(
    city, include_column_family=True)
updated_payana_activity_thumbnail_obj = payana_activity_thumbnail_update[city][activity_one]

print("Status of delete activity image ID operation: " +
      str(new_activity_obj_image_id not in updated_payana_activity_thumbnail_obj))

# Remove the whole profile ID row
payana_activity_thumbnail_row_delete_object = bigtable_write_object_wrapper(
    city, "", "", "")
payana_activity_thumbnail_obj.delete_bigtable_row(payana_activity_thumbnail_row_delete_object)

payana_activity_thumbnail_obj_read_activity_update = payana_activity_thumbnail_obj.get_row_dict(
    city, include_column_family=True)

print("Status of thumbnail image delete row:" +
      str(len(payana_activity_thumbnail_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
