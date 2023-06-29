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

payana_sign_up_mail_id_list_profile_id = bigtable_constants.payana_sign_up_mail_id_list_profile_id
payana_sign_up_mail_id_list_column_family = bigtable_constants.payana_sign_up_mail_id_list_column_family

# POST write
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}'
"""

url = "http://localhost:8888/entity/signup/"

payana_sign_up_mail_id_notification_json = {
    payana_sign_up_mail_id_list_profile_id: "123456789",
    payana_sign_up_mail_id_list_column_family: {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}

profile_id = payana_sign_up_mail_id_notification_json[payana_sign_up_mail_id_list_profile_id]

headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_sign_up_mail_id_notification_json), headers=headers)


print("Payana mail id sign up notification creation status: " +
      str(response.status_code == 201))

payana_sign_up_mail_id_notification_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list read status: " +
      str(response.status_code == 200))

payana_sign_up_mail_id_list_response = response.json()

print("Payana sign_up_mail_id_list creation verification status: " +
      str(len(payana_sign_up_mail_id_list_response[profile_id][payana_sign_up_mail_id_list_column_family]) is not None))


# Edit PUT
"""
curl --location --request PUT 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456"
    }
}'
"""

payana_sign_up_mail_id_json = {
    "profile_id": "123456789",
    "sign_up_mail_id_list": {
        "bharathi.hv@gmail.com": "123456789"
    }
}

new_mail_id = "bharathi.hv@gmail.com"
new_timestamp = "123456789"

headers = {'Content-Type': 'application/json',
           payana_sign_up_mail_id_list_profile_id: profile_id}

response = requests.put(url, data=json.dumps(
    payana_sign_up_mail_id_json), headers=headers)

print("Payana sign_up_mail_id update status: " +
      str(response.status_code == 200))


# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list read status: " +
      str(response.status_code == 200))

payana_sign_up_mail_id_list_response = response.json()

print("Payana sign_up_mail_id_list edit verification status: " +
      str(new_mail_id in payana_sign_up_mail_id_list_response[profile_id][payana_sign_up_mail_id_list_column_family]))

# Delete specific column family and column values
"""
curl --location 'http://localhost:8888/entity/signup/delete/values/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}'
"""
url = "http://localhost:8888/entity/signup/delete/values/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

payana_sign_up_mail_id_delete_cv_json = {
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789"
    }
}

deleted_mail_id = "abhinandanramesh@gmail.com"

response = requests.post(url, data=json.dumps(
    payana_sign_up_mail_id_delete_cv_json), headers=headers)

print("Payana sign up mail id notification contents column values delete status: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list read status: " +
      str(response.status_code == 200))

payana_sign_up_mail_id_list_response = response.json()

print("Payana sign_up_mail_id_list delete values verification status: " +
      str(deleted_mail_id not in payana_sign_up_mail_id_list_response[profile_id][payana_sign_up_mail_id_list_column_family]))

# Delete entire column family
"""
curl --location 'http://localhost:8888/entity/signup/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data '{
    "sign_up_mail_id_list": ""
}'
"""

url = "http://localhost:8888/entity/signup/delete/cf/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

payana_sign_up_mail_id_delete_cf_json = {
    payana_sign_up_mail_id_list_column_family: ""
}

response = requests.post(url, data=json.dumps(
    payana_sign_up_mail_id_delete_cf_json), headers=headers)

print("Payana sign_up_mail_id column family delete CF status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list row delete CF status: " +
      str(response.status_code == 400))

# POST write
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_id": "123456789",
    "sign_up_mail_id_list": {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}'
"""

url = "http://localhost:8888/entity/signup/"

payana_sign_up_mail_id_notification_json = {
    payana_sign_up_mail_id_list_profile_id: "123456789",
    payana_sign_up_mail_id_list_column_family: {
        "abhinandanramesh@gmail.com": "123456789",
        "akelger@ncsu.edu": "123456789"
    }
}

profile_id = payana_sign_up_mail_id_notification_json[payana_sign_up_mail_id_list_profile_id]

headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_sign_up_mail_id_notification_json), headers=headers)


print("Payana mail id sign up notification creation status: " +
      str(response.status_code == 201))

payana_sign_up_mail_id_notification_response_json = response.json()

# GET read
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list read status: " +
      str(response.status_code == 200))

payana_sign_up_mail_id_list_response = response.json()

print("Payana sign_up_mail_id_list creation verification status: " +
      str(len(payana_sign_up_mail_id_list_response[profile_id][payana_sign_up_mail_id_list_column_family]) is not None))

# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/entity/signup/delete/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/delete/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana sign_up_mail_id_list row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://localhost:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789'
"""

url = "http://localhost:8888/entity/signup/"
headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana sign_up_mail_id_list row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
