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

payana_itinerary_city = bigtable_constants.payana_itinerary_city


# POST
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
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
    "checkin_id": {
        "1": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ]
}'
"""

url = "http://localhost:8888/entity/global/rating/city/"

payana_global_city_rating_itinerary_object_json = {
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
    "checkin_id": {
        "1": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ]
}

city = payana_global_city_rating_itinerary_object_json[payana_itinerary_city]

headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_global_city_rating_itinerary_object_json), headers=headers)


print("Payana global city itinerary ranking objects creation status: " +
      str(response.status_code == 201))

profile_global_city_rating_itinerary_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_rating_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_rating_itinerary_object_response = response.json()

print("Payana global_city_rating_itinerary object creation verification status: " +
      str(city in payana_global_city_rating_itinerary_object_response))

# Edit
"""
curl --location --request PUT 'http://localhost:8888/entity/global/rating/city/' \
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
    "checkin_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ]
}'
"""

url = "http://localhost:8888/entity/global/rating/city/"

payana_global_city_rating_itinerary_object_edit_json = {
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
    "checkin_id": {
        "1": "1234578",
        "2": "12345"
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ]
}

new_itinerary_id = "2"
new_itinerary_id_rating = "12345"

old_itinerary_id = "1"
old_itinerary_id_rating = "1234578"

headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_global_city_rating_itinerary_object_edit_json), headers=headers)


print("Payana global_city_rating_itinerary object edit status: " +
      str(response.status_code == 200))

profile_global_city_rating_itinerary_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_rating_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_rating_itinerary_object_response = response.json()

cf_rating = "hiking_rating_itinerary_id"

print("Payana global_city_rating_itinerary object edit verification status: " +
      str(new_itinerary_id_rating == payana_global_city_rating_itinerary_object_response[city][cf_rating][new_itinerary_id] and old_itinerary_id_rating == payana_global_city_rating_itinerary_object_response[city][cf_rating][old_itinerary_id]))

# Delete specific column family and column values
"""
curl --location 'http://localhost:8888/entity/global/rating/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "generic_rating_itinerary_id": {
        "1": "1234578"
    },
    "generic_rating_activity_guide_id": {
        "1": "1234578"
    },
    "generic_rating_excursion_id": {
        "1": "1234578"
    },
    "generic_rating_checkin_id": {
        "1": "1234578"
    }
}'
"""

url = "http://localhost:8888/entity/global/rating/city/delete/values/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

payana_global_city_rating_itinerary_object_delete_cv_json = {
    "generic_rating_itinerary_id": {
        "1": "1234578"
    },
    "generic_rating_activity_guide_id": {
        "1": "1234578"
    },
    "generic_rating_excursion_id": {
        "1": "1234578"
    },
    "generic_rating_checkin_id": {
        "1": "1234578"
    }
}

response = requests.post(url, data=json.dumps(
    payana_global_city_rating_itinerary_object_delete_cv_json), headers=headers)

print("Payana global_city_rating_itinerary object column values delete CV status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_rating_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_rating_itinerary_object_response = response.json()

cf_delete_value_one = "generic_rating_itinerary_id"
cf_delete_value_two = "generic_rating_itinerary_id"

print("Payana global_city_rating_itinerary object delete CV verification status: " +
      str(old_itinerary_id not in payana_global_city_rating_itinerary_object_response[city][cf_delete_value_one] and old_itinerary_id not in payana_global_city_rating_itinerary_object_response[city][cf_delete_value_two]))

# Delete entire column family
"""
curl --location 'http://localhost:8888/entity/global/rating/city/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data '{
    "hiking_rating_itinerary_id": "",
    "hiking_rating_activity_guide_id": "",
    "hiking_rating_excursion_id": "",
    "hiking_rating_checkin_id": ""
}'
"""

url = "http://localhost:8888/entity/global/rating/city/delete/cf/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

profile_global_city_rating_itinerary_object_delete_cf_json = {
    "hiking_rating_itinerary_id": "",
    "hiking_rating_activity_guide_id": "",
    "hiking_rating_excursion_id": "",
    "hiking_rating_checkin_id": ""
}

cf_delete_value_one = "hiking_rating_itinerary_id"
cf_delete_value_two = "hiking_rating_activity_guide_id"

response = requests.post(url, data=json.dumps(
    profile_global_city_rating_itinerary_object_delete_cf_json), headers=headers)

print("Payana global_city_rating_itinerary object column family delete CF status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global_city_rating_itinerary object read status: " +
      str(response.status_code == 200))

payana_global_city_rating_itinerary_object_response = response.json()

print("Payana global_city_rating_itinerary object delete CF verification status: " +
      str(cf_delete_value_one not in payana_global_city_rating_itinerary_object_response[city] and cf_delete_value_two not in payana_global_city_rating_itinerary_object_response[city]))

# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/entity/global/rating/city/delete/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/delete/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana global city rating itinerary object row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/global/rating/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://localhost:8888/entity/global/rating/city/"
headers = {payana_itinerary_city: city,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global city rating itinerary object row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
