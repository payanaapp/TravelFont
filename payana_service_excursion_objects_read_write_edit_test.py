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

column_family_excursion_metadata = bigtable_constants.payana_excursion_metadata
payana_excursion_id = bigtable_constants.payana_excursion_id
payana_excursion_column_family_participants_list = bigtable_constants.payana_excursion_column_family_participants_list
payana_excursion_column_family_checkin_id_list = bigtable_constants.payana_excursion_column_family_checkin_id_list


# POST
# CURL request
"""
curl --location 'http://localhost:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--data '{
    "checkin_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "image_id_list":{
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "34567",
        "3A": "23456",
        "3B": "34567" 
    },
    "cities_checkin_id_list":{
        "1": "cupertino##california##usa",
        "2": "sunnyvale##california##usa",
        "3": "santaclara##california##usa"       
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "roadtrip": "6"},
    "excursion_metadata": {
        "excursion_id": "123456789",
        "activity_guide": "False",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "description": "My excursion",
        "itinerary_id": "1234",
        "itinerary_name": "NewYork, Boston, Maine",
        "place_name": "Land'\''s End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA",
        "excursion_object_position_itinerary": "1",
        "excursion_clone_parent_id": ""
    }
}'
"""

url = "http://127.0.0.1:8888/entity/excursion/"

payana_excursion_object_json = {
    "checkin_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "image_id_list": {
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "34567",
        "3A": "23456",
        "3B": "34567"
    },
    "cities_checkin_id_list": {
        "1": "cupertino##california##usa",
        "2": "sunnyvale##california##usa",
        "3": "santaclara##california##usa"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "roadtrip": "6"},
    "excursion_metadata": {
        "excursion_id": "123456789",
        "activity_guide": "False",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "description": "My excursion",
        "itinerary_id": "1234",
        "itinerary_name": "NewYork, Boston, Maine",
        "place_name": "Land's End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA",
        "excursion_object_position_itinerary": "1",
        "excursion_clone_parent_id": ""
    }
}

excursion_id = payana_excursion_object_json[column_family_excursion_metadata][payana_excursion_id]

headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_excursion_object_json), headers=headers)


print("Payana excursion objects creation status: " +
      str(response.status_code == 201))

profile_excursion_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object read status: " +
      str(response.status_code == 200))

payana_excursion_object_response = response.json()

print(payana_excursion_object_response)

print("Payana excursion object creation verification status: " +
      str(excursion_id in payana_excursion_object_response))

# Edit
"""
curl --location --request PUT 'http://localhost:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data '{
    "checkin_id_list": {
        "5": "34567",
        "4": "45678"
    },
    "image_id_list":{
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "34567",
        "3A": "23456",
        "3B": "34567" 
    },
    "cities_checkin_id_list":{
        "1": "cupertino##california##usa",
        "2": "sunnyvale##california##usa",
        "3": "santaclara##california##usa"       
    },
    "participants_list": {"pf_id_4": "1234567", "pf_id_2": "12345678"},
    "activities_list": {"romantic": "4", "roadtrip": "7"},
    "excursion_metadata": {
        "place_name": "Land's End 1",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}'
"""

url = "http://127.0.0.1:8888/entity/excursion/"

payana_excursion_object_edit_json = {
    "checkin_id_list": {
        "5": "34567",
        "4": "45678"
    },
    "image_id_list": {
        "1A": "12345",
        "1B": "34567",
        "2A": "23456",
        "2B": "34567",
        "3A": "23456",
        "3B": "34567"
    },
    "cities_checkin_id_list": {
        "1": "cupertino##california##usa",
        "2": "sunnyvale##california##usa",
        "3": "santaclara##california##usa"
    },
    "participants_list": {"pf_id_4": "1234567", "pf_id_2": "12345678"},
    "activities_list": {"romantic": "4", "roadtrip": "7"},
    "excursion_metadata": {
        "place_name": "Land's End 1",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}

new_checkin_id = "5"
new_profile_id = "pf_id_4"

headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_excursion_object_edit_json), headers=headers)


print("Payana excursion object edit status: " +
      str(response.status_code == 200))

profile_excursion_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion object edit verification status: " +
      str(new_profile_id in payana_excursion_objects_permission_response[excursion_id][payana_excursion_column_family_participants_list] and new_checkin_id in payana_excursion_objects_permission_response[excursion_id][payana_excursion_column_family_checkin_id_list]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/delete/values/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data '{
    "activities_list": {
        "hiking": ""
    },
    "checkin_id_list": {
        "1": "",
        "2": ""
    },
    "excursion_metadata": {
        "activity_guide": "",
        "city": "",
        "country": "",
        "create_timestamp": ""
    },
    "participants_list": {
        "pf_id_1": "",
        "pf_id_2": ""
    }
}'
"""

url = "http://127.0.0.1:8888/entity/excursion/delete/values/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

payana_excursion_object_delete_cv_json = {
    "activities_list": {
        "hiking": ""
    },
    "checkin_id_list": {
        "1": "",
        "2": ""
    },
    "excursion_metadata": {
        "activity_guide": "",
        "city": "",
        "country": "",
        "create_timestamp": ""
    },
    "participants_list": {
        "pf_id_1": "",
        "pf_id_2": ""
    },
    "image_id_list": {
        "1A": ""
    }
}

deleted_profile_id = "pf_id_1"
deleted_checkin_id = "1"
deleted_excursion_metadata_cv = "activity_guide"
deleted_image_id = "1A"

response = requests.post(url, data=json.dumps(
    payana_excursion_object_delete_cv_json), headers=headers)

print("Payana excursion object column values delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion object CV delete verification status: " +
      str(deleted_excursion_metadata_cv not in payana_excursion_objects_permission_response[excursion_id][column_family_excursion_metadata] and deleted_profile_id not in payana_excursion_objects_permission_response[excursion_id][payana_excursion_column_family_participants_list] and deleted_checkin_id not in payana_excursion_objects_permission_response[excursion_id][payana_excursion_column_family_checkin_id_list] and deleted_image_id not in payana_excursion_objects_permission_response[excursion_id]["image_id_list"]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data '{
    "activities_list": "",
    "checkin_id_list": "",
    "excursion_metadata": "",
    "participants_list": ""
}'
"""

url = "http://127.0.0.1:8888/entity/excursion/delete/cf/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

profile_excursion_object_delete_cf_json = {
    "activities_list": "",
    "checkin_id_list": "",
    "participants_list": ""
}

deleted_cf_1 = "activities_list"
deleted_cf_2 = "checkin_id_list"
deleted_cf_3 = "participants_list"

response = requests.post(url, data=json.dumps(
    profile_excursion_object_delete_cf_json), headers=headers)

print("Payana excursion object column family delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion object CF delete verification status: " +
      str(deleted_cf_1 not in payana_excursion_objects_permission_response[excursion_id] and deleted_cf_2 not in payana_excursion_objects_permission_response[excursion_id] and deleted_cf_3 not in payana_excursion_objects_permission_response[excursion_id]))

# Delete row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/excursion/delete/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/delete/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana excursion object row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object row delete status: " +
      str(response.status_code == 400))


# Create Itinerary transaction POST
""" 
curl --location 'http://localhost:8888/entity/excursion/create/' \
--header 'Content-Type: application/json' \
--data '{
    "excursion_name": "Abhi'\''s itinerary 2",
    "activity_guide": "true",
    "excursion_owner_profile_id": "123456789",
    "create_timestamp": "123456789",
    "cities_list": {
        "Cupertino": "123456",
        "Sunnyvale": "1234567"
    },
    "activities_list": {
        "hiking": "1",
        "spring_break": "2"
    }
}'
"""

payana_create_excursion_transaction_object = {
    "excursion_name": "Abhi's itinerary 2",
    "activity_guide": "true",
    "excursion_owner_profile_id": "123456789",
    "create_timestamp": "123456789",
    "cities_list": {
        "Cupertino": "123456",
        "Sunnyvale": "1234567"
    },
    "activities_list": {
        "hiking": "1",
        "spring_break": "2"
    }
}

url = "http://127.0.0.1:8888/entity/excursion/create/"

headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_create_excursion_transaction_object), headers=headers)

print("Payana excursion objects creation status: " +
      str(response.status_code == 201))

profile_excursion_object_response_json = response.json()

excursion_id = profile_excursion_object_response_json[payana_excursion_id]

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/excursion/' \
--header 'Content-Type: application/json' \
--header 'excursion_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/excursion/"
headers = {payana_excursion_id: excursion_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion object read status: " +
      str(response.status_code == 200))

payana_excursion_object_response = response.json()

print(payana_excursion_object_response)

print("Step 1: Payana excursion object creation verification status: " +
      str(excursion_id in payana_excursion_object_response))

itinerary_id = payana_excursion_object_response[excursion_id][bigtable_constants.payana_excursion_metadata][
    bigtable_constants.payana_excursion_itinerary_id]

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/itinerary/' \
--header 'Content-Type: application/json' \
--header 'itinerary_id: 45f71f4ed3dff44215a9aef2a18ee895b134a05739187e1d8a567e49fdd833dd' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/itinerary/"
headers = {bigtable_constants.payana_excursion_itinerary_id: itinerary_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana itinerary object read status: " +
      str(response.status_code == 200))

payana_itinerary_object_response = response.json()

print(payana_itinerary_object_response)

print("Step 2: Payana itinerary object creation verification status: " +
      str(excursion_id in payana_itinerary_object_response[itinerary_id][bigtable_constants.payana_itinerary_column_family_excursion_id_list].values()))


# GET profile page itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/itineraries/' \
--header 'profile_id: 123456'
"""
profile_id = payana_create_excursion_transaction_object[
    bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id]

url = "http://127.0.0.1:8888/profile/itineraries/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_page_itinerary_response = response.json()

print(profile_page_itinerary_response)

print("Step 3: Profile Page Itinerary update verification status: " +
      str(excursion_id in profile_page_itinerary_response[profile_id]
          ["_".join([bigtable_constants.payana_generic_activity_column_family, bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value])].values()))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
