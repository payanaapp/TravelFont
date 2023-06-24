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

payana_city_autocomplete_column_family = bigtable_constants.payana_city_autocomplete_column_family

payana_autocomplete_city_header = payana_service_constants.payana_autocomplete_city_header

# POST write
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--data '{
    "payana_autocomplete_cities_list": {
        "cupertino##california##usa": "156",
        "sanjose##california##usa": "789",
        "seattle##washington##usa": "8678",
        "sanjuan##xyz##puertorico": "1457"
    }
}'
"""

url = "http://localhost:8888/entity/autocomplete/city/"

payana_autocomplete_cities_obj_json = {
    "payana_autocomplete_cities_list": {
        "cupertino##california##usa": "156",
        "sanjose##california##usa": "789",
        "seattle##washington##usa": "8678",
        "sanjuan##xyz##puertorico": "1457"
    }
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_autocomplete_cities_obj_json), headers=headers)


print("Payana autocomplete cities creation status: " +
      str(response.status_code == 201))

payana_autocomplete_cities_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--header 'city: seatt.*'
"""

url = "http://localhost:8888/entity/autocomplete/city/"
autocomplete_city_string = "cuper.*"
full_city_name = "cupertino##california##usa"
score = payana_autocomplete_cities_obj_json[payana_city_autocomplete_column_family][full_city_name]

headers = {payana_autocomplete_city_header: autocomplete_city_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete city read status: " +
      str(response.status_code == 200))

payana_autocomplete_city_response = response.json()

print("Payana autocomplete city creation verification status: " +
      str(payana_autocomplete_city_response[payana_autocomplete_city_header][payana_city_autocomplete_column_family][full_city_name] == score))


# Edit PUT
"""
curl --location --request PUT 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--data '{
    "payana_autocomplete_cities_list": {
        "seattle##washington##usa": "8671238",
        "sanjuan##xyz##puertorico": "141157"
    }
}'
"""

payana_autocomplete_city_json = {
    "payana_autocomplete_cities_list": {
        "seattle##washington##usa": "8671238",
        "sanjuan##xyz##puertorico": "141157"
    }
}

new_city = "seattle##washington##usa"
new_rating = payana_autocomplete_city_json[payana_city_autocomplete_column_family][new_city]

headers = {'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_autocomplete_city_json), headers=headers)

print("Payana autocomplete city update status: " +
      str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--header 'city: seatt.*'
"""

url = "http://localhost:8888/entity/autocomplete/city/"
autocomplete_city_string = "seat.*"

headers = {payana_autocomplete_city_header: autocomplete_city_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete city read status: " +
      str(response.status_code == 200))

payana_autocomplete_city_response = response.json()

print("Payana autocomplete city edit verification status: " +
      str(payana_autocomplete_city_response[payana_autocomplete_city_header][payana_city_autocomplete_column_family][new_city] == new_rating))


# Delete specific column family and column values
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: city' \
--data '{
    "payana_autocomplete_cities_list": {
        "seattle##washington##usa": "8671238",
        "sanjuan##xyz##puertorico": "1457"
    }
}'
"""
url = "http://localhost:8888/entity/autocomplete/city/delete/values/"
headers = {payana_autocomplete_city_header: payana_autocomplete_city_header,
           'Content-Type': 'application/json'}

payana_autocomplete_city_delete_cv_json = {
    "payana_autocomplete_cities_list": {
        "seattle##washington##usa": "8671238",
        "sanjuan##xyz##puertorico": "1457"
    }
}

deleted_city = "seattle##washington##usa"

response = requests.post(url, data=json.dumps(
    payana_autocomplete_city_delete_cv_json), headers=headers)

print("Payana autocomplete city contents column values delete status: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--header 'city: seatt.*'
"""

url = "http://localhost:8888/entity/autocomplete/city/"
autocomplete_city_string = "cuper.*"

headers = {payana_autocomplete_city_header: autocomplete_city_string,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana autocomplete city read status: " +
      str(response.status_code == 200))

payana_autocomplete_city_response = response.json()

print("Payana autocomplete city values delete verification status: " +
      str(deleted_city not in payana_autocomplete_city_response[payana_autocomplete_city_header][payana_city_autocomplete_column_family]))

# Delete payana country city row
"""
curl --location --request DELETE 'http://localhost:8888/entity/autocomplete/city/delete/' \
--header 'Content-Type: application/json' \
--header 'city: city'
"""

url = "http://localhost:8888/entity/autocomplete/city/delete/"
headers = {payana_autocomplete_city_header: payana_autocomplete_city_header,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/autocomplete/city/' \
--header 'Content-Type: application/json' \
--header 'city: seatt.*'
"""

url = "http://localhost:8888/entity/autocomplete/city/"
headers = {payana_autocomplete_city_header: payana_autocomplete_city_header,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana neighboring city row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
