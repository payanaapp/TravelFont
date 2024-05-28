from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

from urllib import response
import requests
import json

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_itinerary_city = bigtable_constants.payana_itinerary_city

"""
To fetch top itineraries/activities/excursions based on city search & timestamp ordered.
For Alpha - we use this. While rendering we render based on real time ordering of likes/comments
Population of this table happens in real time as a new itinerary is added.
"""

# POST - To add an itinerary/activity guide/excursion into the city search timestamp ordered itinerary table
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "itinerary_id": {
        "1": "12345"          # itinerary_id: timestamp
    },
    "activity_guide_id": {
        "1": "12345"          # activity_guide_id: timestamp
    },
    "excursion_id": {
        "1": "12345"          # excursion_id: timestamp
    },
    "activities": [
        "generic",
        "hiking",
        "romantic"
    ]
}'
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
 
payana_global_city_timestamp_itinerary_object_json = {
    "city": "cupertino##california##usa",
    "itinerary_id": {
        "1": "12345"
    },
    "activity_guide_id": {
        "1": "12345"
    },
    "excursion_id": {
        "1": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic"
    ]
}

city = payana_global_city_timestamp_itinerary_object_json[payana_itinerary_city]

headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_global_city_timestamp_itinerary_object_json), headers=headers)


print("Payana global city itinerary ranking objects creation status: " +
      str(response.status_code == 201))

profile_global_city_timestamp_itinerary_object_response_json = response.json()

# GET - To fetch itineraries/activity guides/excursions corresponding to a given city
"""
Result:

{
    "cupertino##california##usa": {
        "generic_timestamp_activity_guide_id": {
            "1": "12345"
        },
        "generic_timestamp_excursion_id": {
            "1": "12345"
        },
        "generic_timestamp_itinerary_id": {
            "1": "12345"
        },
        "hiking_timestamp_activity_guide_id": {
            "1": "12345"
        },
        "hiking_timestamp_excursion_id": {
            "1": "12345"
        },
        "hiking_timestamp_itinerary_id": {
            "1": "12345"
        },
        "romantic_timestamp_activity_guide_id": {
            "1": "12345"
        },
        "romantic_timestamp_excursion_id": {
            "1": "12345"
        },
        "romantic_timestamp_itinerary_id": {
            "1": "12345"
        }
    }
}
"""
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_timestamp_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_timestamp_itinerary_object_response = response.json()

print(payana_global_city_timestamp_itinerary_object_response)

print("Payana global_city_timestamp_itinerary object creation verification status: " +
      str(city in payana_global_city_timestamp_itinerary_object_response))

# Edit - Edit 
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "city": "cupertino##california##usa",
    "itinerary_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activity_guide_id": {
        "1": "1234578",
        "2": "12345"
    },
    "excursion_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic"
    ]
}'
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"

payana_global_city_timestamp_itinerary_object_edit_json = {
    "city": "cupertino##california##usa",
    "itinerary_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activity_guide_id": {
        "1": "1234578",
        "2": "12345"
    },
    "excursion_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic"
    ]
}

new_itinerary_id = "2"
new_itinerary_id_timestamp = "12345"

old_itinerary_id = "1"
old_itinerary_id_timestamp = "1234578"

headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_global_city_timestamp_itinerary_object_edit_json), headers=headers)


print("Payana global_city_timestamp_itinerary object edit status: " +
      str(response.status_code == 200))

profile_global_city_timestamp_itinerary_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_timestamp_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_timestamp_itinerary_object_response = response.json()

cf_timestamp = "hiking_timestamp_itinerary_id"

print("Payana global_city_timestamp_itinerary object edit verification status: " +
      str(new_itinerary_id_timestamp == payana_global_city_timestamp_itinerary_object_response[city][cf_timestamp][new_itinerary_id] and old_itinerary_id_timestamp == payana_global_city_timestamp_itinerary_object_response[city][cf_timestamp][old_itinerary_id]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "generic_timestamp_itinerary_id": {
        "1": "1234578"
    },
    "generic_timestamp_activity_guide_id": {
        "1": "1234578"
    },
    "generic_timestamp_excursion_id": {
        "1": "1234578"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/delete/values/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

payana_global_city_timestamp_itinerary_object_delete_cv_json = {
    "generic_timestamp_itinerary_id": {
        "1": "1234578"
    },
    "generic_timestamp_activity_guide_id": {
        "1": "1234578"
    },
    "generic_timestamp_excursion_id": {
        "1": "1234578"
    }
}

response = requests.post(url, data=json.dumps(
    payana_global_city_timestamp_itinerary_object_delete_cv_json), headers=headers)

print("Payana global_city_timestamp_itinerary object column values delete CV status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_timestamp_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_timestamp_itinerary_object_response = response.json()

cf_delete_value_one = "generic_timestamp_itinerary_id"
cf_delete_value_two = "generic_timestamp_itinerary_id"

print("Payana global_city_timestamp_itinerary object delete CV verification status: " +
      str(old_itinerary_id not in payana_global_city_timestamp_itinerary_object_response[city][cf_delete_value_one] and old_itinerary_id not in payana_global_city_timestamp_itinerary_object_response[city][cf_delete_value_two]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "hiking_timestamp_itinerary_id": "",
    "hiking_timestamp_activity_guide_id": "",
    "hiking_timestamp_excursion_id": ""
}'
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/delete/cf/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

profile_global_city_timestamp_itinerary_object_delete_cf_json = {
    "hiking_timestamp_itinerary_id": "",
    "hiking_timestamp_activity_guide_id": "",
    "hiking_timestamp_excursion_id": ""
}

cf_delete_value_one = "hiking_timestamp_itinerary_id"
cf_delete_value_two = "hiking_timestamp_activity_guide_id"

response = requests.post(url, data=json.dumps(
    profile_global_city_timestamp_itinerary_object_delete_cf_json), headers=headers)

print("Payana global_city_timestamp_itinerary object column family delete CF status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_timestamp_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_timestamp_itinerary_object_response = response.json()

print("Payana global_city_timestamp_itinerary object delete CF verification status: " +
      str(cf_delete_value_one not in payana_global_city_timestamp_itinerary_object_response[city] and cf_delete_value_two not in payana_global_city_timestamp_itinerary_object_response[city]))

# Delete row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/global/timestamp/city/delete/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/delete/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana global city timestamp itinerary object row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/global/timestamp/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/global/timestamp/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global city timestamp itinerary object row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
