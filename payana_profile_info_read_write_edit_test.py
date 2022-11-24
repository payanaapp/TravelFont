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

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_profile_table_personal_info_column_family = bigtable_constants.payana_profile_table_personal_info_column_family
payana_profile_favorite_places_preference = bigtable_constants.payana_profile_favorite_places_preference
payana_profile_favorite_activities_preference = bigtable_constants.payana_profile_favorite_activities_preference
payana_profile_table_thumbnail_travel_buddies = bigtable_constants.payana_profile_table_thumbnail_travel_buddies
payana_profile_table_top_activities_tracker_rating = bigtable_constants.payana_profile_table_top_activities_tracker_rating

profile_obj = {
    payana_profile_table_personal_info_column_family:
    {
        "profile_name": "abkr",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111",
        "doj" : "11/11/1111"
    },
    payana_profile_table_top_activities_tracker_rating:
    {
        "hiking": "0.67",
        "adventure": "0.4",
        "fashion": "0.78"
    },
    payana_profile_favorite_places_preference: {
        "cupertino##california##usa": "1234578", #place ID
        "california##usa": "1234578",
        "usa": "1234578",
        "sanfrancisco##california##usa": "1234578",
        "oregon##usa": "1234578",
        "france": "1234578"
    },
    payana_profile_favorite_activities_preference: {
        "hiking": "1",
        "ski trips": "2",
        "adventures": "3",
        "spring break" : "4",
        "road trips" : "5",
        "food trips" : "6"
    },
    payana_profile_table_thumbnail_travel_buddies : {
        "123456" : "1",
        "234567" : "2",
        "345678" : "3",
        "456789" : "4",
        "567890" : "5",
        "678911" : "6",
        "678921" : "7",
    }
}

payana_profile_obj = PayanaProfileTable(**profile_obj)
payana_profile_obj_write_status = payana_profile_obj.update_profile_info_bigtable()

print("payana_profile_obj_write_status: " + str(payana_profile_obj_write_status))

profile_id = payana_profile_obj.profile_id
payana_profile_table = bigtable_constants.payana_profile_table
payana_profile_read_obj = PayanaBigTable(payana_profile_table)
payana_profile_obj_read = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
print(payana_profile_obj_read)

print("Addition of a new profile object: " +
      str(payana_profile_obj_read != None))

# Change profile name
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_profile_name = bigtable_constants.payana_profile_table_profile_name
new_profile_name = "abhinandankr"
profile_table_profile_name_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_profile_name, new_profile_name)
payana_profile_read_obj.insert_column(profile_table_profile_name_write_object)
profile_table_profile_name_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_profile_name = profile_table_profile_name_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_profile_name]

print("Status of update profile name operation: " +
      str(new_profile_name == updated_profile_name))

# Change user name
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_user_name = bigtable_constants.payana_profile_table_user_name
new_user_name = "abhinandankr"
profile_table_profile_name_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_user_name, new_user_name)
payana_profile_read_obj.insert_column(profile_table_profile_name_write_object)
profile_table_user_name_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_user_name = profile_table_user_name_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_user_name]

print("Status of update user name operation: " +
      str(new_user_name == updated_user_name))

# Change profile description
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_profile_description = bigtable_constants.payana_profile_table_profile_description
new_profile_description = "abhinandankr's profile"
profile_table_profile_description_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_profile_description, new_profile_description)
payana_profile_read_obj.insert_column(
    profile_table_profile_description_write_object)
profile_table_profile_description_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_profile_description = profile_table_profile_description_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_profile_description]

print("Status of update profile description operation: " +
      str(new_profile_description == updated_profile_description))

# Change blog url
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_blog_url = bigtable_constants.payana_profile_table_blog_url
new_blog_url = "abhinandankr.com"
profile_table_blog_url_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_blog_url, new_blog_url)
payana_profile_read_obj.insert_column(profile_table_blog_url_write_object)
profile_table_blog_url_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_blog_url = profile_table_blog_url_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_blog_url]

print("Status of update blog_url operation: " +
      str(new_blog_url == updated_blog_url))

# Change email
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_email = bigtable_constants.payana_profile_table_email
new_email = "abhinandankr@gmail.com"
profile_table_email_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_email, new_email)
payana_profile_read_obj.insert_column(profile_table_email_write_object)
profile_table_email_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_email = profile_table_email_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_email]

print("Status of update email operation: " + str(new_email == updated_email))


# Change phone
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_phone = bigtable_constants.payana_profile_table_phone
new_phone = "67891234"
profile_table_phone_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_phone, new_phone)
payana_profile_read_obj.insert_column(profile_table_phone_write_object)
profile_table_phone_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_phone = profile_table_phone_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_phone]

print("Status of update phone operation: " + str(new_phone == updated_phone))

# Change private_account
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_private_account = bigtable_constants.payana_profile_table_private_account
new_private_account = "false"
profile_table_private_account_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_private_account, new_private_account)
payana_profile_read_obj.insert_column(
    profile_table_private_account_write_object)
profile_table_private_account_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_private_account = profile_table_private_account_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_private_account]

print("Status of update private_account operation: " +
      str(new_private_account == updated_private_account))


# Change gender
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_gender = bigtable_constants.payana_profile_table_gender
new_gender = "female"
profile_table_gender_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_gender, new_gender)
payana_profile_read_obj.insert_column(profile_table_gender_write_object)
profile_table_gender_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_gender = profile_table_gender_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_gender]

print("Status of update phone operation: " + str(new_gender == updated_gender))

# Change date of birth
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_date_of_birth = bigtable_constants.payana_profile_table_date_of_birth
new_date_of_birth = "22/22/2222"
profile_table_date_of_birth_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_date_of_birth, new_date_of_birth)
payana_profile_read_obj.insert_column(profile_table_date_of_birth_write_object)
profile_table_date_of_birth_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_date_of_birth = profile_table_date_of_birth_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_date_of_birth]

print("Status of update date_of_birth operation: " +
      str(new_date_of_birth == updated_date_of_birth))

# Change doj
column_family_profile_table_metadata = bigtable_constants.payana_profile_table_personal_info_column_family
column_qualifier_profile_table_doj = bigtable_constants.payana_profile_table_doj
new_doj = "22/22/2222"
profile_table_doj_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_profile_table_metadata, column_qualifier_profile_table_doj, new_doj)
payana_profile_read_obj.insert_column(profile_table_doj_write_object)
profile_table_doj_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_doj = profile_table_doj_update[profile_id][
    column_family_profile_table_metadata][column_qualifier_profile_table_doj]

print("Status of update doj operation: " +
      str(new_doj == updated_doj))


# Change top activity tracker score
column_family_top_activities = bigtable_constants.payana_profile_table_top_activities_tracker_rating
activity_name = "hiking"
new_hiking_score = "1.23"
profile_table_hiking_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_top_activities, activity_name, new_hiking_score)
payana_profile_read_obj.insert_column(profile_table_hiking_write_object)
profile_table_hiking_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_hiking_score = profile_table_hiking_update[profile_id][
    column_family_top_activities][activity_name]

print("Status of update tracker hiking activity score operation: " +
      str(new_hiking_score == updated_hiking_score))

# Add an activity into top activity tracker section
column_family_top_activities = bigtable_constants.payana_profile_table_top_activities_tracker_rating
activity_name = "road_trip"
new_road_trip_score = "0.87"
profile_table_road_trip_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_top_activities, activity_name, new_road_trip_score)
payana_profile_read_obj.insert_column(profile_table_road_trip_write_object)
profile_table_road_trip_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_road_trip_score = profile_table_road_trip_update[
    profile_id][column_family_top_activities][activity_name]

print("Status of add road_trip activity score operation into favorite activity preference section: " +
      str(new_road_trip_score == updated_road_trip_score))

# Delete an activity from top activity tracker section
payana_profile_obj_delete_activity_status = payana_profile_read_obj.delete_bigtable_row_column(
    profile_table_road_trip_write_object)

print("payana_profile_obj_delete_activity_status: " + str(payana_profile_obj_delete_activity_status))

profile_table_road_trip_delete = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_top_activities = profile_table_road_trip_delete[profile_id][column_family_top_activities]

print("Status of delete activity operation: " +
      str(activity_name not in updated_top_activities))

# Change favorite place place ID
column_family_favorite_places_preference = bigtable_constants.payana_profile_favorite_places_preference
favorite_place = "cupertino##california##usa"
new_favorite_place_id = "95054"
profile_table_favorite_place_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_favorite_places_preference, favorite_place, new_favorite_place_id)
payana_profile_read_obj.insert_column(profile_table_favorite_place_write_object)
profile_table_favorite_place_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_place_id = profile_table_favorite_place_score_update[profile_id][
    column_family_favorite_places_preference][favorite_place]

print("Status of update favorite place score operation: " +
      str(new_favorite_place_id == updated_favorite_place_id))

# Add a new favorite place
column_family_favorite_places_preference = bigtable_constants.payana_profile_favorite_places_preference
new_favorite_place = "mpk##california##usa"
new_favorite_place_id = "95014"
profile_table_favorite_place_write_object = bigtable_write_object_wrapper(
    profile_id, column_family_favorite_places_preference, new_favorite_place, new_favorite_place_id)
payana_profile_read_obj.insert_column(profile_table_favorite_place_write_object)
profile_table_favorite_place_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_place_id = profile_table_favorite_place_score_update[profile_id][
    column_family_favorite_places_preference][new_favorite_place]

print("Status of update favorite place operation: " +
      str(new_favorite_place_id == updated_favorite_place_id))

# Delete a favorite place
payana_profile_obj_delete_favorite_place_status = payana_profile_read_obj.delete_bigtable_row_column(
    profile_table_favorite_place_write_object)

print("payana_profile_obj_delete_favorite_place_status: " + str(payana_profile_obj_delete_favorite_place_status))

profile_table_favorite_place_delete = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_favorite_places = profile_table_favorite_place_delete[profile_id][column_family_favorite_places_preference]

print("Status of delete favorite place operation: " +
      str(new_favorite_place not in updated_favorite_places))


# Change favorite activity score
payana_profile_favorite_activities_preference = bigtable_constants.payana_profile_favorite_activities_preference
favorite_activity = "hiking"
new_favorite_activity_score = "18"
profile_table_favorite_activity_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_favorite_activities_preference, favorite_activity, new_favorite_activity_score)
payana_profile_read_obj.insert_column(profile_table_favorite_activity_write_object)
profile_table_favorite_activity_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_activity_score = profile_table_favorite_activity_score_update[profile_id][
    payana_profile_favorite_activities_preference][favorite_activity]

print("Status of update favorite activity score operation: " +
      str(new_favorite_activity_score == updated_favorite_activity_score))

# Add a new favorite activity
payana_profile_favorite_activities_preference = bigtable_constants.payana_profile_favorite_activities_preference
new_favorite_activity = "spring_break"
new_favorite_activity_score = "7"
profile_table_favorite_activity_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_favorite_activities_preference, new_favorite_activity, new_favorite_activity_score)
payana_profile_read_obj.insert_column(profile_table_favorite_activity_write_object)
profile_table_favorite_activity_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_activity_score = profile_table_favorite_activity_score_update[profile_id][
    payana_profile_favorite_activities_preference][new_favorite_activity]

print("Status of update favorite activity operation: " +
      str(new_favorite_activity_score == updated_favorite_activity_score))

# Delete a favorite activity
payana_profile_obj_delete_favorite_activity_status = payana_profile_read_obj.delete_bigtable_row_column(
    profile_table_favorite_activity_write_object)

print("payana_profile_obj_delete_favorite_activity_status: " + str(payana_profile_obj_delete_favorite_activity_status))

profile_table_favorite_activity_delete = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_favorite_activities = profile_table_favorite_activity_delete[profile_id][payana_profile_favorite_activities_preference]

print("Status of delete favorite activity operation: " +
      str(new_favorite_activity not in updated_favorite_activities))


# Change thumbnail friend rating
payana_profile_table_thumbnail_travel_buddies = bigtable_constants.payana_profile_table_thumbnail_travel_buddies
favorite_travel_buddy = "123456"
new_favorite_travel_buddy_score = "9"
profile_table_favorite_travel_buddy_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_table_thumbnail_travel_buddies, favorite_travel_buddy, new_favorite_travel_buddy_score)
payana_profile_read_obj.insert_column(profile_table_favorite_travel_buddy_write_object)
profile_table_favorite_travel_buddy_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_travel_buddy_score = profile_table_favorite_travel_buddy_score_update[profile_id][
    payana_profile_table_thumbnail_travel_buddies][favorite_travel_buddy]

print("Status of update favorite travel buddy score operation: " +
      str(new_favorite_travel_buddy_score == updated_favorite_travel_buddy_score))

# Add a new thumbnail friend
payana_profile_table_thumbnail_travel_buddies = bigtable_constants.payana_profile_table_thumbnail_travel_buddies
new_favorite_travel_buddy = "654321"
new_favorite_travel_buddy_score = "8"
profile_table_favorite_travel_buddy_write_object = bigtable_write_object_wrapper(
    profile_id, payana_profile_table_thumbnail_travel_buddies, new_favorite_travel_buddy, new_favorite_travel_buddy_score)
payana_profile_read_obj.insert_column(profile_table_favorite_travel_buddy_write_object)
profile_table_favorite_travel_buddy_score_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)
updated_favorite_travel_buddy_score = profile_table_favorite_travel_buddy_score_update[profile_id][
    payana_profile_table_thumbnail_travel_buddies][new_favorite_travel_buddy]

print("Status of update favorite travel buddy score operation: " +
      str(new_favorite_travel_buddy_score == updated_favorite_travel_buddy_score))

# Delete a thumbnail friend
payana_profile_obj_delete_favorite_travel_buddy_status = payana_profile_read_obj.delete_bigtable_row_column(
    profile_table_favorite_travel_buddy_write_object)

print("payana_profile_obj_delete_favorite_travel_buddy_status: " + str(payana_profile_obj_delete_favorite_travel_buddy_status))

profile_table_favorite_travel_buddy_delete = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)

updated_favorite_travel_buddies = profile_table_favorite_travel_buddy_delete[profile_id][payana_profile_table_thumbnail_travel_buddies]

print("Status of delete favorite travel buddy operation: " +
      str(new_favorite_travel_buddy not in updated_favorite_travel_buddies))

# Remove the whole profile ID row
profile_row_delete_object = bigtable_write_object_wrapper(
    profile_id, "", "", "")
payana_profile_read_obj.delete_bigtable_row(profile_row_delete_object)

profile_obj_read_activity_update = payana_profile_read_obj.get_row_dict(
    profile_id, include_column_family=True)

print("Status of profile obj delete row:" +
      str(len(profile_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
