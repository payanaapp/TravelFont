import time
import copy
import os
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
from payana.payana_bl.cloud_storage_utils.payana_upload_storage_object import payana_upload_storage_object
from payana.payana_bl.cloud_storage_utils.payana_download_storage_object import payana_download_storage_object
from payana.payana_bl.bigtable_utils.PayanaGlobalCityTimestampItineraryTable import PayanaGlobalCityTimestampItineraryTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
from payana.payana_bl.bigtable_utils.PayanaActivityGuideThumbNailTable import PayanaActivityGuideThumbNailTable
from payana.payana_bl.bigtable_utils.PayanaCitiesAutocompleteTable import PayanaCitiesAutocompleteTable
from payana.payana_bl.bigtable_utils.PayanaUsersAutocompleteTable import PayanaUsersAutocompleteTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

# Step 2 in payana_homepage_flow.txt

# add a neighboring city obj
neighboring_cities_obj = {
    "city": "sanfrancisco##california##usa",
    "neighboring_city_list": {
        "sanfrancisco##california##usa": "77.78"
    }
}

payana_neighboring_cities_obj = PayanaNeighboringCitiesTable(
    **neighboring_cities_obj)
payana_neighboring_cities_obj_write_status = payana_neighboring_cities_obj.update_neighboring_city_list_bigtable()

print("payana_neighboring_cities_obj_write_status: " +
      str(payana_neighboring_cities_obj_write_status))

payana_neighboring_cities_table = bigtable_constants.payana_neighboring_cities_table
city = payana_neighboring_cities_obj.city
payana_neighboring_cities_read_obj = PayanaBigTable(
    payana_neighboring_cities_table)
payana_neighboring_cities_get_obj = payana_neighboring_cities_read_obj.get_row_dict(
    city, include_column_family=True)
print(payana_neighboring_cities_get_obj)

# Step 3A in payana_homepage_flow.txt

# 3A1 - Create Excursion and activity guide objects
excursion_obj_1 = {
    "checkin_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "image_id_list": {
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "45678",
        "3A": "23456",
        "3B": "56789"
    },
    "cities_checkin_id_list": {
        "1": "cupertino##california##usa",
        "2": "sanfrancisco##california##usa",
        "3": "santaclara##california##usa"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "romantic": "6"},
    "excursion_metadata": {
        "excursion_id": "12345",
        "activity_guide": "False",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "description": "My excursion 1",
        "itinerary_id": "1234678",
        "itinerary_name": "My itinerary 1",
        "place_name": "Land'\''s End",
        "city": "sanfrancisco##California##USA",
        "state": "California##USA",
        "country": "USA",
        "excursion_object_position_itinerary": "1",
        "excursion_clone_parent_id": ""
    }
}

excursion_obj_2 = copy.deepcopy(excursion_obj_1)
excursion_obj_2["excursion_metadata"]["excursion_id"] = "23456"
excursion_obj_2["excursion_metadata"]["excursion_object_position_itinerary"] = "2"
excursion_obj_2["excursion_metadata"]["description"] = "My excursion 2"

excursion_obj_3 = copy.deepcopy(excursion_obj_1)
excursion_obj_3["excursion_metadata"]["excursion_id"] = "34567"
excursion_obj_3["excursion_metadata"]["excursion_object_position_itinerary"] = "3"
excursion_obj_3["excursion_metadata"]["description"] = "My excursion 3"

activity_guide_1 = copy.deepcopy(excursion_obj_1)
activity_guide_1["excursion_metadata"]["excursion_id"] = "45678"
activity_guide_1["excursion_metadata"]["activity_guide"] = "True"
activity_guide_1["excursion_metadata"]["excursion_object_position_itinerary"] = "1"
activity_guide_1["excursion_metadata"]["itinerary_id"] = "2345678910"
activity_guide_1["excursion_metadata"]["description"] = "My activity guide 1"
activity_guide_1["excursion_metadata"]["itinerary_name"] = "My itinerary 2"

activity_guide_2 = copy.deepcopy(excursion_obj_1)
activity_guide_2["excursion_metadata"]["excursion_id"] = "56789"
activity_guide_2["excursion_metadata"]["activity_guide"] = "True"
activity_guide_2["excursion_metadata"]["excursion_object_position_itinerary"] = "2"
activity_guide_2["excursion_metadata"]["itinerary_id"] = "34567891011"
activity_guide_2["excursion_metadata"]["description"] = "My activity guide 2"
activity_guide_2["excursion_metadata"]["itinerary_name"] = "My itinerary 2"

activity_guide_3 = copy.deepcopy(excursion_obj_1)
activity_guide_3["excursion_metadata"]["excursion_id"] = "678910"
activity_guide_3["excursion_metadata"]["activity_guide"] = "True"
activity_guide_3["excursion_metadata"]["excursion_object_position_itinerary"] = "3"
activity_guide_3["excursion_metadata"]["itinerary_id"] = "456789101112"
activity_guide_3["excursion_metadata"]["description"] = "My activity guide 3"
activity_guide_3["excursion_metadata"]["itinerary_name"] = "My itinerary 2"

excursion_object_list = [excursion_obj_1, excursion_obj_2,
                         excursion_obj_3, activity_guide_1, activity_guide_2, activity_guide_3]

for excursion_obj in excursion_object_list:
    payana_excursion_obj = PayanaExcursionTable(**excursion_obj)
    payana_excursion_obj_write_status = payana_excursion_obj.update_excursion_bigtable()

    print("Payana excursion object write status: " +
          str(payana_excursion_obj_write_status))

    excursion_id = payana_excursion_obj.excursion_id

    payana_excursion_table = bigtable_constants.payana_excursion_table
    payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)
    excursion_obj_read = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)

    print(excursion_obj_read)

    print("Addition of a new excursion object: " +
          str(excursion_obj_read[excursion_id]["excursion_metadata"]["excursion_id"] == excursion_id))

excursion_id_list = ["12345", "23456", "34567"]
activity_guide_list = ["45678", "56789", "678910"]

# 3A2 - Create Itinerary objects and add excursion/activity guide metadata
payana_itinerary_object_one = {
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {"hiking": "1.0", "romantic": "1.0"},
    "itinerary_metadata": {
        "description": "My itinerary 1",
        "visit_timestamp": "123456789",
        "itinerary_id": "456789101112",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "sanfrancisco##California##USA",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "12345678",  # city: place_id
        "santaclara##california##usa": "12345678"
    }
}

payana_itinerary_object_two = {
    "excursion_id_list": {
        "1": "45678",
        "2": "56789",
        "3": "678910"
    },
    "activities_list": {"hiking": "1.0", "romantic": "1.0"},
    "itinerary_metadata": {
        "description": "My itinerary 2",
        "visit_timestamp": "123456789",
        "itinerary_id": "12345678",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "sanfrancisco##California##USA",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "12345678",  # city: place_id
        "santaclara##california##usa": "12345678"
    }
}

itinerary_object_list = [
    payana_itinerary_object_one, payana_itinerary_object_two]

# 3A3 - Create Check In objects
for itinerary_obj in itinerary_object_list:
    payana_itinerary_obj = PayanaItineraryTable(**itinerary_obj)

    payana_itinerary_obj_write_status = payana_itinerary_obj.update_itinerary_bigtable()
    print("payana_itinerary_obj_write_status: " +
          str(payana_itinerary_obj_write_status))

    itinerary_id = payana_itinerary_obj.itinerary_id
    payana_itinerary_table = bigtable_constants.payana_itinerary_table
    payana_itinerary_read_obj = PayanaBigTable(payana_itinerary_table)
    itinerary_obj_read = payana_itinerary_read_obj.get_row_dict(
        itinerary_id, include_column_family=True)
    print(itinerary_obj_read)

    print("Addition of a new itinerary object: " +
          str(itinerary_obj_read != None))

# 3A4 - Upload Google cloud images
# upload a blob
gcs_payana_itinerary_pictures_bucket_name = bigtable_constants.payana_gcs_profile_pictures

itinerary_picture_bucket_name_list = {"12345": "fishermans_wharf.jpg", "34567": "golden_gate_night.jpg", "23456": "golden-gate-bridge-sf.jpg",
                                      "45678": "fishermans_wharf.jpg", "23456": "golden_gate_night.jpg", "56789": "golden-gate-bridge-sf.jpg"}

for itinerary_picture_bucket_name, image_path in itinerary_picture_bucket_name_list.items():
    payana_gcs_image_upload_path = os.path.join(
        bigtable_constants.travelfont_home, image_path)

    payana_profile_picture_upload_storage_object_status = payana_upload_storage_object(
        gcs_payana_itinerary_pictures_bucket_name, payana_gcs_image_upload_path, itinerary_picture_bucket_name)

    print("Payana Profile Picture Upload Storage Object Status: " +
          str(payana_profile_picture_upload_storage_object_status))

    payana_gcs_image_download_path = os.path.join(
        bigtable_constants.travelfont_home, "downloaded_" + image_path)

    # download a blob
    payana_profile_picture_download_storage_object_status = payana_download_storage_object(
        gcs_payana_itinerary_pictures_bucket_name, itinerary_picture_bucket_name, payana_gcs_image_download_path)

# 3A5 - Write into the payana_global_city_timestamp_itinerary
current_timestamp_unix = int(time.time())

global_city_itinerary_obj = {
    "city": "sanfrancisco##california##usa",
    "itinerary_id": {
    },
    "excursion_id": {
        excursion_id: str(current_timestamp_unix + index) for index, excursion_id in enumerate(excursion_id_list)
    },
    "activity_guide_id": {
        activity_guide_id: str(current_timestamp_unix + 2 * index) for index, activity_guide_id in enumerate(activity_guide_list)
    },
    "activities": [
        "generic",
        "hiking",
        "romantic"
    ]
}

payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value = bigtable_constants.payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value

payana_global_city_itinerary_obj = PayanaGlobalCityTimestampItineraryTable(
    **global_city_itinerary_obj)

payana_global_city_itinerary_obj_write_status = payana_global_city_itinerary_obj.update_global_city_itinerary_bigtable()
print("payana_global_city_itinerary_obj write status: " +
      str(payana_global_city_itinerary_obj_write_status))

payana_global_city_itinerary_table = bigtable_constants.payana_global_city_itinerary_table

row_id = payana_global_city_itinerary_obj.row_id
payana_global_city_itinerary_read_obj = PayanaBigTable(
    payana_global_city_itinerary_table)
payana_global_city_itinerary_read_row_obj = payana_global_city_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print(payana_global_city_itinerary_read_row_obj)

print("Status of add global city itinerary: " +
      str(payana_global_city_itinerary_read_row_obj is not None))

# 3A6 - Write into profile itinerary objects
profile_page_itinerary_obj = {
    "profile_id": "1234567",
    "saved_itinerary_id_mapping": {"My itinerary 1": "456789101112", "My itinerary 2": "12345678"},
    "saved_excursion_id_mapping": {"My excursion 1": "12345", "My excursion 2": "23456", "My excursion 3": "34567"},
    "saved_activity_guide_id_mapping": {"My activity guide 1": "45678", "My activity guide 2": "56789", "My activity guide 3": "678910"},
    "created_itinerary_id_mapping": {"My itinerary 1": "456789101112", "My itinerary 2": "12345678"},
    "created_activity_guide_id_mapping": {"My activity guide 1": "45678", "My activity guide 2": "56789", "My activity guide 3": "678910"},
    "created_excursion_id_mapping": {"My excursion 1": "12345", "My excursion 2": "23456", "My excursion 3": "34567"},
    "activities": ["generic", "hiking", "romantic"]
}

payana_profile_page_itinerary_obj = PayanaProfilePageItineraryTable(
    **profile_page_itinerary_obj)
payana_profile_page_itinerary_obj_write_status = payana_profile_page_itinerary_obj.update_payana_profile_page_itinerary_bigtable()

print("payana_profile_page_itinerary_obj_write_status: " +
      str(payana_profile_page_itinerary_obj_write_status))

payana_profile_page_itinerary_table = bigtable_constants.payana_profile_page_itinerary_table

row_id = payana_profile_page_itinerary_obj.row_id
payana_profile_page_itinerary_read_obj = PayanaBigTable(
    payana_profile_page_itinerary_table)
payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(
    row_id, include_column_family=True)

print(payana_profile_page_itinerary_read_row_obj)

print("Status of add payana_profile_page itinerary: " +
      str(payana_profile_page_itinerary_read_row_obj is not None))

# Step 3B in payana_homepage_flow.txt

# 3B1 - Write Thumbnail activity metadata
payana_activity_thumbnail = bigtable_constants.payana_activity_thumbnail
payana_activity_guide_thumbnail_table = bigtable_constants.payana_activity_guide_thumbnail_table
payana_activity_thumbnail_city = bigtable_constants.payana_activity_thumbnail_city

payana_activity_column_family = bigtable_constants.payana_activity_column_family
payana_activity_column_family.remove("generic")

payana_activity_thumbnail_obj = {
    payana_activity_thumbnail: {
        activity: {
            "12345": str(current_timestamp_unix)  # image ID: timestamp
        } for activity in bigtable_constants.payana_activity_column_family
    },
    payana_activity_thumbnail_city: "sanfrancisco##california##usa"
}

print(payana_activity_thumbnail_obj)

city = payana_activity_thumbnail_obj[payana_activity_thumbnail_city]

payana_activity_thumbnail_obj = PayanaActivityGuideThumbNailTable(
    **payana_activity_thumbnail_obj)
payana_activity_thumbnail_obj_write_status = payana_activity_thumbnail_obj.update_activity_guide_thumbnail_bigtable()

print("payana_activity_thumbnail_obj_write_status: " +
      str(payana_activity_thumbnail_obj_write_status))

activity_one = "_".join(["hiking", payana_activity_thumbnail])
activity_two = "_".join(["romantic", payana_activity_thumbnail])

payana_activity_thumbnail_obj = PayanaBigTable(
    payana_activity_guide_thumbnail_table)

payana_activity_thumbnail_obj_read = payana_activity_thumbnail_obj.get_row_dict(
    city, include_column_family=True)
print(payana_activity_thumbnail_obj_read)

print("Addition of a new activity thumbnail object: " +
      str(payana_activity_thumbnail_obj_read != None))


# 3B2 - Upload GCS images
# Already done

# Step 4A in payana_homepage_flow.txt

# 4A1 - autocomplete city name write
# Add travel buddy objects for a city and also by name
autocomplete_cities_obj = {
    "payana_autocomplete_cities_list": {
        "cupertino##california##usa": "156",
        "santaclara##california##usa": "789",
        "seattle##washington##usa": "8678",
        "sanjuan##xyz##puertorico": "1457",
        "sanfrancisco##california##usa": "123",
        "zainzibar": "1234"
    }
}

payana_autocomplete_cities_obj = PayanaCitiesAutocompleteTable(
    **autocomplete_cities_obj)
payana_autocomplete_cities_obj_write_status = payana_autocomplete_cities_obj.update_autocomplete_city_list_bigtable()

print("payana_autocomplete_cities_obj_write_status: " +
      str(payana_autocomplete_cities_obj_write_status))
payana_autocomplete_cities_table = bigtable_constants.payana_city_autocomplete_table
city = bigtable_constants.payana_city_autocomplete_row_key
payana_autocomplete_cities_read_obj = PayanaBigTable(
    payana_autocomplete_cities_table)
print(payana_autocomplete_cities_read_obj.get_row_dict(
    city, include_column_family=True))

# Step 7B1, 7B2 in payana_homepage_flow.txt

# 7B1
travel_buddy_obj_one = {
    "profile_id": "1234567",
    "profile_name": "abkr",
    "travel_buddy_profile_name": "abhinandankr",
    "travel_buddy_profile_id": "456789",
    "global_influencer": True,  # flag for global influencer or not
    "favorite": True,  # a flag to mark a travel buddy favorite
    # adding into your pending approval requests for the requests that you sent
    "sent_pending_request": True,
    # adding into your received approval requests for the requests that you sent
    "received_pending_request": True,
    "new_friend_request": True  # marking whether a new friend request is sent out or not
}

travel_buddy_obj_two = copy.deepcopy(travel_buddy_obj_one)
travel_buddy_obj_two["travel_buddy_profile_name"] = "bob"
travel_buddy_obj_two["travel_buddy_profile_id"] = "456789"

travel_buddy_obj_three = copy.deepcopy(travel_buddy_obj_one)
travel_buddy_obj_three["travel_buddy_profile_name"] = "zain"
travel_buddy_obj_three["travel_buddy_profile_id"] = "5678910"

travel_buddy_obj_four = copy.deepcopy(travel_buddy_obj_one)
travel_buddy_obj_four["travel_buddy_profile_name"] = "carter"
travel_buddy_obj_four["travel_buddy_profile_id"] = "67891011"

travel_buddy_objects = [travel_buddy_obj_one, travel_buddy_obj_two,
                        travel_buddy_obj_three, travel_buddy_obj_four]

# Adding a travel buddy
for travel_buddy_obj in travel_buddy_objects:
    payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj)

    payana_travel_buddy_obj_write_status = payana_travel_buddy_obj.update_travel_buddy_bigtable()
    print("payana_travel_buddy_obj_write_status: " +
          str(payana_travel_buddy_obj_write_status))

    payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
    profile_id = payana_travel_buddy_obj.profile_id
    travel_buddy_profile_id = payana_travel_buddy_obj.travel_buddy_profile_id
    profile_name = payana_travel_buddy_obj.profile_name
    travel_buddy_profile_name = payana_travel_buddy_obj.travel_buddy_profile_name
    payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)

    payana_profile_id_travel_buddy_obj = payana_travel_buddy_read_obj.get_row_dict(
        profile_id, include_column_family=True)
    print(payana_profile_id_travel_buddy_obj)

# 7B2
autocomplete_users_obj = {
    "city": "sanfrancisco##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",  # user_name: user_id
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457",
        "zain": "6799"
    }
}

payana_autocomplete_users_obj = PayanaUsersAutocompleteTable(
    **autocomplete_users_obj)
payana_autocomplete_users_obj_write_status = payana_autocomplete_users_obj.update_autocomplete_users_list_bigtable()

print("payana_autocomplete_users_obj_write_status: " +
      str(payana_autocomplete_users_obj_write_status))
payana_autocomplete_users_table = bigtable_constants.payana_users_autocomplete_table
city = payana_autocomplete_users_obj.city
payana_autocomplete_users_read_obj = PayanaBigTable(
    payana_autocomplete_users_table)
print(payana_autocomplete_users_read_obj.get_row_dict(
    city, include_column_family=True))

# Steps 7C or 7D
# 7B1 and 7B2 above covers

# Add travel buddy profiles, profile pictures for travel buddy objects in 7B1, 7B2 above
# Do it in travel buddy page
