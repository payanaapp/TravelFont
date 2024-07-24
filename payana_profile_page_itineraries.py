from datetime import datetime
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
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

profile_page_itinerary_obj = {
    "profile_id": "12345",
    "saved_itinerary_id_mapping": {"itinerary_name_one": "12345"},
    "saved_excursion_id_mapping": {"excursion_name_one": "12345"},
    "saved_activity_guide_id_mapping": {"activity_guide_name_one": "12345"},
    "created_itinerary_id_mapping": {"itinerary_name_one": "12345"},
    "created_activity_guide_id_mapping": {"activity_guide_name_one": "12345"},
    "created_excursion_id_mapping": {"excursion_name_one": "12345"},
    "activities": ["generic", "hiking", "romantic"]
}

payana_profile_page_itinerary_obj = PayanaProfilePageItineraryTable(
    **profile_page_itinerary_obj)
payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_obj.update_payana_profile_page_itinerary_bigtable()

print("payana_profile_page_itinerary_obj_write_status: " +
      str(payana_profile_page_itinerary_obj_write_status))

payana_profile_page_itinerary_table = bigtable_constants.payana_profile_page_itinerary_table
# We could use regular expression to exclude the year part while querying
row_id = payana_profile_page_itinerary_obj.row_id
payana_profile_page_itinerary_read_obj = PayanaBigTable(
    payana_profile_page_itinerary_table)
payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print(payana_profile_page_itinerary_read_row_obj)

print("Status of add payana_profile_page itinerary: " +
      str(payana_profile_page_itinerary_read_row_obj is not None))

activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family

# generic activity write objects
payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_itinerary_id_mapping_quantifier_value
payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value
payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value
payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value

saved_itinerary_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value])

saved_excursion_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value])

created_itinerary_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value])

created_excursion_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value])

# Add another itinerary ID, excursion ID into created, saved itinerary/excursio ID list
itinerary_new = ["67891"]
excursion_new = ["78910"]

current_ts = str(int(datetime.utcnow().timestamp()))

for itinerary_id in itinerary_new:
    payana_profile_page_itinerary_table_saved_write_object = bigtable_write_object_wrapper(
        row_id, saved_itinerary_id_list_activity_generic_column_family_id, current_ts, itinerary_id)
    payana_profile_page_saved_itinerary_obj_write_status = payana_profile_page_itinerary_read_obj.insert_column(
        payana_profile_page_itinerary_table_saved_write_object)
    print("payana_profile_page_saved_itinerary_obj_write_status: " +
          str(payana_profile_page_saved_itinerary_obj_write_status))
    payana_profile_page_saved_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_itinerary_id = payana_profile_page_saved_itinerary_read_row_obj[row_id][
        saved_itinerary_id_list_activity_generic_column_family_id][current_ts]

    print("Status of itinerary ID update for saved itinerary ID list: " +
          str(itinerary_id == updated_itinerary_id))

for itinerary_id in itinerary_new:
    payana_profile_page_itinerary_table_created_write_object = bigtable_write_object_wrapper(
        row_id, created_itinerary_id_list_activity_generic_column_family_id, current_ts, itinerary_id)
    payana_profile_page_created_itinerary_obj_write_status = payana_profile_page_itinerary_read_obj.insert_column(
        payana_profile_page_itinerary_table_created_write_object)
    print("payana_profile_page_created_itinerary_obj_write_status: " +
          str(payana_profile_page_created_itinerary_obj_write_status))
    payana_profile_page_created_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_itinerary_id = payana_profile_page_created_itinerary_read_row_obj[row_id][
        saved_itinerary_id_list_activity_generic_column_family_id][current_ts]

    print("Status of itinerary ID update for created itinerary ID list: " +
          str(itinerary_id == updated_itinerary_id))

for excursion_id in excursion_new:
    payana_profile_page_excursion_table_saved_write_object = bigtable_write_object_wrapper(
        row_id, saved_excursion_id_list_activity_generic_column_family_id, current_ts, excursion_id)
    payana_profile_page_saved_excursion_obj_write_status = payana_profile_page_itinerary_read_obj.insert_column(
        payana_profile_page_excursion_table_saved_write_object)
    print("payana_profile_page_saved_excursion_obj_write_status: " +
          str(payana_profile_page_saved_excursion_obj_write_status))
    payana_profile_page_saved_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_excursion_id = payana_profile_page_saved_excursion_read_row_obj[row_id][
        saved_excursion_id_list_activity_generic_column_family_id][current_ts]

    print("Status of excursion ID update for saved excursion ID list: " +
          str(excursion_id == updated_excursion_id))

for excursion_id in excursion_new:
    payana_profile_page_excursion_table_created_write_object = bigtable_write_object_wrapper(
        row_id, created_excursion_id_list_activity_generic_column_family_id, current_ts, excursion_id)
    payana_profile_page_created_excursion_obj_write_status = payana_profile_page_itinerary_read_obj.insert_column(
        payana_profile_page_excursion_table_created_write_object)
    print("payana_profile_page_created_excursion_obj_write_status: " +
          str(payana_profile_page_created_excursion_obj_write_status))
    payana_profile_page_created_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_excursion_id = payana_profile_page_created_excursion_read_row_obj[row_id][
        saved_excursion_id_list_activity_generic_column_family_id][current_ts]

    print("Status of excursion ID update for created excursion ID list: " +
          str(excursion_id == updated_excursion_id))

# Add another itinerary ID, excursion ID with activities
itinerary_update = ["34567"]
excursion_update = ["45678"]
activity_update = ["hiking", "romantic"]

current_ts_new = str(int(datetime.utcnow().timestamp()))

# itinerary ID list activity write
for itinerary_id in itinerary_update:
    for activity in activity_update:
        saved_itinerary_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value])

        created_itinerary_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value])

        # insert into saved itinerary ID list
        payana_profile_page_saved_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, saved_itinerary_id_list_activity_column_family_id, current_ts_new, itinerary_id)

        payana_profile_page_saved_itinerary_table_write_object_status = payana_profile_page_itinerary_read_obj.insert_column(
            payana_profile_page_saved_itinerary_table_write_object)

        print("payana_profile_page_saved_itinerary_table_write_object_status: " +
              str(payana_profile_page_saved_itinerary_table_write_object_status))

        payana_profile_page_saved_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)

        updated_itinerary_id = payana_profile_page_saved_itinerary_read_row_obj[
            row_id][saved_itinerary_id_list_activity_column_family_id][current_ts_new]

        print("Status of saved itinerary ID activity update: " +
              str(itinerary_id == updated_itinerary_id))

        # insert into created itinerary ID list
        payana_profile_page_created_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, created_itinerary_id_list_activity_column_family_id, current_ts_new, itinerary_id)

        payana_profile_page_created_itinerary_table_write_object_status = payana_profile_page_itinerary_read_obj.insert_column(
            payana_profile_page_created_itinerary_table_write_object)

        print("payana_profile_page_created_itinerary_table_write_object_status: " +
              str(payana_profile_page_created_itinerary_table_write_object_status))

        payana_profile_page_created_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)

        updated_itinerary_id = payana_profile_page_created_itinerary_read_row_obj[
            row_id][created_itinerary_id_list_activity_column_family_id][current_ts_new]

        print("Status of created itinerary ID activity update: " +
              str(itinerary_id == updated_itinerary_id))

# excursion ID list activity write
for excursion_id in excursion_update:
    for activity in activity_update:
        saved_excursion_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value])

        created_excursion_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value])

        # insert into saved excursion ID list
        payana_profile_page_saved_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, saved_excursion_id_list_activity_column_family_id, current_ts_new, excursion_id)

        payana_profile_page_saved_excursion_table_write_object_status = payana_profile_page_itinerary_read_obj.insert_column(
            payana_profile_page_saved_excursion_table_write_object)

        print("payana_profile_page_saved_excursion_table_write_object_status: " +
              str(payana_profile_page_saved_excursion_table_write_object_status))

        payana_profile_page_saved_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)

        updated_excursion_id = payana_profile_page_saved_excursion_read_row_obj[
            row_id][saved_excursion_id_list_activity_column_family_id][current_ts_new]

        print("Status of saved excursion ID activity update: " +
              str(excursion_id == updated_excursion_id))

        # insert into created excursion ID list
        payana_profile_page_created_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, created_excursion_id_list_activity_column_family_id, current_ts_new, excursion_id)

        payana_profile_page_created_excursion_table_write_object_status = payana_profile_page_itinerary_read_obj.insert_column(
            payana_profile_page_created_excursion_table_write_object)

        print("payana_profile_page_created_excursion_table_write_object_status: " +
              str(payana_profile_page_created_excursion_table_write_object_status))

        payana_profile_page_created_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)

        updated_rating = payana_profile_page_created_excursion_read_row_obj[
            row_id][created_excursion_id_list_activity_column_family_id][current_ts_new]

        print("Status of created excursion ID activity update: " +
              str(excursion_id == updated_excursion_id))


# Remove operations
for itinerary_id in itinerary_new:
    # remove from saved itinerary list
    payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(
        row_id, saved_itinerary_id_list_activity_generic_column_family_id, current_ts, "")

    payana_profile_page_itinerary_table_delete_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
        payana_profile_page_itinerary_table_write_object)
    print("payana_profile_page_itinerary_table_delete_object_status: " +
          str(payana_profile_page_itinerary_table_delete_object_status))

    payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[
        row_id][saved_itinerary_id_list_activity_generic_column_family_id]

    print("Status of itinerary ID remove from saved itinerary list: " +
          str(current_ts not in removed_itinerary_row))

    # remove from created itinerary list
    payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(
        row_id, created_itinerary_id_list_activity_generic_column_family_id, current_ts, "")

    payana_profile_page_itinerary_table_delete_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
        payana_profile_page_itinerary_table_write_object)
    print("payana_profile_page_itinerary_table_delete_object_status: " +
          str(payana_profile_page_itinerary_table_delete_object_status))

    payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[
        row_id][created_itinerary_id_list_activity_generic_column_family_id]

    print("Status of itinerary ID remove from created itinerary list: " +
          str(current_ts not in removed_itinerary_row))

for excursion_id in excursion_new:
    # remove from saved excursion list
    payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(
        row_id, saved_excursion_id_list_activity_generic_column_family_id, current_ts, "")

    payana_profile_page_excursion_table_delete_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
        payana_profile_page_excursion_table_write_object)
    print("payana_profile_page_excursion_table_delete_object_status: " +
          str(payana_profile_page_excursion_table_delete_object_status))

    payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_excursion_row = payana_profile_page_excursion_read_row_obj[
        row_id][saved_excursion_id_list_activity_generic_column_family_id]

    print("Status of excursion ID remove from saved excursion list: " +
          str(current_ts not in removed_excursion_row))

    # remove from created excursion list
    payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(
        row_id, created_excursion_id_list_activity_generic_column_family_id, current_ts, "")

    payana_profile_page_excursion_table_delete_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
        payana_profile_page_excursion_table_write_object)
    print("payana_profile_page_excursion_table_delete_object_status: " +
          str(payana_profile_page_excursion_table_delete_object_status))

    payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_excursion_row = payana_profile_page_excursion_read_row_obj[
        row_id][created_excursion_id_list_activity_generic_column_family_id]

    print("Status of excursion ID remove from created excursion list: " +
          str(current_ts not in removed_excursion_row))

# Remove the activity based itinerary ID
for itinerary_id in itinerary_update:
    for activity in activity_update:
        saved_itinerary_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value])

        created_itinerary_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value])

        # remove from saved itinerary list
        payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, saved_itinerary_id_list_activity_column_family_id, current_ts_new, "")

        payana_profile_page_itinerary_table_delete_activity_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
            payana_profile_page_itinerary_table_write_object)
        print("payana_profile_page_itinerary_table_delete_activity_object_status: " +
              str(payana_profile_page_itinerary_table_delete_activity_object_status))

        payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[
            row_id][saved_itinerary_id_list_activity_column_family_id]

        print("Status of itinerary ID remove from saved itinerary list: " +
              str(current_ts_new not in removed_itinerary_row))

        # remove from created itinerary list
        payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, created_itinerary_id_list_activity_column_family_id, current_ts_new, "")

        payana_profile_page_itinerary_table_delete_activity_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
            payana_profile_page_itinerary_table_write_object)
        print("payana_profile_page_itinerary_table_delete_activity_object_status: " +
              str(payana_profile_page_itinerary_table_delete_activity_object_status))

        payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[
            row_id][created_itinerary_id_list_activity_column_family_id]

        print("Status of itinerary ID remove from created itinerary list: " +
              str(current_ts_new not in removed_itinerary_row))

# Remove the activity based excursion ID
for excursion_id in excursion_update:
    for activity in activity_update:
        saved_excursion_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value])

        created_excursion_id_list_activity_column_family_id = "_".join(
            [activity, payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value])

        # remove from saved excursion list
        payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, saved_excursion_id_list_activity_column_family_id, current_ts_new, "")

        payana_profile_page_excursion_table_delete_activity_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
            payana_profile_page_excursion_table_write_object)
        print("payana_profile_page_excursion_table_delete_activity_saved_object_status: " +
              str(payana_profile_page_excursion_table_delete_activity_object_status))

        payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_excursion_row = payana_profile_page_excursion_read_row_obj[
            row_id][saved_excursion_id_list_activity_column_family_id]

        print("Status of excursion ID remove from saved excursion list: " +
              str(current_ts_new not in removed_excursion_row))

        # remove from created excursion list
        payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, created_excursion_id_list_activity_column_family_id, current_ts_new, "")

        payana_profile_page_excursion_table_delete_activity_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(
            payana_profile_page_excursion_table_write_object)
        print("payana_profile_page_excursion_table_delete_activity_object_status: " +
              str(payana_profile_page_excursion_table_delete_activity_object_status))

        payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_excursion_row = payana_profile_page_excursion_read_row_obj[
            row_id][created_excursion_id_list_activity_column_family_id]

        print("Status of excursion ID remove from created excursion list: " +
              str(current_ts_new not in removed_excursion_row))

# Delete the whole row
payana_profile_page_row_delete_object = bigtable_write_object_wrapper(
    row_id, "", "", "")
payana_profile_page_row_delete_object_status = payana_profile_page_itinerary_read_obj.delete_bigtable_row(
    payana_profile_page_row_delete_object)
print("payana_profile_page_row_delete_object_status: " +
      str(payana_profile_page_row_delete_object_status))

payana_profile_page_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of profile_page delete row: " +
      str(len(payana_profile_page_read_row_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
