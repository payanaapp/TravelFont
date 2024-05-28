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
from payana.payana_service.constants import payana_service_constants

from urllib import response
import requests
import json

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_users_autocomplete_column_family = bigtable_constants.payana_users_autocomplete_column_family

payana_autocomplete_city_header = payana_service_constants.payana_autocomplete_city_header
payana_autocomplete_users_header = payana_service_constants.payana_autocomplete_users_header

# Note: Reasons why we have a city field

# 1. To search all travel influencers indexed by a city

# 2. To search for travel influencers based on a name autocomplete regex
  # -- Start the search with user's city radius. Example - "cupertino##california##usa"
  # -- Expand to neighboring city list. 
  # -- Expand to State. Example - "*.##california##usa"
  # -- Expand to country. Example - "*.##usa"
  
# POST write
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"

payana_autocomplete_users_obj_json = {
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457"
    }
}

city = payana_autocomplete_users_obj_json[payana_autocomplete_city_header]

headers = {payana_autocomplete_city_header: city,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_autocomplete_users_obj_json), headers=headers)


print("Payana autocomplete users creation status: " +
      str(response.status_code == 201))

payana_autocomplete_users_response_json = response.json()

# GET read - regex column values i.e. for a given city (row key - no regex), search matching user (column quantifier - regex)
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--header 'user: user.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"
autocomplete_user_string = "user.*" # strings starting with 'user'
# autocomplete_user_string = ".*1$" -- strings ending with '1'
full_user_name = "user_1"
score = "156"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read regex status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print("Payana autocomplete user creation verification regex read status: " +
      str(payana_autocomplete_user_response[city][payana_users_autocomplete_column_family][full_user_name] == score))

# POST write
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"

payana_autocomplete_users_obj_json_two = {
    "city": "sf##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789",
        "user_3": "8678",
        "user_4": "1457"
    }
}

city_two = payana_autocomplete_users_obj_json_two[payana_autocomplete_city_header]

headers = {payana_autocomplete_city_header: city_two,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_autocomplete_users_obj_json_two), headers=headers)


print("Payana autocomplete users creation status for object two: " +
      str(response.status_code == 201))

payana_autocomplete_users_response_json = response.json()

# GET read - regex column values i.e. for a matching city (row key - regex), search matching user (column qualifier - regex)
# CURL request
"""
# curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/regex/' \
--header 'Content-Type: application/json' \
--header 'city: .*##usa' \
--header 'user: user.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/regex/"
# autocomplete_user_string = "user.*" # strings starting with 'user'
autocomplete_user_string = ".*1$" # -- strings ending with '1'
full_user_name = "user_1"
score = "156"
regex_city = ".*##usa"

headers = {payana_autocomplete_city_header: regex_city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read regex (both row & column quantifier) status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print(payana_autocomplete_user_response)

print("Payana autocomplete user creation verification regex (both row & column quantifier) read status: " +
      str(len(payana_autocomplete_user_response) == 2))

# GET read - regex column values i.e. for a all rows (all cities in this case), search matching user (column qualifier - regex)
# CURL request
"""
# curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/regex/' \
--header 'Content-Type: application/json' \
--header 'city: .*##usa' \
--header 'user: user.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/regex/"
# autocomplete_user_string = "user.*" # strings starting with 'user'
autocomplete_user_string = ".*1$" # -- strings ending with '1'
full_user_name = "user_1"
score = "156"
regex_empty_city = ""

headers = {payana_autocomplete_city_header: regex_empty_city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read regex (column quantifier) status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print(payana_autocomplete_user_response)

print("Payana autocomplete user creation verification regex (column quantifier) read status: " +
      str(len(payana_autocomplete_user_response) == 2))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--header 'user;'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"
autocomplete_user_string = ""

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read row status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print("Payana autocomplete user creation verification row read status: " +
      str(len(payana_autocomplete_user_response[city][payana_users_autocomplete_column_family]) == 4))

# Edit PUT
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "1526",
        "user_2": "789",
        "user_3": "86748",
        "user_4": "1457"
    }
}'
"""

payana_autocomplete_users_json = {
    "city": "cupertino##california##usa",
    "payana_autocomplete_users_list": {
        "user_1": "1526",
        "user_2": "789",
        "user_3": "86748",
        "user_4": "1457"
    }
}

new_user = "user_1"
new_rating = "1526"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_autocomplete_users_json), headers=headers)

print("Payana autocomplete user update status: " +
      str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--header 'user: user.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print("Payana autocomplete user creation verification status: " +
      str(payana_autocomplete_user_response[city][payana_users_autocomplete_column_family][new_user] == new_rating))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789"
    }
}'
"""
url = "http://127.0.0.1:8888/entity/autocomplete/users/delete/values/"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

payana_autocomplete_users_delete_cv_json = {
    "payana_autocomplete_users_list": {
        "user_1": "156",
        "user_2": "789"
    }
}

deleted_user = "user_1"

response = requests.post(url, data=json.dumps(
    payana_autocomplete_users_delete_cv_json), headers=headers)

print("Payana autocomplete users contents column values delete status: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--header 'user: user.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete user read status: " +
      str(response.status_code == 200))

payana_autocomplete_user_response = response.json()

print("Payana autocomplete user creation verification status: " +
      str(deleted_user not in payana_autocomplete_user_response[city][payana_users_autocomplete_column_family]))

# Delete payana country city row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/autocomplete/users/delete/' \
--header 'Content-Type: application/json' \
--header 'city: city'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/delete/"
headers = {payana_autocomplete_city_header: city,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/autocomplete/users/' \
--header 'Content-Type: application/json' \
--header 'city: seatt.*'
"""

url = "http://127.0.0.1:8888/entity/autocomplete/users/"

headers = {payana_autocomplete_city_header: city,
           payana_autocomplete_users_header: autocomplete_user_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
