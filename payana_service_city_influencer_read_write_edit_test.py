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

payana_city_to_influencers_table_global_influencers_column_family = bigtable_constants.payana_city_to_influencers_table_global_influencers_column_family

# POST profile travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data '{
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"123456789": "0.49"},
    "activities": ["generic", "hiking", "romantic"]
}'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"

profile_travel_city_influencer_json = {
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"12345678": "0.48"},
    "activities": ["generic", "hiking", "romantic"]
}

city = profile_travel_city_influencer_json["city"]

headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_travel_city_influencer_json), headers=headers)


print("Profile travel city influencer creation status: " + str(response.status_code == 201))

profile_travel_city_influencer_response_json = response.json()

# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Travel city influencer read status: " + str(response.status_code == 200))

profile_travel_city_influencer_response = response.json()

print("Profile travel city influencer creation verification status: " +
      str(len(profile_travel_city_influencer_response[city]) is not None))


# Edit travel influencer city object
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/influencers/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data '{
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"123456789": "0.48"},
    "activities": ["generic", "hiking", "romantic"]
}'
"""
profile_travel_influencer_city_json = {
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"12345678": "0.49"},
    "activities": ["generic", "hiking", "romantic"]
}

headers = {'Content-Type': 'application/json', 'city': city}

response = requests.put(url, data=json.dumps(
    profile_travel_influencer_city_json), headers=headers)

print("Profile travel city influencer update status: " + str(response.status_code == 200))

updated_cf = "_".join(["hiking", payana_city_to_influencers_table_global_influencers_column_family])
updated_cq, updated_cq_value = list(profile_travel_influencer_city_json[payana_city_to_influencers_table_global_influencers_column_family].items())[0]

# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Travel city influencer read status: " + str(response.status_code == 200))

profile_travel_city_influencer_response = response.json()
get_updated_cq, get_updated_cq_value = list(profile_travel_city_influencer_response[city][updated_cf].items())[0]

print("Profile travel city influencer update verification status: " +
      str(get_updated_cq == get_updated_cq and get_updated_cq_value == get_updated_cq_value))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city/delete/values/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data '{
    "generic_city_global_influencers": ["123456789"],
    "hiking_city_global_influencers": ["123456789"]
}'
"""
url = "http://127.0.0.1:8888/entity/influencers/city/delete/values/"
headers = {'city': city, 'Content-Type': 'application/json'}

profile_travel_city_influencer_delete_cv_json = {
    "generic_city_global_influencers": ["12345678"],
    "hiking_city_global_influencers": ["12345678"]
}

response = requests.post(url, data=json.dumps(
    profile_travel_city_influencer_delete_cv_json), headers=headers)

print("Profile travel city influencer contents column values delete status: " +
      str(response.status_code == 200))

# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Travel city influencer read status: " + str(response.status_code == 200))

profile_travel_city_influencer_response = response.json()

print("Profile travel city influencer delete value verification status: " +
      str(updated_cf not in profile_travel_city_influencer_response[city]))

# POST profile travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data '{
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"123456789": "0.49"},
    "activities": ["generic", "hiking", "romantic"]
}'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"

profile_travel_city_influencer_json = {
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"12345678": "0.48"},
    "activities": ["generic", "hiking", "romantic"]
}

city = profile_travel_city_influencer_json["city"]

headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_travel_city_influencer_json), headers=headers)


print("Profile travel city influencer creation status: " + str(response.status_code == 201))

profile_travel_city_influencer_response_json = response.json()

# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Travel city influencer read status: " + str(response.status_code == 200))

profile_travel_city_influencer_response = response.json()

print("Profile travel city influencer creation verification status: " +
      str(len(profile_travel_city_influencer_response[city]) is not None))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data '{
    "generic_city_global_influencers": {},
    "hiking_city_global_influencers": {}
}'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/delete/cf/"
headers = {'city': city, 'Content-Type': 'application/json'}

profile_travel_city_influencer_delete_cf_json = {
    "generic_city_global_influencers": {},
    "hiking_city_global_influencers": {}
}

response = requests.post(url, data=json.dumps(
    profile_travel_city_influencer_delete_cf_json), headers=headers)

print("Profile travel city influencer column family delete status: " +
      str(response.status_code == 200))


# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Travel city influencer read status: " + str(response.status_code == 200))

profile_travel_city_influencer_response = response.json()

print("Profile travel city influencer delete CF verification status: " +
      str(updated_cf not in profile_travel_city_influencer_response[city]))

# Delete profile travel city influencer row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/influencers/city/delete/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/influencers/city/delete/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Profile travel city influencer row delete status: " + str(response.status_code == 200))


# GET travel city influencer
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/influencers/city' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa##november##2022'
"""

url = "http://127.0.0.1:8888/entity/influencers/city/"
headers = {'city': city, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Profile travel city influencer row delete status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
