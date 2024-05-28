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
from payana.payana_bl.bigtable_utils.PayanaEntityToCommentsTable import PayanaEntityToCommentsTable
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
 
checkin_obj = {
    "image_id_list": {
        "A": "img_id_1",
        "B": "img_id_2",
        "C": "img_id_3"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "8", "roadtrip": "9"},
    "instagram_metadata": {
        "instagram_embed_url": "xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "checkin_id": "",
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}

payana_checkin_obj = PayanaCheckinTable(**checkin_obj)
payana_checkin_obj_write_status = payana_checkin_obj.update_checkin_bigtable()
print("Payana checkin object write status: " + str(payana_checkin_obj_write_status))

checkin_id = payana_checkin_obj.checkin_id
payana_checkin_table = bigtable_constants.payana_checkin_table
payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)
checkin_obj_read = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
print(checkin_obj_read)

print("Addition of a new check in object: " + str(checkin_obj_read != None))

# Change place ID
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_checkin_place_id = bigtable_constants.payana_checkin_place_id
new_place_id = "23456789"
checkin_table_place_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_checkin_place_id, new_place_id)
payana_checkin_read_obj.insert_column(checkin_table_place_write_object)
checkin_obj_read_place_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_place_id = checkin_obj_read_place_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_checkin_place_id]

print("Status of update place ID operation: " +
      str(new_place_id == updated_place_id))

# Change city
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_checkin_city = bigtable_constants.payana_checkin_city
new_city = "Seattle"
checkin_table_place_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_checkin_city, new_city)
payana_checkin_read_obj.insert_column(checkin_table_place_write_object)
checkin_obj_read_place_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_city = checkin_obj_read_place_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_checkin_city]

print("Status of update city operation: " +
      str(new_city == updated_city))

# Change state
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_checkin_state = bigtable_constants.payana_checkin_state
new_state = "Washington"
checkin_table_place_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_checkin_state, new_state)
payana_checkin_read_obj.insert_column(checkin_table_place_write_object)
checkin_obj_read_place_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_state = checkin_obj_read_place_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_checkin_state]

print("Status of update State operation: " +
      str(new_state == updated_state))

# Change country
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_checkin_country = bigtable_constants.payana_checkin_country
new_country = "Canada"
checkin_table_place_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_checkin_country, new_country)
payana_checkin_read_obj.insert_column(checkin_table_place_write_object)
checkin_obj_read_place_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_country = checkin_obj_read_place_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_checkin_country]

print("Status of update Country operation: " +
      str(new_country == updated_country))

# Change place name
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_checkin_place_name = bigtable_constants.payana_checkin_place_name
new_place_name = "SC"
checkin_table_place_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_checkin_place_name, new_place_name)
payana_checkin_read_obj.insert_column(checkin_table_place_write_object)
checkin_obj_read_place_name_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_place_name = checkin_obj_read_place_name_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_checkin_place_name]

print("Status of update place name operation: " +
      str(new_place_name == updated_place_name))

# Change description
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_description = bigtable_constants.payana_checkin_column_family_description
new_description = "Totally enjoyed the beach!"
checkin_table_description_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_description, new_description)
payana_checkin_read_obj.insert_column(checkin_table_description_write_object)
checkin_obj_read_description_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_description = checkin_obj_read_description_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_description]

print("Status of update description operation: " +
      str(new_description == updated_description))

# Change transport mode
column_family_checkin_metadata = bigtable_constants.payana_checkin_metadata
column_qualifier_transport_mode = bigtable_constants.payana_checkin_transport_mode
new_transport_mode = "Cruise"
checkin_table_transport_mode_write_object = bigtable_write_object_wrapper(
    checkin_id, column_family_checkin_metadata, column_qualifier_transport_mode, new_transport_mode)
payana_checkin_read_obj.insert_column(
    checkin_table_transport_mode_write_object)
checkin_obj_read_transport_mode_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)
updated_transport_mode = checkin_obj_read_transport_mode_update[checkin_id][
    column_family_checkin_metadata][column_qualifier_transport_mode]

print("Status of update transport mode operation: " +
      str(new_transport_mode == updated_transport_mode))

# Add a new participant
column_family_participants_list = bigtable_constants.payana_checkin_column_family_participants_list
new_participant = {"pf_id_new": "1234567"}

for column_qualifier_new_participant, column_value_new_participant in new_participant.items():

    checkin_table_participant_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_participants_list, column_qualifier_new_participant, column_value_new_participant)
    payana_checkin_read_obj.insert_column(
        checkin_table_participant_write_object)
    checkin_obj_read_participant_mode_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_participant_list = checkin_obj_read_participant_mode_update[
        checkin_id][column_family_participants_list]

    print("Status of update participant operation: " +
          str(column_qualifier_new_participant in updated_participant_list))
    print("Status of update participant value operation: " +
          str(column_value_new_participant in updated_participant_list[column_qualifier_new_participant]))

    # Delete the new participant added
    payana_checkin_read_obj.delete_bigtable_row_column(
        checkin_table_participant_write_object)
    checkin_obj_read_participant_mode_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)

    updated_participant_list = checkin_obj_read_participant_mode_update[
        checkin_id][column_family_participants_list]

    print("Status of update participant operation: " +
          str(column_qualifier_new_participant not in updated_participant_list))


# Add an image ID -- no use case to call as an API end point. For debugging or backfilling purpose
column_family_image_id_list = bigtable_constants.payana_checkin_column_family_image_id_list
new_image_id = {"D": "image_id_new"}

for column_qualifier_new_image_id, column_value_new_image_id in new_image_id.items():

    checkin_table_image_id_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_image_id_list, column_qualifier_new_image_id, column_value_new_image_id)
    payana_checkin_read_obj.insert_column(checkin_table_image_id_write_object)
    checkin_obj_read_image_id_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_image_id_list = checkin_obj_read_image_id_update[
        checkin_id][column_family_image_id_list]

    print("Status of update image ID operation: " +
          str(column_qualifier_new_image_id in updated_image_id_list))
    print("Status of update image ID value operation: " +
          str(column_value_new_image_id in updated_image_id_list[column_qualifier_new_image_id]))

    # Delete newly added image ID
    payana_checkin_read_obj.delete_bigtable_row_column(
        checkin_table_image_id_write_object)
    checkin_obj_read_image_id_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)

    updated_image_id_list = checkin_obj_read_image_id_update[
        checkin_id][column_family_image_id_list]

    print("Status of delete image ID operation: " +
          str(column_qualifier_new_image_id not in updated_image_id_list))


# Add an acivity
column_family_activity_list = bigtable_constants.payana_checkin_activities_list
new_activity = {"date": "3"}

for column_qualifier_activity, column_value_activity in new_activity.items():

    checkin_table_activity_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_activity_list, column_qualifier_activity, column_value_activity)
    payana_checkin_read_obj.insert_column(checkin_table_activity_write_object)
    checkin_obj_read_activity_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_activity_list = checkin_obj_read_activity_update[
        checkin_id][column_family_activity_list]

    print("Status of update activity operation: " +
          str(column_qualifier_activity in updated_activity_list))
    print("Status of update activity value operation: " +
          str(column_value_activity in updated_activity_list[column_qualifier_activity]))

    # Delete activity
    payana_checkin_read_obj.delete_bigtable_row_column(
        checkin_table_activity_write_object)
    checkin_obj_read_activity_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_activity_list = checkin_obj_read_activity_update[
        checkin_id][column_family_activity_list]

    print("Status of update activity operation: " +
          str(column_qualifier_activity not in updated_activity_list))


# Change Instagram embed URL
column_family_instagram_metadata = bigtable_constants.payana_checkin_instagram_metadata

payana_checkin_instagram_embed_url = bigtable_constants.payana_checkin_instagram_embed_url
payana_checkin_instagram_post_id = bigtable_constants.payana_checkin_instagram_post_id

insta_embed_url = {"instagram_embed_url": "abc.com"}

for column_qualifier_insta_embed_url, column_value_insta_embed_url in insta_embed_url.items():

    checkin_table_insta_embed_url_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_instagram_metadata, column_qualifier_insta_embed_url, column_value_insta_embed_url)
    payana_checkin_read_obj.insert_column(
        checkin_table_insta_embed_url_write_object)
    checkin_obj_read_insta_embed_url_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_insta_embed_url_list = checkin_obj_read_insta_embed_url_update[
        checkin_id][column_family_instagram_metadata]

    print("Status of update instagram_embed_url operation: " +
          str(column_qualifier_insta_embed_url in updated_insta_embed_url_list))
    print("Status of update instagram_embed_url value operation: " +
          str(column_value_insta_embed_url in updated_insta_embed_url_list[column_qualifier_insta_embed_url]))

# Change Instagram Post ID
insta_post_id = {"instagram_post_id": "6789"}

for column_qualifier_insta_post_id, column_value_insta_post_id in insta_post_id.items():

    checkin_table_insta_post_id_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_instagram_metadata, column_qualifier_insta_post_id, column_value_insta_post_id)
    payana_checkin_read_obj.insert_column(
        checkin_table_insta_post_id_write_object)
    checkin_obj_read_insta_post_id_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_insta_post_id = checkin_obj_read_insta_post_id_update[
        checkin_id][column_family_instagram_metadata]

    print("Status of update insta_post_id operation: " +
          str(column_qualifier_insta_post_id in updated_insta_post_id))
    print("Status of update insta_post_id value operation: " +
          str(column_value_insta_post_id in updated_insta_post_id[column_qualifier_insta_post_id]))


# Change Airbnb embed URL
column_family_airbnb_metadata = bigtable_constants.payana_checkin_airbnb_metadata

payana_checkin_airbnb_embed_url = bigtable_constants.payana_checkin_airbnb_embed_url
payana_checkin_airbnb_post_id = bigtable_constants.payana_checkin_airbnb_post_id

airbnb_embed_url = {"airbnb_embed_url": "abc.com"}

for column_qualifier_airbnb_embed_url, column_value_airbnb_embed_url in airbnb_embed_url.items():

    checkin_table_airbnb_embed_url_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_airbnb_metadata, column_qualifier_airbnb_embed_url, column_value_airbnb_embed_url)
    payana_checkin_read_obj.insert_column(
        checkin_table_airbnb_embed_url_write_object)
    checkin_obj_read_airbnb_embed_url_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_airbnb_embed_url_list = checkin_obj_read_airbnb_embed_url_update[
        checkin_id][column_family_airbnb_metadata]

    print("Status of update airbnb_embed_url operation: " +
          str(column_qualifier_airbnb_embed_url in updated_airbnb_embed_url_list))
    print("Status of update airbnb_embed_url value operation: " +
          str(column_value_airbnb_embed_url in updated_airbnb_embed_url_list[column_qualifier_airbnb_embed_url]))

# Change Airbnb Post ID
airbnb_post_id = {"airbnb_post_id": "6789"}

for column_qualifier_airbnb_post_id, column_value_airbnb_post_id in airbnb_post_id.items():

    checkin_table_airbnb_post_id_write_object = bigtable_write_object_wrapper(
        checkin_id, column_family_airbnb_metadata, column_qualifier_airbnb_post_id, column_value_airbnb_post_id)
    payana_checkin_read_obj.insert_column(
        checkin_table_airbnb_post_id_write_object)
    checkin_obj_read_airbnb_post_id_update = payana_checkin_read_obj.get_row_dict(
        checkin_id, include_column_family=True)
    updated_airbnb_post_id = checkin_obj_read_airbnb_post_id_update[
        checkin_id][column_family_airbnb_metadata]

    print("Status of update airbnb_post_id operation: " +
          str(column_qualifier_airbnb_post_id in updated_airbnb_post_id))
    print("Status of update airbnb_post_id value operation: " +
          str(column_value_airbnb_post_id in updated_airbnb_post_id[column_qualifier_airbnb_post_id]))

# Remove the whole chekcin row
checkin_row_delete_object = bigtable_write_object_wrapper(
    checkin_id, "", "", "")
payana_checkin_obj_delete_status = payana_checkin_read_obj.delete_bigtable_row(checkin_row_delete_object)
print("Payana checkin object delete status: " + str(payana_checkin_obj_delete_status))

checkin_obj_read_activity_update = payana_checkin_read_obj.get_row_dict(
    checkin_id, include_column_family=True)

print("Status of checkin obj delete row:" +
      str(len(checkin_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
