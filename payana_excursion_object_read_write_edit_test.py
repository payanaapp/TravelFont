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
from payana.payana_bl.bigtable_utils.PayanaPersonalPlaceIdItineraryTable import PayanaPersonalPlaceIdItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCityItineraryTable import PayanaPersonalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

excursion_obj = {
    "checkin_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "roadtrip": "6"},
    "excursion_metadata": {
        "excursion_id": "",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "visit_timestamp": "123456789",
        "description": "",
        "itinerary_id": "1234",
        "place_name": "SF"
    }
}

payana_excursion_obj = PayanaExcursionTable(**excursion_obj)
payana_excursion_obj.update_excursion_bigtable()
excursion_id = payana_excursion_obj.excursion_id
payana_excursion_table = bigtable_constants.payana_excursion_table
payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)
excursion_obj_read = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
print(excursion_obj_read)

print("Addition of a new excursion object: " + str(excursion_obj_read != None))

# Change place ID
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_place_id = bigtable_constants.payana_excursion_id
new_place_id = "23456789"
excursion_table_place_write_object = bigtable_write_object_wrapper(excursion_id, column_family_excursion_metadata, column_qualifier_excursion_place_id, new_place_id)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
updated_place_id = excursion_obj_read_place_update[excursion_id][column_family_excursion_metadata][column_qualifier_excursion_place_id]

print("Status of update place ID operation: " + str(new_place_id == updated_place_id))

# Change place name
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_excursion_place_name = bigtable_constants.payana_excursion_place_name
new_place_name = "SC"
excursion_table_place_write_object = bigtable_write_object_wrapper(excursion_id, column_family_excursion_metadata, column_qualifier_excursion_place_name, new_place_name)
payana_excursion_read_obj.insert_column(excursion_table_place_write_object)
excursion_obj_read_place_name_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
updated_place_name = excursion_obj_read_place_name_update[excursion_id][column_family_excursion_metadata][column_qualifier_excursion_place_name]

print("Status of update place name operation: " + str(new_place_name == updated_place_name))

# Change description
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_description = bigtable_constants.payana_excursion_column_family_description
new_description = "Totally enjoyed the beach!"
excursion_table_description_write_object = bigtable_write_object_wrapper(excursion_id, column_family_excursion_metadata, column_qualifier_description, new_description)
payana_excursion_read_obj.insert_column(excursion_table_description_write_object)
excursion_obj_read_description_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
updated_description = excursion_obj_read_description_update[excursion_id][column_family_excursion_metadata][column_qualifier_description]

print("Status of update description operation: " + str(new_description == updated_description))

# Change transport
column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
column_qualifier_transport_mode = bigtable_constants.payana_excursion_transport_mode
new_transport_mode = "Cruise"
excursion_table_transport_mode_write_object = bigtable_write_object_wrapper(excursion_id, column_family_excursion_metadata, column_qualifier_transport_mode, new_transport_mode)
payana_excursion_read_obj.insert_column(excursion_table_transport_mode_write_object)
excursion_obj_read_transport_mode_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
updated_transport_mode = excursion_obj_read_transport_mode_update[excursion_id][column_family_excursion_metadata][column_qualifier_transport_mode]

print("Status of update transport mode operation: " + str(new_transport_mode == updated_transport_mode))

# Add a new participant
column_family_participants_list = bigtable_constants.payana_excursion_column_family_participants_list
new_participant = {"pf_id_new" : "1234567"}

for column_qualifier_new_participant, column_value_new_participant in new_participant.items():

    excursion_table_participant_write_object = bigtable_write_object_wrapper(excursion_id, column_family_participants_list, column_qualifier_new_participant, column_value_new_participant)
    payana_excursion_read_obj.insert_column(excursion_table_participant_write_object)
    excursion_obj_read_participant_mode_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
    updated_participant_list = excursion_obj_read_participant_mode_update[excursion_id][column_family_participants_list]

    print("Status of update participant operation: " + str(column_qualifier_new_participant in updated_participant_list))
    print("Status of update participant value operation: " + str(column_value_new_participant in updated_participant_list[column_qualifier_new_participant]))

    # Delete the new participant added
    payana_excursion_read_obj.delete_bigtable_row_column(excursion_table_participant_write_object)
    excursion_obj_read_participant_mode_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)

    updated_participant_list = excursion_obj_read_participant_mode_update[excursion_id][column_family_participants_list]

    print("Status of update participant operation: " + str(column_qualifier_new_participant not in updated_participant_list))


#Add a check in ID -- no use case to call as an API end point. For debugging or backfilling purpose
column_family_checkin_id_list = bigtable_constants.payana_excursion_column_family_checkin_id_list
new_checkin_id = {"4" : "12345"}

for column_qualifier_new_checkin_id, column_value_new_checkin_id in new_checkin_id.items():

    excursion_table_checkin_id_write_object = bigtable_write_object_wrapper(excursion_id, column_family_checkin_id_list, column_qualifier_new_checkin_id, column_value_new_checkin_id)
    payana_excursion_read_obj.insert_column(excursion_table_checkin_id_write_object)
    excursion_obj_read_checkin_id_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
    updated_checkin_id_list = excursion_obj_read_checkin_id_update[excursion_id][column_family_checkin_id_list]

    print("Status of update check in ID operation: " + str(column_qualifier_new_checkin_id in updated_checkin_id_list))
    print("Status of update check in ID value operation: " + str(column_value_new_checkin_id in updated_checkin_id_list[column_qualifier_new_checkin_id]))

    # Delete newly added checkin ID
    payana_excursion_read_obj.delete_bigtable_row_column(excursion_table_checkin_id_write_object)
    excursion_obj_read_checkin_id_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)

    updated_checkin_id_list = excursion_obj_read_checkin_id_update[excursion_id][column_family_checkin_id_list]

    print("Status of delete checkin ID operation: " + str(column_qualifier_new_checkin_id not in updated_checkin_id_list))


#Add an acivity
column_family_activity_list = bigtable_constants.payana_excursion_activities_list
new_activity = {"date" : "3"}

for column_qualifier_activity, column_value_activity in new_activity.items():

    excursion_table_activity_write_object = bigtable_write_object_wrapper(excursion_id, column_family_activity_list, column_qualifier_activity, column_value_activity)
    payana_excursion_read_obj.insert_column(excursion_table_activity_write_object)
    excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
    updated_activity_list = excursion_obj_read_activity_update[excursion_id][column_family_activity_list]

    print("Status of update activity operation: " + str(column_qualifier_activity in updated_activity_list))
    print("Status of update activity value operation: " + str(column_value_activity in updated_activity_list[column_qualifier_activity]))

    # Delete activity
    payana_excursion_read_obj.delete_bigtable_row_column(excursion_table_activity_write_object)
    excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True)
    updated_activity_list = excursion_obj_read_activity_update[excursion_id][column_family_activity_list]

    print("Status of update activity operation: " + str(column_qualifier_activity not in updated_activity_list))


#Add a comment
comment_obj = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj.update_comment_bigtable()
entity_id = payana_comment_obj.entity_id
comment_id = payana_comment_obj.comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(entity_id, include_column_family=False)

print("Comment added: " + str(payana_comment_obj is not None))

# Edit a comment
comment_obj = {
    "comment_timestamp": "678910234",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "13",
    "comment_id": comment_id,
    "entity_id": "imagee"
}

payana_comments_table_timestamp = bigtable_constants.payana_comments_table_timestamp
payana_comments_table_likes_count = bigtable_constants.payana_comments_table_likes_count
new_timestamp = comment_obj[payana_comments_table_timestamp]
new_likes_count = comment_obj[payana_comments_table_likes_count]

payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj.update_comment_bigtable()
entity_id = payana_comment_obj.entity_id
comment_id = payana_comment_obj.comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(entity_id, include_column_family=False)
payana_comment_obj_edited = payana_comment_obj[entity_id][comment_id]

import re
p = re.compile('(?<!\\\\)\'')
payana_comment_obj_edited = p.sub('\"', payana_comment_obj_edited)

payana_comment_obj_edited = json.loads(payana_comment_obj_edited)
print(payana_comment_obj_edited)

print("Comment timestamp edited: " + str(payana_comment_obj_edited[payana_comments_table_timestamp] == new_timestamp))
print("Comment likes count edited: " + str(payana_comment_obj_edited[payana_comments_table_likes_count] == new_likes_count))

#Add another comment
comment_obj_dup = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

payana_comment_obj_dup = PayanaCommentsTable(**comment_obj_dup)
payana_comment_obj_dup.update_comment_bigtable()
entity_id = payana_comment_obj_dup.entity_id
comment_id = payana_comment_obj_dup.comment_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
payana_comment_obj = payana_comment_read_obj.get_row_dict(entity_id, include_column_family=False)

print("Status of new comment write: " + str(len(payana_comment_obj[entity_id]) == 2))

# Delete one comment in the row
payana_comments_family_id = bigtable_constants.payana_comments_table_comments_family_id
payana_comment_bigtable_obj = bigtable_write_object_wrapper(entity_id, payana_comments_family_id, comment_id, "")
payana_comment_read_obj.delete_bigtable_row_column(payana_comment_bigtable_obj)

comment_obj = payana_comment_read_obj.get_row_dict(entity_id, include_column_family=False)

print("Status of one comment delete operation: " + str(len(comment_obj[entity_id]) == 1))

# Delete the comment row
payana_comment_bigtable_obj = bigtable_write_object_wrapper(entity_id, "", "", "")
payana_comment_read_obj.delete_bigtable_row(payana_comment_bigtable_obj)

comment_obj = payana_comment_read_obj.get_row_dict(entity_id, include_column_family=False)

print("Status of comment row delete: " + str(len(comment_obj) == 0))

#Add a like and read a like
likes_obj = {
    "payana_likes": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "entity_id": "12345"
}

payana_like_column_family = bigtable_constants.payana_likes_table_column_family
payana_likes_obj = PayanaLikesTable(**likes_obj)
payana_likes_obj.update_likes_bigtable()
payana_likes_table = bigtable_constants.payana_likes_table
like_object_id = payana_likes_obj.entity_id
payana_likes_read_obj = PayanaBigTable(payana_likes_table)
likes_obj = payana_likes_read_obj.get_row_dict(like_object_id, include_column_family=True)

participant_delete = "pf_id_1"
print("Status of like write operation: " + str(participant_delete in likes_obj[like_object_id][payana_like_column_family]))

# Remove a specific like
payana_like_bigtable_obj = bigtable_write_object_wrapper(like_object_id, payana_like_column_family, participant_delete, "")
payana_likes_read_obj.delete_bigtable_row_column(payana_like_bigtable_obj)

likes_obj = payana_likes_read_obj.get_row_dict(like_object_id, include_column_family=True)

print("Status of like delete operation: " + str(participant_delete not in likes_obj[like_object_id][payana_like_column_family]))

#Remove the whole row
payana_like_bigtable_obj = bigtable_write_object_wrapper(like_object_id, "", "", "")
payana_likes_read_obj.delete_bigtable_row(payana_like_bigtable_obj)

likes_obj = payana_likes_read_obj.get_row_dict(like_object_id, include_column_family=False)
print("Status of like row delete: " + str(len(likes_obj) == 0))


payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)