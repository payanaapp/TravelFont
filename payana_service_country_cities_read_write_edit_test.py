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

payana_country_table_column_family_city_list = bigtable_constants.payana_country_table_column_family_city_list

# POST country cities
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"

payana_country_city_json = {
    "country": "usa",
    "city_list": {
        "cupertino##california##usa": "1.2",
        "seattle##washington##usa": "1.78"
    }
}

country = payana_country_city_json["country"]

headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_country_city_json), headers=headers)


print("Payana country cities creation status: " +
      str(response.status_code == 201))

profile_travel_city_influencer_response_json = response.json()

# GET country cities
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city read status: " + str(response.status_code == 200))

payana_country_city_response = response.json()

print("Payana country city creation verification status: " +
      str(len(payana_country_city_response[country]) is not None))


# Edit travel influencer city object
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.7",
        "vancouver##bc##canada" : "1.79"
        }
}'
"""
new_city = "vancouver##bc##canada"
new_rating = "1.79"

payana_country_city_json = {
    "country": "usa",
    "city_list": {
        "cupertino##california##usa": "1.2",
        "seattle##washington##usa": "1.7",
        new_city: new_rating
    }
}

headers = {'Content-Type': 'application/json', 'country': country}

response = requests.put(url, data=json.dumps(
    payana_country_city_json), headers=headers)

print("Payana country city update status: " + str(response.status_code == 200))


# GET country cities
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city read status: " + str(response.status_code == 200))

payana_country_city_response = response.json()

print("Payana country city edit verification status: " +
      str(new_city in payana_country_city_response[country][payana_country_table_column_family_city_list]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/country/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "city_list": {
        "cupertino##california##usa" : "",
        "seattle##washington##usa" : ""
        }
}'
"""
url = "http://127.0.0.1:8888/entity/country/city/delete/values/"
headers = {'country': country, 'Content-Type': 'application/json'}

payana_country_city_delete_cv_json = {
    "city_list": {
        new_city: "",
        "seattle##washington##usa": ""
    }
}

response = requests.post(url, data=json.dumps(
    payana_country_city_delete_cv_json), headers=headers)

print("Payana country city contents column values delete status: " +
      str(response.status_code == 200))

# GET country cities
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city read status: " + str(response.status_code == 200))

payana_country_city_response = response.json()

print("Payana country city creation verification status: " +
      str(new_city not in payana_country_city_response[country][payana_country_table_column_family_city_list]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/country/city/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "city_list": ""
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/delete/cf/"
headers = {'country': country, 'Content-Type': 'application/json'}

profile_travel_city_influencer_delete_cf_json = {
    payana_country_table_column_family_city_list: ""
}

response = requests.post(url, data=json.dumps(
    profile_travel_city_influencer_delete_cf_json), headers=headers)

print("Payana country city column family delete status: " +
      str(response.status_code == 200))

# GET travel city influencer
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 400))

# POST country cities
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"

payana_country_city_json = {
    "country": "usa",
    "city_list": {
        "cupertino##california##usa": "1.2",
        "seattle##washington##usa": "1.78"
    }
}

country = payana_country_city_json["country"]

headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_country_city_json), headers=headers)


print("Payana country cities creation status: " +
      str(response.status_code == 201))

profile_travel_city_influencer_response_json = response.json()

# GET country cities
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data '{
    "country": "usa",
    "city_list": {
        "cupertino##california##usa" : "1.2",
        "seattle##washington##usa" : "1.78"
        }
}'
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city read status: " + str(response.status_code == 200))

payana_country_city_response = response.json()

print("Payana country city creation verification status: " +
      str(len(payana_country_city_response[country]) is not None))

# Delete payana country city row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/country/city/delete/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/country/city/delete/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 200))

# GET travel city influencer
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/country/city/' \
--header 'Content-Type: application/json' \
--header 'country: usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/country/city/"
headers = {'country': country, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana country city row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
