from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTravelFootPrintTable import PayanaProfileTravelFootPrintTable
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

payana_travel_buddy_table_column_family_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_travel_buddy_list
payana_travel_buddy_table_column_family_favorite_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_favorite_travel_buddy_list
payana_travel_buddy_table_column_family_top_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_top_travel_buddy_list
payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list
payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list
payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list = bigtable_constants.payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list

payana_travel_buddy_table_column_family_profile_id = bigtable_constants.payana_travel_buddy_table_column_family_profile_id
payana_travel_buddy_table_column_family_travel_buddy_profile_id = bigtable_constants.payana_travel_buddy_table_column_family_travel_buddy_profile_id
payana_travel_buddy_table_column_family_global_influencer = bigtable_constants.payana_travel_buddy_table_column_family_global_influencer
payana_travel_buddy_table_column_family_favorite = bigtable_constants.payana_travel_buddy_table_column_family_favorite
payana_travel_buddy_table_column_family_sent_pending_request = bigtable_constants.payana_travel_buddy_table_column_family_sent_pending_request
payana_travel_buddy_table_column_family_received_pending_request = bigtable_constants.payana_travel_buddy_table_column_family_received_pending_request


# POST write
# CURL request
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567' \
--data '{
    "profile_id": "1234567",
    "travel_buddy_profile_id": "456789",
    "global_influencer": false,
    "favorite": false,
    "sent_pending_request": true,
    "received_pending_request": true,
    "new_friend_request": true
}'
"""

url = "http://localhost:8888/profile/travelbuddy/"

profile_travel_buddy_json = {
    "profile_id": "1234567",
    "travel_buddy_profile_id": "456789",
    "global_influencer": False,
    "favorite": False,
    "sent_pending_request": True,
    "received_pending_request": True,
    "new_friend_request": True
}

travel_buddy_profile_id = "456789"

profile_id = profile_travel_buddy_json[payana_travel_buddy_table_column_family_profile_id]

headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_travel_buddy_json), headers=headers)


print("Profile travel buddy object creation status: " +
      str(response.status_code == 201))

profile_info_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567'
"""

url = "http://localhost:8888/profile/travelbuddy/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel buddy read status: " + str(response.status_code == 200))

profile_travel_buddy_response = response.json()

print("Profile travel buddy creation verification status: " +
      str(travel_buddy_profile_id in profile_travel_buddy_response[profile_id][payana_travel_buddy_table_column_family_travel_buddy_list]))


# Edit travel buddy object
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567' \
--data '{
    "profile_id": "1234567",
    "travel_buddy_profile_id": "456789123",
    "global_influencer": false,
    "favorite": false,
    "sent_pending_request": true,
    "received_pending_request": true,
    "new_friend_request": true
}'
"""
profile_travel_buddy_json = {
    "profile_id": "1234567",
    "travel_buddy_profile_id": "456789123",
    "global_influencer": False,
    "favorite": False,
    "sent_pending_request": True,
    "received_pending_request": True,
    "new_friend_request": True
}

new_travel_buddy_profile_id = "456789123"

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_travel_buddy_json), headers=headers)

print("Profile travel buddy update status: " + str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567'
"""

url = "http://localhost:8888/profile/travelbuddy/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel buddy update read status: " + str(response.status_code == 200))

profile_travel_buddy_response = response.json()

print("Profile travel buddy update read verification status: " +
      str(new_travel_buddy_profile_id in profile_travel_buddy_response[profile_id][payana_travel_buddy_table_column_family_travel_buddy_list]))

# Delete specific column family and column values
"""
curl --location 'http://localhost:8888/profile/travelbuddy/delete/values/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567' \
--data '{
    "payana_travel_buddy_list": {
        "456789": "1684481568.048925"
    }
}'
"""
url = "http://localhost:8888/profile/travelbuddy/delete/values/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

profile_travel_buddy_delete_cv_json = {
    "payana_travel_buddy_list": {
        new_travel_buddy_profile_id: ""
    }
}

response = requests.post(url, data=json.dumps(
    profile_travel_buddy_delete_cv_json), headers=headers)

print("Profile travel buddy contents column values delete status: " +
      str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567'
"""

url = "http://localhost:8888/profile/travelbuddy/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel buddy read status: " + str(response.status_code == 200))

profile_travel_buddy_response = response.json()

print("Profile travel buddy delete CV verification status: " +
      str(new_travel_buddy_profile_id not in profile_travel_buddy_response[profile_id][payana_travel_buddy_table_column_family_travel_buddy_list]))

# Delete entire column family
"""
curl --location 'http://localhost:8888/profile/travelbuddy/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567' \
--data '{
    "payana_travel_buddy_list": ""
}'
"""

url = "http://localhost:8888/profile/travelbuddy/delete/cf/"

headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

profile_travel_buddy_delete_cf_json = {
    "payana_travel_buddy_list": ""
}

response = requests.post(url, data=json.dumps(
    profile_travel_buddy_delete_cf_json), headers=headers)

print("Profile travel buddy column family delete status: " +
      str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567'
"""

url = "http://localhost:8888/profile/travelbuddy/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel buddy read status: " + str(response.status_code == 200))

profile_travel_buddy_response = response.json()

print("Profile travel buddy creation verification status: " +
      str(payana_travel_buddy_table_column_family_travel_buddy_list not in profile_travel_buddy_response[profile_id]))


# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/profile/travelbuddy/delete/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 1234567'
"""

url = "http://localhost:8888/profile/travelbuddy/delete/"
headers = {payana_travel_buddy_table_column_family_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Profile travel buddy row delete status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelbuddy/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelbuddy/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile travel buddy row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
