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

payana_profile_page_travel_footprint_profile_id = bigtable_constants.payana_profile_page_travel_footprint_profile_id
payana_profile_page_travel_footprint_place_id = bigtable_constants.payana_profile_page_travel_footprint_place_id
payana_profile_page_travel_footprint_excursion_id = bigtable_constants.payana_profile_page_travel_footprint_excursion_id
payana_profile_page_travel_footprint_latitude = bigtable_constants.payana_profile_page_travel_footprint_latitude
payana_profile_page_travel_footprint_longitude = bigtable_constants.payana_profile_page_travel_footprint_longitude
payana_profile_page_travel_footprint_column_family = bigtable_constants.payana_profile_page_travel_footprint_column_family
payana_profile_travel_footprint_obj_list = bigtable_constants.payana_profile_travel_footprint_obj_list

# POST profile travel footprint
# CURL request
"""
curl --location --request POST 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "travelfont_obj_list": [
        {
            "excursion_id": "678910",
            "latitude": "1.234",
            "longitude": "2.3456",
            "place_id": "123456"
        }
    ]
}'
"""

url = "http://localhost:8888/profile/travelfont/"

profile_travel_footprint_json = {
    payana_profile_page_travel_footprint_profile_id: "123456789",
    payana_profile_travel_footprint_obj_list: [
        {
            payana_profile_page_travel_footprint_excursion_id: "678910",
            payana_profile_page_travel_footprint_latitude: "1.234",
            payana_profile_page_travel_footprint_longitude: "2.3456",
            payana_profile_page_travel_footprint_place_id: "12345"
        }
    ]
}

profile_id = profile_travel_footprint_json[payana_profile_page_travel_footprint_profile_id]

headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_travel_footprint_json), headers=headers)


print("Profile travel footprint creation status: " + str(response.status_code == 201))

profile_info_response_json = response.json()

# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_travel_footprint_response = response.json()

print("Profile travel footprint creation verification status: " +
      str(len(profile_travel_footprint_response[payana_profile_travel_footprint_obj_list]) == 1))


# Edit travel footprint object
"""
curl --location --request PUT 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "travelfont_obj_list": [
        {
            "excursion_id": "678910",
            "latitude": "1.2345",
            "longitude": "2.3456",
            "place_id": "12345"
        }
    ]
}'
"""
profile_travel_footprint_json = {
    payana_profile_page_travel_footprint_profile_id: "123456789",
    payana_profile_travel_footprint_obj_list: [
        {
            payana_profile_page_travel_footprint_excursion_id: "678910",
            payana_profile_page_travel_footprint_latitude: "1.234",
            payana_profile_page_travel_footprint_longitude: "2.3456",
            payana_profile_page_travel_footprint_place_id: "123456"
        }
    ]
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_travel_footprint_json), headers=headers)

print("Profile travel footprint update status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile update read status: " + str(response.status_code == 200))

profile_travel_footprint_response = response.json()

print("Profile travel footprint update verification status: " +
      str(len(profile_travel_footprint_response[payana_profile_travel_footprint_obj_list]) == 2))

# Delete specific column family and column values
"""
curl --location --request POST 'http://localhost:8888/profile/travelfont/delete/values/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "travelfont_obj_list": [
        {
            "excursion_id": "678910",
            "latitude": "1.2345",
            "longitude": "2.3456",
            "place_id": "12345"
        }
    ]
}'
"""
url = "http://localhost:8888/profile/travelfont/delete/values/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

profile_travel_footprint_delete_cv_json = {
    payana_profile_travel_footprint_obj_list: [
        {
            payana_profile_page_travel_footprint_excursion_id: "678910",
            payana_profile_page_travel_footprint_latitude: "1.234",
            payana_profile_page_travel_footprint_longitude: "2.3456",
            payana_profile_page_travel_footprint_place_id: "12345"
        }
    ]
}

response = requests.post(url, data=json.dumps(
    profile_travel_footprint_delete_cv_json), headers=headers)

print("Profile travel footprint contents column values delete status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile travel footprint column value post delete read status: " + str(response.status_code == 200))

profile_travel_footprint_response = response.json()

print("Profile travel footprint column value deleteion verification status: " +
      str(len(profile_travel_footprint_response[payana_profile_travel_footprint_obj_list]) == 1))

# Delete entire column family
"""
curl --location --request POST 'http://localhost:8888/profile/travelfont/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/delete/cf/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.post(url, headers=headers)

print("Profile travel footprint column family delete status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel footprint column family delete status: " + str(response.status_code == 400))


# POST profile info
# CURL request
"""
curl --location --request POST 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "travelfont_obj_list": [
        {
            "excursion_id": "678910",
            "latitude": "1.234",
            "longitude": "2.3456",
            "place_id": "123456"
        }
    ]
}'
"""

url = "http://localhost:8888/profile/travelfont/"

profile_travel_footprint_json = {
    payana_profile_page_travel_footprint_profile_id: "123456789",
    payana_profile_travel_footprint_obj_list: [
        {
            payana_profile_page_travel_footprint_excursion_id: "678910",
            payana_profile_page_travel_footprint_latitude: "1.234",
            payana_profile_page_travel_footprint_longitude: "2.3456",
            payana_profile_page_travel_footprint_place_id: "12345"
        }
    ]
}

profile_id = profile_travel_footprint_json[payana_profile_page_travel_footprint_profile_id]

headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_travel_footprint_json), headers=headers)


print("Profile travel footprint creation status: " + str(response.status_code == 201))

profile_info_response_json = response.json()

# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_travel_footprint_response = response.json()

print("Profile travel footprint creation verification status: " +
      str(len(profile_travel_footprint_response[payana_profile_travel_footprint_obj_list]) == 1))

# Delete profile travel footprint row
"""
curl --location --request DELETE 'http://localhost:8888/profile/travelfont/delete/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/delete/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Profile travelfootprint row delete status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://localhost:8888/profile/travelfont/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/profile/travelfont/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile travelfootprint row delete status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
