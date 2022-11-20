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
from payana.payana_bl.bigtable_utils.PayanaGlobalCountryTimestampItineraryTable import PayanaGlobalCountryTimestampItineraryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

global_country_itinerary_obj = {
    "country": "usa",
    "itinerary_id": {"1" : "12345"},
    "excursion_id": {"1" : "12345"},
    "checkin_id": {"1" : "12345"},
    "activities": ["hiking", "romantic", "exotic"]
}

payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value = bigtable_constants.payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value

payana_global_country_itinerary_obj = PayanaGlobalCountryTimestampItineraryTable(
    **global_country_itinerary_obj)

payana_global_country_itinerary_obj_write_status = payana_global_country_itinerary_obj.update_global_country_itinerary_bigtable()
print("payana_global_country_itinerary_obj write status: " +
      str(payana_global_country_itinerary_obj_write_status))

payana_global_country_itinerary_table = bigtable_constants.payana_global_country_itinerary_table
# We could use regular expression to exclude the year part while querying
row_id = payana_global_country_itinerary_obj.row_id
payana_global_country_itinerary_read_obj = PayanaBigTable(
    payana_global_country_itinerary_table)
payana_global_country_itinerary_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print(payana_global_country_itinerary_read_row_obj)

print("Status of add global country itinerary: " +
      str(payana_global_country_itinerary_read_row_obj is not None))

activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family

# generic activity write objects
itinerary_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

excursion_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

checkin_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

payana_global_country_itinerary_table_itinerary_id_quantifier_value = bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value
payana_global_country_itinerary_table_excursion_id_quantifier_value = bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value
payana_global_country_itinerary_table_checkin_id_quantifier_value = bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value

# Add another itinerary ID, excursion ID and checkin ID
itinerary_new = {"2": "6789"}
excursion_new = {"2": "6789"}
checkin_new = {"2": "6789"}

for rating, itinerary_id in itinerary_new.items():
    payana_global_country_itinerary_table_write_object = bigtable_write_object_wrapper(
        row_id, itinerary_activity_generic_column_family_id, rating, itinerary_id)
    payana_global_country_itinerary_read_obj.insert_column(
        payana_global_country_itinerary_table_write_object)
    payana_global_country_itinerary_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_itinerary_id = payana_global_country_itinerary_read_row_obj[row_id][
        itinerary_activity_generic_column_family_id][rating]

    print("Status of itinerary ID update: " + str(itinerary_id == updated_itinerary_id))

for rating, excursion_id in excursion_new.items():
    payana_global_country_excursion_table_write_object = bigtable_write_object_wrapper(
        row_id, excursion_activity_generic_column_family_id, rating, excursion_id)
    payana_global_country_itinerary_read_obj.insert_column(
        payana_global_country_excursion_table_write_object)
    payana_global_country_excursion_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_excursion_id = payana_global_country_excursion_read_row_obj[row_id][
        excursion_activity_generic_column_family_id][rating]

    print("Status of excursion ID update: " + str(excursion_id == updated_excursion_id))

for rating, checkin_id in checkin_new.items():
    payana_global_country_checkin_table_write_object = bigtable_write_object_wrapper(
        row_id, checkin_activity_generic_column_family_id, rating, checkin_id)
    payana_global_country_itinerary_read_obj.insert_column(
        payana_global_country_checkin_table_write_object)
    payana_global_country_checkin_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    updated_checkin_id = payana_global_country_checkin_read_row_obj[row_id][
        checkin_activity_generic_column_family_id][rating]

    print("Status of checkin ID update: " + str(checkin_id == updated_checkin_id))

# Add another itinerary ID, excursion ID and checkin ID with activities
global_country_itinerary_update_obj = {
    "itinerary_id": {"3": "34567"},
    "excursion_id": {"3": "34567"},
    "checkin_id": {"3": "34567"},
    "activities": ["hiking", "romantic", "exotic"]
}

itinerary_update = global_country_itinerary_update_obj[
    payana_global_country_itinerary_table_itinerary_id_quantifier_value]
excursion_update = global_country_itinerary_update_obj[
    payana_global_country_itinerary_table_excursion_id_quantifier_value]
checkin_update = global_country_itinerary_update_obj[
    payana_global_country_itinerary_table_checkin_id_quantifier_value]
activity_update = global_country_itinerary_update_obj[
    bigtable_constants.payana_global_country_itinerary_table_activities]

for rating, itinerary_id in itinerary_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, itinerary_activity_column_family_id, rating, itinerary_id)
        payana_global_country_itinerary_read_obj.insert_column(
            payana_global_country_itinerary_table_write_object)
        payana_global_country_itinerary_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        updated_itinerary_id = payana_global_country_itinerary_read_row_obj[
            row_id][itinerary_activity_column_family_id][rating]

        print("Status of itinerary ID activity update: " +
              str(itinerary_id == updated_itinerary_id))

for rating, excursion_id in excursion_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, excursion_activity_column_family_id, rating, excursion_id)
        payana_global_country_itinerary_read_obj.insert_column(
            payana_global_country_excursion_table_write_object)
        payana_global_country_excursion_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        updated_excursion_id = payana_global_country_excursion_read_row_obj[
            row_id][excursion_activity_column_family_id][rating]

        print("Status of excursion ID activity update: " +
              str(excursion_id == updated_excursion_id))

for rating, checkin_id in checkin_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_checkin_table_write_object = bigtable_write_object_wrapper(
            row_id, checkin_activity_column_family_id, rating, checkin_id)
        payana_global_country_itinerary_read_obj.insert_column(
            payana_global_country_checkin_table_write_object)
        payana_global_country_checkin_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        updated_checkin_id = payana_global_country_checkin_read_row_obj[
            row_id][checkin_activity_column_family_id][rating]

        print("Status of checkin ID activity update: " +
              str(checkin_id == updated_checkin_id))

# Remove an itinerary ID, excursion ID, check ID
for rating, itinerary_id in itinerary_new.items():
    payana_global_country_itinerary_table_write_object = bigtable_write_object_wrapper(
        row_id, itinerary_activity_generic_column_family_id, rating, "")
    payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
        payana_global_country_itinerary_table_write_object)
    payana_global_country_itinerary_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_itinerary_row = payana_global_country_itinerary_read_row_obj[
        row_id][itinerary_activity_generic_column_family_id]

    print("Status of itinerary ID remove: " +
          str(rating not in removed_itinerary_row))

for rating, excursion_id in excursion_new.items():
    payana_global_country_excursion_table_write_object = bigtable_write_object_wrapper(
        row_id, excursion_activity_generic_column_family_id, rating, "")
    payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
        payana_global_country_excursion_table_write_object)
    payana_global_country_excursion_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_excursion_row = payana_global_country_excursion_read_row_obj[
        row_id][excursion_activity_generic_column_family_id]

    print("Status of excursion ID remove: " +
          str(rating not in removed_excursion_row))

for rating, checkin_id in checkin_new.items():
    payana_global_country_checkin_table_write_object = bigtable_write_object_wrapper(
        row_id, checkin_activity_generic_column_family_id, rating, "")
    payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
        payana_global_country_checkin_table_write_object)
    payana_global_country_checkin_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_checkin_row = payana_global_country_checkin_read_row_obj[
        row_id][checkin_activity_generic_column_family_id]

    print("Status of checkin ID remove: " +
          str(rating not in removed_checkin_row))

# Remove the activity based itinerary ID, excursion ID, checkin ID
for rating, itinerary_id in itinerary_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_itinerary_table_write_object = bigtable_write_object_wrapper(
            row_id, itinerary_activity_column_family_id, rating, "")
        payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
            payana_global_country_itinerary_table_write_object)
        payana_global_country_itinerary_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_itinerary_row = payana_global_country_itinerary_read_row_obj[
            row_id][itinerary_activity_column_family_id]

        print("Status of itinerary ID activity remove: " +
              str(rating not in removed_itinerary_row))

for rating, excursion_id in excursion_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_excursion_table_write_object = bigtable_write_object_wrapper(
            row_id, excursion_activity_column_family_id, rating, "")
        payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
            payana_global_country_excursion_table_write_object)
        payana_global_country_excursion_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_excursion_row = payana_global_country_excursion_read_row_obj[
            row_id][excursion_activity_column_family_id]

        print("Status of excursion ID activity remove: " +
              str(rating not in removed_excursion_row))

for rating, checkin_id in checkin_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join(
            [activity, payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value, bigtable_constants.payana_global_country_itinerary_table_checkin_id_quantifier_value])

        payana_global_country_checkin_table_write_object = bigtable_write_object_wrapper(
            row_id, checkin_activity_column_family_id, rating, "")
        payana_global_country_itinerary_read_obj.delete_bigtable_row_column(
            payana_global_country_checkin_table_write_object)
        payana_global_country_checkin_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
            row_id, include_column_family=True)
        removed_checkin_row = payana_global_country_checkin_read_row_obj[
            row_id][checkin_activity_column_family_id]

        print("Status of checkin ID activity remove: " +
              str(rating not in removed_checkin_row))

# Delete the whole row
payana_global_country_row_delete_object = bigtable_write_object_wrapper(
    row_id, "", "", "")
payana_global_country_itinerary_read_obj_delete_status = payana_global_country_itinerary_read_obj.delete_bigtable_row(
    payana_global_country_row_delete_object)
print("payana_global_country_itinerary_read_obj_delete_status: " +
      str(payana_global_country_itinerary_read_obj_delete_status))

payana_global_country_read_row_obj = payana_global_country_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of payana_global_city delete row: " +
      str(len(payana_global_country_read_row_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
