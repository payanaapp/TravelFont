from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
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

payana_auth_information = bigtable_constants.payana_auth_information
payana_auth_mail_id = bigtable_constants.payana_auth_mail_id
payana_auth_profile_name = bigtable_constants.payana_auth_profile_name
payana_auth_profile_picture_id = bigtable_constants.payana_auth_profile_picture_id


# POST profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "auth_information":
    {
        "profile_name": "abkr",
        "mail_id": "abkr@gmail.com",
        "profile_picture_id": "123456789",
        "profile_id": "123456789010"
    }
}'
"""

url = "http://127.0.0.1:8888/profile/auth/"

profile_info_json = {
    payana_auth_information:
    {
        payana_auth_profile_name: "abkr",
        payana_auth_mail_id: "abkr@gmail.com",
        payana_auth_profile_picture_id: "123456789",
        "profile_id": "123456789010"
    }
}
headers = {'Content-Type': 'application/json'}

mail_id = profile_info_json[payana_auth_information][payana_auth_mail_id]

response = requests.post(url, data=json.dumps(
    profile_info_json), headers=headers)


print("Profile Auth Creation status: " + str(response.status_code == 201))

profile_info_response_json = response.json()

profile_mail_id = profile_info_response_json[payana_auth_mail_id]

print("Profile Auth creation verification status: " +
      str(profile_mail_id is not None and len(profile_mail_id) > 0))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': mail_id}

response = requests.get(url, headers=headers)

print("Profile Auth read status: " + str(response.status_code == 200))

profile_info_response = response.json()
print("Profile creation verification status: " +
      str(profile_info_response[mail_id][payana_auth_information][payana_auth_profile_name] == profile_info_json[payana_auth_information][payana_auth_profile_name]))


# Edit personal information
"""
curl --location --request PUT 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com' \
--header 'Content-Type: application/json' \
--data-raw '{
    "auth_information":
    {
        "profile_name": "abkr1",
        "mail_id": "abkr@gmail.com",
        "profile_picture_id": "123456789",
        "profile_id": "123456789010"
    }
}'
"""
profile_info_personal_information_json = {
    payana_auth_information:
    {
        payana_auth_profile_name: "abkr1",
        payana_auth_mail_id: "abkr@gmail.com",
        payana_auth_profile_picture_id: "123456789",
        "profile_id": "123456789010"
    }
}

headers = {'Content-Type': 'application/json', 'mail_id': mail_id}

response = requests.put(url, data=json.dumps(
    profile_info_personal_information_json), headers=headers)

print("Profile Auth info update status: " + str(response.status_code == 200))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': mail_id}

response = requests.get(url, headers=headers)

print("Profile Auth read status: " + str(response.status_code == 200))

profile_info_response = response.json()
print("Profile Auth info update verification status: " +
      str(profile_info_response[mail_id][payana_auth_information][payana_auth_profile_name] == profile_info_personal_information_json[payana_auth_information][payana_auth_profile_name]))

# Delete specific column values
"""
curl --location 'http://localhost:8888/profile/auth/delete/values/' \
--header 'mail_id: abkr@gmail.com' \
--header 'Content-Type: application/json' \
--data '{
    "auth_information":
    {
        "profile_picture_id": "123456789"
    }
}'
"""
url = "http://127.0.0.1:8888/profile/auth/delete/values/"
headers = {'mail_id': mail_id, 'Content-Type': 'application/json'}

profile_info_personal_information_json = {
    payana_auth_information:
    {
        payana_auth_profile_name: "abkr1",
    }
}

response = requests.post(url, data=json.dumps(
    profile_info_personal_information_json), headers=headers)

print("Profile auth info contents delete status: " +
      str(response.status_code == 200))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': mail_id}

response = requests.get(url, headers=headers)

print("Profile Auth contents delete read status: " + str(response.status_code == 200))

profile_info_response = response.json()
print("Profile creation verification status: " +
      str(payana_auth_profile_name not in profile_info_response[mail_id][payana_auth_information]))

# Delete  - entire column family
"""
curl --location 'http://localhost:8888/profile/auth/delete/cf/' \
--header 'mail_id: abkr@gmail.com' \
--header 'Content-Type: application/json' \
--data '{
    "auth_information": ""
}'
"""
url = "http://127.0.0.1:8888/profile/auth/delete/cf/"
headers = {'mail_id': mail_id, 'Content-Type': 'application/json'}

profile_info_personal_information_json = {
    payana_auth_information: ""
}

response = requests.post(url, data=json.dumps(
    profile_info_personal_information_json), headers=headers)

print("Profile auth info CF delete status: " +
      str(response.status_code == 200))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': mail_id}

response = requests.get(url, headers=headers)

print("Profile auth CF delete status: " + str(response.status_code == 400))

# POST profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "auth_information":
    {
        "profile_name": "abkr",
        "mail_id": "abkr@gmail.com",
        "profile_picture_id": "123456789",
        "profile_id": "123456789010"
    }
}'
"""

url = "http://127.0.0.1:8888/profile/auth/"

profile_info_json = {
    payana_auth_information:
    {
        payana_auth_profile_name: "abkr",
        payana_auth_mail_id: "abkr@gmail.com",
        payana_auth_profile_picture_id: "123456789",
        "profile_id": "123456789010"
    }
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_info_json), headers=headers)


print("Profile Auth Creation status: " + str(response.status_code == 201))

profile_info_response_json = response.json()

profile_mail_id = profile_info_response_json[payana_auth_mail_id]

print("Profile Auth creation verification status: " +
      str(profile_mail_id is not None and len(profile_mail_id) > 0))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': profile_mail_id}

response = requests.get(url, headers=headers)

print("Profile Auth read status: " + str(response.status_code == 200))

profile_info_response = response.json()
print("Profile Auth creation verification status: " +
      str(profile_info_response[profile_mail_id][payana_auth_information][payana_auth_profile_name] == profile_info_json[payana_auth_information][payana_auth_profile_name]))

# Delete Row
"""
curl --location --request DELETE 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""
url = "http://127.0.0.1:8888/profile/auth/delete/"
headers = {'mail_id': profile_mail_id}

response = requests.delete(url, headers=headers)

print("Profile info delete status: " + str(response.status_code == 200))

# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/profile/auth/' \
--header 'mail_id: abkr@gmail.com'
"""

url = "http://127.0.0.1:8888/profile/auth/"
headers = {'mail_id': profile_mail_id}

response = requests.get(url, headers=headers)

print("Profile info auth delete status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
