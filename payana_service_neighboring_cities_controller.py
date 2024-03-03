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

payana_neighboring_cities_column_family = bigtable_constants.payana_neighboring_cities_column_family
payana_neighboring_city_header = payana_service_constants.payana_neighboring_city_header

# POST write
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"

payana_neighboring_city_json = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}

city = payana_neighboring_city_json[payana_neighboring_city_header]

headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_neighboring_city_json), headers=headers)


print("Payana neighboring cities creation status: " +
      str(response.status_code == 201))

payana_neighboring_cities_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city read status: " + str(response.status_code == 200))

payana_neighboring_city_response = response.json()

print(payana_neighboring_city_response)

print("Payana neighboring city creation verification status: " +
      str(len(payana_neighboring_city_response[city]) is not None))


# Edit PUT
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "73.56",
        "seattle##washington##usa": "82.56"
    }
}'
"""

payana_neighboring_city_json = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "73.56",
        "seattle##washington##usa": "82.56",
        "boston##masachussets##usa": "82.99"
    }
}

new_city = "seattle##washington##usa"
new_rating = "82.56"

headers = {'Content-Type': 'application/json', payana_neighboring_city_header: city}

response = requests.put(url, data=json.dumps(
    payana_neighboring_city_json), headers=headers)

print("Payana neighboring city update status: " + str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city read status: " + str(response.status_code == 200))

payana_neighboring_city_response = response.json()

print("Payana neighboring city update verification status: " +
      str(new_city in payana_neighboring_city_response[city][payana_neighboring_cities_column_family]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}'
"""
url = "http://127.0.0.1:8888/entity/neighbors/city/delete/values/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

payana_neighboring_city_delete_cv_json = {
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}

deleted_city = "cupertino##california##usa"

response = requests.post(url, data=json.dumps(
    payana_neighboring_city_delete_cv_json), headers=headers)

print("Payana neighboring city contents column values delete status: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city read status: " + str(response.status_code == 200))

payana_neighboring_city_response = response.json()

print("Payana neighboring city delete value verification status: " +
      str(deleted_city not in payana_neighboring_city_response[city][payana_neighboring_cities_column_family]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "neighboring_city_list": ""
}'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/delete/cf/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

payana_neighboring_city_delete_cf_json = {
    payana_neighboring_cities_column_family: ""
}

response = requests.post(url, data=json.dumps(
    payana_neighboring_city_delete_cf_json), headers=headers)

print("Payana neighboring city column family delete CF status: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city row delete CF status: " +
      str(response.status_code == 400))

# POST write
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"

payana_neighboring_city_json = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}

city = payana_neighboring_city_json[payana_neighboring_city_header]

headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_neighboring_city_json), headers=headers)


print("Payana neighboring cities creation status: " +
      str(response.status_code == 201))

payana_neighboring_cities_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa'
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city read status: " + str(response.status_code == 200))

payana_neighboring_city_response = response.json()

print("Payana neighboring city creation verification status: " +
      str(len(payana_neighboring_city_response[city]) is not None))

# Delete payana country city row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/neighbors/city/delete/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/delete/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 200))

# GET 
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/neighbors/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/neighbors/city/"
headers = {payana_neighboring_city_header: city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
