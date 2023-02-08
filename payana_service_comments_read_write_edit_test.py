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

payana_comments_table_entity_id = bigtable_constants.payana_comments_table_entity_id
payana_comments_table_comment_id = bigtable_constants.payana_comments_table_comment_id
payana_entity_to_comments_table_comment_id_list = bigtable_constants.payana_entity_to_comments_table_comment_id_list

# POST profile comments
# CURL request
"""
curl --location --request POST 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee' \
--data-raw '{
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}'
"""

url = "http://localhost:8888/entity/comments/"

profile_comments_json = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

entity_id = profile_comments_json[payana_comments_table_entity_id]

headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_comments_json), headers=headers)


print("Profile comments object creation status: " +
      str(response.status_code == 201))

# GET payana comments
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee'
"""

url = "http://localhost:8888/entity/comments/"
headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana entity comments read status: " + str(response.status_code == 200))

profile_entity_comments_response = response.json()

comment_id, _ = list(profile_entity_comments_response[entity_id].items())[0]

print("Profile entity comments creation verification status: " +
      str(len(profile_entity_comments_response[entity_id]) == 1))

"""
curl --location --request GET 'http://localhost:8888/entity/comments/details/' \
--header 'Content-Type: application/json' \
--header 'comment_id: bd87253f6de33321353645c41ce7e7bfa57c515430b2df01831ffe67f318706e'
"""

url = "http://localhost:8888/entity/comments/details/"
headers = {payana_comments_table_comment_id: comment_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana comments read status: " + str(response.status_code == 200))

profile_comments_response = response.json()

comment_id_response = profile_comments_response[comment_id][payana_comments_table_comment_id]

print("Profile comments creation verification status: " +
      str(comment_id == comment_id_response))


# Edit payana comments object
# POST profile comments
# CURL request
"""
curl --location --request POST 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee' \
--data-raw '{
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}'
"""

url = "http://localhost:8888/entity/comments/"

profile_comments_json = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic2!",
    "likes_count": "11",
    "comment_id": comment_id,
    "entity_id": "imagee"
}

entity_id = profile_comments_json[payana_comments_table_entity_id]

headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    profile_comments_json), headers=headers)

print("Profile comments object edit status: " +
      str(response.status_code == 200))


# GET payana comments
# CURL request

"""
curl --location --request GET 'http://localhost:8888/entity/comments/details/' \
--header 'Content-Type: application/json' \
--header 'comment_id: bd87253f6de33321353645c41ce7e7bfa57c515430b2df01831ffe67f318706e'
"""

url = "http://localhost:8888/entity/comments/details/"
headers = {payana_comments_table_comment_id: comment_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana comments read status: " + str(response.status_code == 200))

profile_comments_response = response.json()

payana_comments_table_comment = bigtable_constants.payana_comments_table_comment

comment = profile_comments_response[comment_id][payana_comments_table_comment]

print("Profile comments edit verification status: " +
      str(comment == "Beautiful pic2!"))

# POST profile comments
# CURL request
"""
curl --location --request POST 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee' \
--data-raw '{
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}'
"""

url = "http://localhost:8888/entity/comments/"

profile_comments_json = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "imagee"
}

entity_id = profile_comments_json[payana_comments_table_entity_id]

headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_comments_json), headers=headers)


print("Profile comments object creation status: " +
      str(response.status_code == 201))

# GET payana comments
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee'
"""

url = "http://localhost:8888/entity/comments/"
headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana entity comments read status: " + str(response.status_code == 200))

profile_entity_comments_response = response.json()
print(profile_entity_comments_response)

print("Profile entity comments creation verification status: " +
      str(len(profile_entity_comments_response[entity_id]) == 2))

# Delete comment row and entity comment table column value
"""
curl --location --request POST 'http://localhost:8888/entity/comments/delete/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee' \
--data-raw '{
    "payana_comment_id_list": ["a1a9d3748bbdf7d5c95e6620da0a07bcccd02c191d53a84ceb4ec57ecf9762f7"]
}'
"""

url = "http://localhost:8888/entity/comments/delete/"
headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

profile_comments_delete_cv_json = {
    payana_entity_to_comments_table_comment_id_list: [
        comment_id
    ]
}

response = requests.post(url, data=json.dumps(
    profile_comments_delete_cv_json), headers=headers)

print("Payana comments row and entity column values delete status: " +
      str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee'
"""

url = "http://localhost:8888/entity/comments/"
headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana entity comments read status: " + str(response.status_code == 200))

profile_entity_comments_response = response.json()

print("Profile entity comments creation verification status: " +
      str(comment_id not in profile_entity_comments_response[entity_id]))

"""
curl --location --request GET 'http://localhost:8888/entity/comments/details/' \
--header 'Content-Type: application/json' \
--header 'comment_id: bd87253f6de33321353645c41ce7e7bfa57c515430b2df01831ffe67f318706e'
"""

url = "http://localhost:8888/entity/comments/details/"
headers = {payana_comments_table_comment_id: comment_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana comments deletion verification status: " + str(response.status_code == 400))

# Delete payana coments row
"""
curl --location --request DELETE 'http://localhost:8888/entity/comments/entity/delete/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee'
"""

url = "http://localhost:8888/entity/comments/entity/delete/"

headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana comments row delete status: " + str(response.status_code == 200))


# GET payana likes
# CURL request
"""
curl --location --request GET 'http://localhost:8888/entity/comments/' \
--header 'Content-Type: application/json' \
--header 'entity_id: imagee'
"""

url = "http://localhost:8888/entity/comments/"
headers = {payana_comments_table_entity_id: entity_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana entity comments read status: " + str(response.status_code == 400))

"""
curl --location --request GET 'http://localhost:8888/entity/comments/details/' \
--header 'Content-Type: application/json' \
--header 'comment_id: bd87253f6de33321353645c41ce7e7bfa57c515430b2df01831ffe67f318706e'
"""

url = "http://localhost:8888/entity/comments/details/"
headers = {payana_comments_table_comment_id: comment_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana comments read status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
