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

payana_excursion_checkin_permission_participants_column_family = bigtable_constants.payana_excursion_checkin_permission_participants_column_family
payana_excursion_checkin_permission_edit_participants_column_family = bigtable_constants.payana_excursion_checkin_permission_edit_participants_column_family
payana_excursion_checkin_permission_table_admin_column_family = bigtable_constants.payana_excursion_checkin_permission_table_admin_column_family

# POST
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data '{
    "entity_id": "123456789",
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "edit_participants_list": {"pf_id_2": "1234567", "pf_id_3": "1234567"},
    "admin": {"pf_id_1": "1234567"}
}'
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"

payana_excursion_objects_permission_json = {
    "entity_id": "123456789",
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "edit_participants_list": {"pf_id_2": "1234567", "pf_id_3": "1234567"},
    "admin": {"pf_id_1": "1234567"}
}

sample_profile_id = "pf_id_3"
sample_profile_id_number = "1234567"

entity_id = payana_excursion_objects_permission_json["entity_id"]

headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_excursion_objects_permission_json), headers=headers)


print("Payana excursion objects permission creation status: " +
      str(response.status_code == 201))

profile_excursion_objects_permission_response_json = response.json()

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion objects permission edit verification status: " +
      str(sample_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_participants_column_family] and sample_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_edit_participants_column_family]))

# Edit 
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data '{
    "entity_id": "123456789",
    "participants_list": {"pf_id_3": "12345678", "pf_id_4": "1234567"},
    "edit_participants_list": {"pf_id_4": "1234567", "pf_id_3": "12345678"},
    "admin": {"pf_id_1": "1234567"}
}'
"""
url = "http://127.0.0.1:8888/entity/edit/permission/"

new_profile_id = "pf_id_4"
new_profile_id_number = "1234567"
payana_excursion_objects_permission_edit_json = {
    "entity_id": "123456789",
    "participants_list": {"pf_id_3": "12345678", new_profile_id: new_profile_id_number},
    "edit_participants_list": {new_profile_id: new_profile_id_number, "pf_id_3": "12345678"},
    "admin": {"pf_id_1": "1234567"}
}

entity_id = payana_excursion_objects_permission_edit_json["entity_id"]

headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_excursion_objects_permission_edit_json), headers=headers)


print("Payana excursion objects permission edit status: " +
      str(response.status_code == 200))

profile_excursion_objects_permission_response_json = response.json()

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion objects permission edit verification status: " +
      str(new_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_participants_column_family] and new_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_edit_participants_column_family]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/delete/values/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data '{
    "participants_list": {"pf_id_1": ""},
    "edit_participants_list": {"pf_id_2": ""}
}'
"""
url = "http://127.0.0.1:8888/entity/edit/permission/delete/values/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

payana_excursion_object_permission_delete_cv_json = {
    "participants_list": {new_profile_id: ""},
    "edit_participants_list": {new_profile_id: ""}
}

response = requests.post(url, data=json.dumps(
    payana_excursion_object_permission_delete_cv_json), headers=headers)

print("Payana excursion object permission column values delete status: " +
      str(response.status_code == 200))

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion objects permission delete values verification status: " +
      str(new_profile_id not in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_participants_column_family] and new_profile_id not in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_edit_participants_column_family]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data '{
    "participants_list": "",
    "edit_participants_list": "",
    "admin": ""
}'
"""

url = "http://127.0.0.1:8888/entity/edit/permission/delete/cf/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

profile_excursion_object_permission_delete_cf_json = {
    payana_excursion_checkin_permission_participants_column_family: "",
    payana_excursion_checkin_permission_edit_participants_column_family: ""
}

response = requests.post(url, data=json.dumps(
    profile_excursion_object_permission_delete_cf_json), headers=headers)

print("Payana country city column family delete status: " +
      str(response.status_code == 200))

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion objects permission delete column family verification status: " +
      str(payana_excursion_checkin_permission_participants_column_family not in payana_excursion_objects_permission_response[entity_id] and payana_excursion_checkin_permission_edit_participants_column_family not in payana_excursion_objects_permission_response[entity_id]))

# POST
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data '{
    "entity_id": "123456789",
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "edit_participants_list": {"pf_id_2": "1234567", "pf_id_3": "1234567"},
    "admin": {"pf_id_1": "1234567"}
}'
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"

payana_excursion_objects_permission_json = {
    "entity_id": "123456789",
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "edit_participants_list": {"pf_id_2": "1234567", "pf_id_3": "1234567"},
    "admin": {"pf_id_1": "1234567"}
}

sample_profile_id = "pf_id_3"
sample_profile_id_number = "1234567"

entity_id = payana_excursion_objects_permission_json["entity_id"]

headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_excursion_objects_permission_json), headers=headers)


print("Payana excursion objects permission creation status: " +
      str(response.status_code == 201))

profile_excursion_objects_permission_response_json = response.json()

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission read status: " +
      str(response.status_code == 200))

payana_excursion_objects_permission_response = response.json()

print("Payana excursion objects permission edit verification status: " +
      str(sample_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_participants_column_family] and sample_profile_id in payana_excursion_objects_permission_response[entity_id][payana_excursion_checkin_permission_edit_participants_column_family]))

# Delete row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/edit/permission/delete/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/delete/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana excursion objects permission row delete status: " +
      str(response.status_code == 200))

# GET 
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/edit/permission/' \
--header 'Content-Type: application/json' \
--header 'entity_id: 123456789' \
--data ''
"""

url = "http://127.0.0.1:8888/entity/edit/permission/"
headers = {'entity_id': entity_id, 'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana excursion objects permission row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
