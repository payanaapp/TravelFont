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

from urllib import response
import requests
import json

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family

# generic activity write objects
payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value
payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value
payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value
payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value
payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value
payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value
payana_profile_page_itinerary_table_activities = bigtable_constants.payana_profile_page_itinerary_table_activities
payana_profile_table_profile_id = bigtable_constants.payana_profile_table_profile_id


saved_itinerary_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value])

saved_excursion_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value])

created_itinerary_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value])

created_excursion_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value])

created_activity_guide_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value])

created_activity_guide_id_list_activity_generic_column_family_id = "_".join(
    [activity_generic_column_family_id, payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value])

# POST profile info
# CURL request
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "profile_id": "123456",
    "saved_itinerary_id_list": ["12345"],
    "saved_excursion_id_list": ["12345"],
    "saved_activity_guide_id_list": ["12345"],
    "created_itinerary_id_list": ["12345"],
    "created_activity_guide_id_list": ["12345"],
    "created_excursion_id_list": ["12345"],
    "saved_itinerary_id_mapping": {"12345": "itinerary_name_one"},
    "saved_excursion_id_mapping": {"12345": "excursion_name_one"},
    "saved_activity_guide_id_mapping": {"12345": "activity_guide_name_one"},
    "created_itinerary_id_mapping": {"12345": "itinerary_name_one"},
    "created_activity_guide_id_mapping": {"12345": "activity_guide_name_one"},
    "created_excursion_id_mapping": {"12345": "excursion_name_one"},
    "activities": ["generic", "hiking", "romantic", "exotic"]
}'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"

profile_page_itinerary_json = {
    payana_profile_table_profile_id: "123456",
    payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value: ["12345"],
    payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value: ["12345"],
    payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value: ["12345"],
    payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value: ["12345"],
    payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value: ["12345"],
    payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value: ["12345"],
    "saved_itinerary_id_mapping": {"12345": "itinerary_name_one"},
    "saved_excursion_id_mapping": {"12345": "excursion_name_one"},
    "saved_activity_guide_id_mapping": {"12345": "activity_guide_name_one"},
    "created_itinerary_id_mapping": {"12345": "itinerary_name_one"},
    "created_activity_guide_id_mapping": {"12345": "activity_guide_name_one"},
    "created_excursion_id_mapping": {"12345": "excursion_name_one"},
    payana_profile_page_itinerary_table_activities: [
        "generic", "hiking", "romantic", "exotic"]
}


headers = {'Content-Type': 'application/json',
           payana_profile_table_profile_id: profile_page_itinerary_json[payana_profile_table_profile_id]}

response = requests.post(url, data=json.dumps(
    profile_page_itinerary_json), headers=headers)


print("Profile Page Itinerary Object creation status: " +
      str(response.status_code == 201))

profile_page_itinerary_response_json = response.json()

profile_id = profile_page_itinerary_response_json['profile_id']

print("Profile Page Itinerary creation verification status: " +
      str(profile_id is not None and len(profile_id) > 0))

# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_page_itinerary_response = response.json()
print("Profile Page Itinerary creation verification status: " +
      str(len(profile_page_itinerary_response[profile_id]
          [created_activity_guide_id_list_activity_generic_column_family_id]) == 1))


# Edit itinerary id list -- add a new one
"""
curl --location --request PUT 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "profile_id": "123456",
    "saved_itinerary_id_list": ["123456"],
    "saved_excursion_id_list": ["123456"],
    "saved_activity_guide_id_list": ["123456"],
    "created_itinerary_id_list": ["123456"],
    "created_activity_guide_id_list": ["123456"],
    "created_excursion_id_list": ["123456"],
    "saved_itinerary_id_mapping": {"12345": "itinerary_name_two"},
    "saved_excursion_id_mapping": {"12345": "excursion_name_two"},
    "saved_activity_guide_id_mapping": {"12345": "activity_guide_name_two"},
    "created_itinerary_id_mapping": {"12345": "itinerary_name_two"},
    "created_activity_guide_id_mapping": {"12345": "activity_guide_name_two"},
    "created_excursion_id_mapping": {"12345": "excursion_name_two"},
    "activities": ["generic", "hiking", "romantic", "exotic"]
}'
"""
profile_page_itinerary_json = {
    payana_profile_table_profile_id: "123456",
    payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value: ["123456"],
    payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value: ["123456"],
    payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value: ["123456"],
    payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value: ["123456"],
    payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value: ["123456"],
    payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value: ["123456"],
    "saved_itinerary_id_mapping": {"12345": "itinerary_name_two"},
    "saved_excursion_id_mapping": {"12345": "excursion_name_two"},
    "saved_activity_guide_id_mapping": {"12345": "activity_guide_name_two"},
    "created_itinerary_id_mapping": {"12345": "itinerary_name_two"},
    "created_activity_guide_id_mapping": {"12345": "activity_guide_name_two"},
    "created_excursion_id_mapping": {"12345": "excursion_name_two"},
    payana_profile_page_itinerary_table_activities: [
        "generic", "hiking", "romantic", "exotic"]
}


headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_page_itinerary_json), headers=headers)

print("Profile Page Itinerary update status: " +
      str(response.status_code == 200))


# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_page_itinerary_response = response.json()
print("Profile Page Itinerary update verification status: " +
      str(len(profile_page_itinerary_response[profile_id]
          [created_activity_guide_id_list_activity_generic_column_family_id]) == 2))

# Delete specific column family and column values
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/itineraries/delete/values/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "exotic_created_activity_guide_id_list": {
            "1674896220": "12345"
        }
}'
"""

url = "http://127.0.0.1:8888/profile/itineraries/delete/values/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

key, value = list(profile_page_itinerary_response[profile_id]
                  [created_activity_guide_id_list_activity_generic_column_family_id].items())[0]

profile_page_itineraries_column_value_delete_json = {
    created_activity_guide_id_list_activity_generic_column_family_id: {key: value}}

response = requests.post(url, data=json.dumps(
    profile_page_itineraries_column_value_delete_json), headers=headers)

print("Profile page itineraries contents column values delete status: " +
      str(response.status_code == 200))


# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_page_itinerary_response = response.json()
print("Profile Page Itinerary deletion column values verification status: " +
      str(len(profile_page_itinerary_response[profile_id]
          [created_activity_guide_id_list_activity_generic_column_family_id]) == 1))

# Delete created_activity_guide_id_list_activity_generic_column_family_id - entire column family
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/itineraries/delete/cf/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "exotic_created_activity_guide_id_list": "",
    "exotic_created_excursion_id_list": ""
}'
"""
url = "http://127.0.0.1:8888/profile/itineraries/delete/cf/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

profile_page_itinerary_delete_cf_json = {
    created_itinerary_id_list_activity_generic_column_family_id: "",
    created_excursion_id_list_activity_generic_column_family_id: ""
}

response = requests.post(url, data=json.dumps(
    profile_page_itinerary_delete_cf_json), headers=headers)

print("Profile page itinerary contents column family delete status: " +
      str(response.status_code == 200))


# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_page_itinerary_response = response.json()
print("Profile Page Itinerary column family deletion verification status: " +
      str(saved_excursion_id_list_activity_generic_column_family_id in profile_page_itinerary_response[profile_id] and created_itinerary_id_list_activity_generic_column_family_id not in profile_page_itinerary_response[profile_id] and created_excursion_id_list_activity_generic_column_family_id not in profile_page_itinerary_response[profile_id]))


# Delete profile info
"""
curl --location --request DELETE 'http://127.0.0.1:8888/profile/itineraries/delete/' \
--header 'profile_id: 123456'
"""
url = "http://127.0.0.1:8888/profile/itineraries/delete/"
headers = {'profile_id': profile_id}

response = requests.delete(url, headers=headers)

print("Profile page itineraries row delete status: " +
      str(response.status_code == 200))


# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile Page Itinerary row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
