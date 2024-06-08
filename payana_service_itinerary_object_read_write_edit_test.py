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

column_family_itinerary_metadata = bigtable_constants.payana_itinerary_metadata
payana_itinerary_id = bigtable_constants.payana_itinerary_id
payana_itinerary_activities_list = bigtable_constants.payana_itinerary_activities_list
payana_itinerary_column_family_excursion_id_list = bigtable_constants.payana_itinerary_column_family_excursion_id_list
payana_itinerary_city = bigtable_constants.payana_itinerary_city

# POST 
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--data '{
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {
        "hiking": "1.0",
        "roadtrip": "1.0"
    },
    "itinerary_metadata": {
        "description": "Abhinandan'\''s SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": "",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "Land'\''s End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "123456",
        "sunnyvale##california##usa": "1234567"
    }
}'
""" 

url = "http://127.0.0.1:8888/entity/itinerary/"

payana_itinerary_object_json = {
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {"hiking": "1.0", "roadtrip": "1.0"},
    "itinerary_metadata": {
        "description": "Abhinandan's SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": "12345678",
        "itinerary_owner_profile_id": "1234567", 
        "place_id": "123456",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "12345678",  # city: place_id
        "sunnyvale##california##usa": "12345678"
    }
}

itinerary_id = payana_itinerary_object_json[column_family_itinerary_metadata][payana_itinerary_id]

headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_itinerary_object_json), headers=headers)


print("Payana itinerary objects creation status: " +
      str(response.status_code == 201))

profile_itinerary_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana itinerary object read status: " +
      str(response.status_code == 200))

payana_itinerary_object_response = response.json()

print(payana_itinerary_object_response)

city_name = payana_itinerary_object_json[column_family_itinerary_metadata][payana_itinerary_city]

print("Payana itinerary object creation verification status: " +
      str((itinerary_id in payana_itinerary_object_response) and (city_name == payana_itinerary_object_response[itinerary_id][column_family_itinerary_metadata][payana_itinerary_city])))

# Edit
"""
curl --location --request PUT 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: a57ea7b44912faf705d33b929d6134fe65ca84cafd1a4bbd7a631dfe077b9e15' \
--data '{
    "excursion_id_list": {
        "1": "12345",
        "4": "23456",
        "3": "34567"
    },
    "activities_list": {
        "hiking": "1.0",
        "roadtrip": "2.0",
        "aerial_activities": "1.0"
    },
    "itinerary_metadata": {
        "description": "Abhinandan'\''s SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": "12345678",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "Land'\''s End",
        "city": "SF##California##USA1",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "123456",
        "sunnyvale##california##usa": "1234567"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/itinerary/"

payana_itinerary_object_edit_json = {
    "excursion_id_list": {
        "1": "12345",
        "4": "23456",
        "3": "34567"
    },
    "activities_list": {
        "hiking": "1.0",
        "roadtrip": "2.0",
        "aerial_activities": "1.0"
    },
    "itinerary_metadata": {
        "description": "Abhinandan's SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": "12345678",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "Land's End",
        "city": "SF##California##USA1",
        "state": "California##USA",
        "country": "USA",
        "last_updated_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "123456",
        "sunnyvale##california##usa": "1234567"
    }
}

new_excursion_id = "4"
new_city_name = payana_itinerary_object_edit_json[column_family_itinerary_metadata][payana_itinerary_city]
new_activity = "aerial_activities"

headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_itinerary_object_edit_json), headers=headers)


print("Payana itinerary object edit status: " +
      str(response.status_code == 200))

profile_itinerary_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana itinerary object read status: " +
      str(response.status_code == 200))

payana_itinerary_object_response = response.json()

print(payana_itinerary_object_response)

print("Payana itinerary object creation verification status: " +
      str((itinerary_id in payana_itinerary_object_response) and (new_excursion_id in payana_itinerary_object_response[itinerary_id][payana_itinerary_column_family_excursion_id_list]) and (new_city_name == payana_itinerary_object_response[itinerary_id][column_family_itinerary_metadata][payana_itinerary_city]) and new_activity in payana_itinerary_object_response[itinerary_id][payana_itinerary_activities_list]))

# Delete specific column family and column values
"""
curl --location 'http://localhost:8888/entity/itinerary/delete/values/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 12345678' \
--data '{
    "excursion_id_list": {
        "1": "12345",
        "4": "23456"
    },
    "activities_list": {
        "hiking": "1.0",
        "roadtrip": "2.0"
    },
    "itinerary_metadata": {
        "description": "Abhinandan'\''s SF excursions",
        "visit_timestamp": "123456789",
        "itinerary_id": ""
    },
    "cities_list": {
        "cupertino##california##usa": "123456",
        "sunnyvale##california##usa": "1234567"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/itinerary/delete/values/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

payana_itinerary_object_delete_cv_json = {
    "excursion_id_list": {
        "1": "12345",
        "4": "23456"
    },
    "activities_list": {
        "hiking": "1.0",
        "roadtrip": "2.0"
    },
    "itinerary_metadata": {
        "description": "Abhinandan's SF excursions",
        "visit_timestamp": "123456789"
    },
    "cities_list": {
        "cupertino##california##usa": "123456",
        "sunnyvale##california##usa": "1234567"
    }
}

deleted_excursion_id = "4"
deleted_activity =  "hiking"
deleted_itinerary_metadata_cv = "description"

response = requests.post(url, data=json.dumps(
    payana_itinerary_object_delete_cv_json), headers=headers)

print("Payana itinerary object column values delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana itinerary object read status: " +
      str(response.status_code == 200))

payana_itinerary_object_response = response.json()

print(payana_itinerary_object_response)

print("Payana itinerary object creation verification status: " +
      str((itinerary_id in payana_itinerary_object_response) and (deleted_excursion_id not in payana_itinerary_object_response[itinerary_id][payana_itinerary_column_family_excursion_id_list]) and (deleted_itinerary_metadata_cv not in payana_itinerary_object_response[itinerary_id][column_family_itinerary_metadata]) and deleted_activity not in payana_itinerary_object_response[itinerary_id][payana_itinerary_activities_list]))


# Delete entire column family
"""
curl --location 'http://localhost:8888/entity/itinerary/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 12345678' \
--data '{
    "excursion_id_list": {},
    "activities_list": {},
    "itinerary_metadata": {}
}'
"""

url = "http://127.0.0.1:8888/entity/itinerary/delete/cf/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

profile_itinerary_object_delete_cf_json = {
    "excursion_id_list": {},
    "activities_list": {}
}

deleted_cf_1 = "excursion_id_list"
deleted_cf_2 = "activities_list"

response = requests.post(url, data=json.dumps(
    profile_itinerary_object_delete_cf_json), headers=headers)

print("Payana itinerary object column family delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana itinerary object read status: " +
      str(response.status_code == 200))

payana_itinerary_object_response = response.json()

print(payana_itinerary_object_response)

print("Payana itinerary object creation verification status: " +
      str((itinerary_id in payana_itinerary_object_response) and (deleted_cf_1 not in payana_itinerary_object_response[itinerary_id]) and (deleted_cf_2 not in payana_itinerary_object_response[itinerary_id])))

# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/entity/itinerary/delete/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 12345678' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/delete/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana itinerary object row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {payana_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
