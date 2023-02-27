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

payana_like_column_family = bigtable_constants.payana_likes_table_column_family
payana_likes_table_entity_id = bigtable_constants.payana_likes_table_entity_id

# POST profile likes
# CURL request
"""
curl --location --request POST 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345' \
--data-raw '{
    "payana_likes": {
        "pf_id_1": "1234567",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    },
    "entity_id": "12345"
}'
"""

url = "http://localhost:8888/entity/likes/"

profile_likes_json = {
    payana_like_column_family: {
        "pf_id_1": "1234567",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    },
    payana_likes_table_entity_id: "12345"
}

entity_id = profile_likes_json[payana_likes_table_entity_id]

headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_likes_json), headers=headers)


print("Profile likes object creation status: " +
      str(response.status_code == 201))

# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana likes read status: " + str(response.status_code == 200))

profile_likes_response = response.json()

print("Profile likes creation verification status: " +
      str(profile_likes_response[entity_id][payana_like_column_family]["pf_id_1"] == "1234567"))


# Edit payana likes object
"""
curl --location --request PUT 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345' \
--data-raw '{
    "payana_likes": {
        "pf_id_1": "12345679",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    },
    "entity_id": "12345"
}'
"""
profile_likes_json = {
    payana_like_column_family: {
        "pf_id_1": "12345679",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    }
}

headers = {'Content-Type': 'application/json',
           payana_likes_table_entity_id: entity_id}

response = requests.put(url, data=json.dumps(
    profile_likes_json), headers=headers)

print("Profile Likes object update status: " + str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana likes read status: " + str(response.status_code == 200))

profile_likes_response = response.json()

print("Profile likes creation verification status: " +
      str(profile_likes_response[entity_id][payana_like_column_family]["pf_id_1"] == "12345679"))

# Delete specific column family and column values
"""
curl --location --request POST 'http://localhost:8888/entity/likes/delete/values/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345' \
--data-raw '{
    "payana_likes": ["pf_id_1", "pf_id_2"]
}'
"""
url = "http://localhost:8888/entity/likes/delete/values/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

profile_likes_delete_cv_json = {
    payana_like_column_family: ["pf_id_1"]
}

response = requests.post(url, data=json.dumps(
    profile_likes_delete_cv_json), headers=headers)

print("Payana likes contents column values delete status: " +
      str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana likes read status: " + str(response.status_code == 200))

profile_likes_response = response.json()

print("Profile likes creation verification status: " +
      str("pf_id_1" not in profile_likes_response[entity_id][payana_like_column_family]))

# Delete entire column family
"""
curl --location --request POST 'http://localhost:8888/profile/travelfont/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/likes/delete/cf/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.post(url, headers=headers)

print("Payana Likes column family delete status: " +
      str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana likes read status: " + str(response.status_code == 400))

# POST profile likes
# CURL request
"""
curl --location --request POST 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345' \
--data-raw '{
    "payana_likes": {
        "pf_id_1": "1234567",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    },
    "entity_id": "12345"
}'
"""

url = "http://localhost:8888/entity/likes/"

profile_likes_json = {
    payana_like_column_family: {
        "pf_id_1": "1234567",
        "pf_id_2": "1234567",
        "pf_id_3": "1234567"
    },
    payana_likes_table_entity_id: "12345"
}

entity_id = profile_likes_json[payana_likes_table_entity_id]

headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_likes_json), headers=headers)


print("Profile likes object creation status: " +
      str(response.status_code == 201))

# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana likes read status: " + str(response.status_code == 200))

profile_likes_response = response.json()

print("Profile likes creation verification status: " +
      str(profile_likes_response[entity_id][payana_like_column_family]["pf_id_1"] == "1234567"))

# Delete payana likes row
"""
curl --location --request DELETE 'http://localhost:8888/entity/likes/delete/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/delete/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana likes row delete status: " + str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/likes/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 12345'
"""

url = "http://localhost:8888/entity/likes/"
headers = {payana_likes_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile likes row delete status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
