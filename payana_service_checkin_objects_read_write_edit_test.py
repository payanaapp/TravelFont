from datetime import datetime
from tabnanny import check

from pyrsistent import b

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

# POST profile checkin objects
# CURL request
"""
curl --location --request POST 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "image_id_list": {
        "1": "img_id_1",
        "2": "img_id_2",
        "3": "img_id_3"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "8", "roadtrip": "9"},
    "instagram_metadata": {
        "instagram_embed_url": "xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "checkin_id": "",
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "Land'\''s End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}
'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

payana_checkin_obj_json = {
    "image_id_list": {
        "1": "img_id_1",
        "2": "img_id_2",
        "3": "img_id_3"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "8", "roadtrip": "9"},
    "instagram_metadata": {
        "instagram_embed_url": "xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "checkin_id": "",
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "Land's End",
        # Useful when search happens on a specific profile for a given city/state/country
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}

payana_checkin_id = bigtable_constants.payana_checkin_id

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_checkin_obj_json), headers=headers)

post_response = response.json()

checkin_id = post_response[payana_checkin_id]

print("Profile checkin object creation status: " +
      str(response.status_code == 201))

# GET payana checkin objects
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: 730665e80500a504eb0caab7a15f65c76dc6465efb9090546595e6318694be05'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

headers = {payana_checkin_id: checkin_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana checkin object read status: " + str(response.status_code == 200))

profile_checkin_response = response.json()

print(profile_checkin_response)

payana_checkin_metadata = bigtable_constants.payana_checkin_metadata

print("Profile checkin object creation verification status: " +
      str(profile_checkin_response[checkin_id][payana_checkin_metadata][payana_checkin_id] == checkin_id))


# Edit payana checkin object
# CURL request
"""
curl --location --request PUT 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: d5abe50bba3a82383300e46ee14ce283d30d70bc9a4dc855a853011f124b3ba8' \
--data-raw '{
    "image_id_list": {
        "4": "img_id_4"
    },
    "activities_list": {"hiking": "8", "roadtrip": "9"},
    "instagram_metadata": {
        "instagram_embed_url": "abc_xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "abc_xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "checkin_id": "d5abe50bba3a82383300e46ee14ce283d30d70bc9a4dc855a853011f124b3ba8",
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "Land'\''s End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}
'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

payana_checkin_obj_edit_json = {
    "image_id_list": {
        "4": "img_id_4"
    },
    "activities_list": {"hiking": "8", "roadtrip": "9"},
    "instagram_metadata": {
        "instagram_embed_url": "abc_xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "abc_xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "create_timestamp": "123456789",
        "last_updated_timestamp": "123456789",
        "checkin_id": checkin_id,
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "Land's End",
        "city": "SF##California##USA",
        "state": "California##USA",
        "country": "USA"
    }
}


headers = {payana_checkin_id: checkin_id,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_checkin_obj_edit_json), headers=headers)

print("Profile checkin object edit status: " +
      str(response.status_code == 200))


# GET payana checkin objects
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: 730665e80500a504eb0caab7a15f65c76dc6465efb9090546595e6318694be05'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

headers = {payana_checkin_id: checkin_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana checkin object read status: " + str(response.status_code == 200))

profile_checkin_response = response.json()

payana_checkin_airbnb_metadata = bigtable_constants.payana_checkin_airbnb_metadata
payana_checkin_airbnb_embed_url = bigtable_constants.payana_checkin_airbnb_embed_url

print("Profile checkin object edit verification status: " +
      str(profile_checkin_response[checkin_id][payana_checkin_airbnb_metadata][payana_checkin_airbnb_embed_url] == payana_checkin_obj_edit_json[payana_checkin_airbnb_metadata][payana_checkin_airbnb_embed_url]))

# Delete specific column family and column values
"""
curl --location --request POST 'http://127.0.0.1:8888/entity/checkin/delete/values/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: d5abe50bba3a82383300e46ee14ce283d30d70bc9a4dc855a853011f124b3ba8' \
--data-raw '{
    "image_id_list": [
        "1"
    ],
    "checkin_metadata": [
        "transport_mode",
        "description"
    ]
}'
"""

url = "http://127.0.0.1:8888/entity/checkin/delete/values/"
headers = {payana_checkin_id: checkin_id, 'Content-Type': 'application/json'}

payana_checkin_value_delete_json = {
    "image_id_list": [
        "1"
    ],
    "checkin_metadata": [
        "transport_mode",
        "description"
    ]
}

response = requests.post(url, data=json.dumps(
    payana_checkin_value_delete_json), headers=headers)

print("Profile checkin objects contents column values delete status: " +
      str(response.status_code == 200))


# GET payana checkin objects
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: 730665e80500a504eb0caab7a15f65c76dc6465efb9090546595e6318694be05'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

headers = {payana_checkin_id: checkin_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana checkin object read status: " + str(response.status_code == 200))

profile_checkin_response = response.json()

payana_checkin_transport_mode = bigtable_constants.payana_checkin_transport_mode
payana_checkin_metadata = bigtable_constants.payana_checkin_metadata
payana_checkin_column_family_description = bigtable_constants.payana_checkin_column_family_description

print("Profile checkin object delete values verification status: " +
      str(payana_checkin_transport_mode not in profile_checkin_response[checkin_id][payana_checkin_metadata] or payana_checkin_column_family_description not in profile_checkin_response[checkin_id][payana_checkin_metadata]))

# Delete entire column family
"""
curl --location --request POST 'http://127.0.0.1:8888/entity/checkin/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: d5abe50bba3a82383300e46ee14ce283d30d70bc9a4dc855a853011f124b3ba8' \
--data-raw '{
    "image_id_list": {},
    "checkin_metadata": {}
}'
"""
url = "http://127.0.0.1:8888/entity/checkin/delete/cf/"
headers = {payana_checkin_id: checkin_id, 'Content-Type': 'application/json'}

profile_checkin_delete_cf_json = {
    "image_id_list": {},
    "checkin_metadata": {}
}

response = requests.post(url, data=json.dumps(
    profile_checkin_delete_cf_json), headers=headers)

print("Profile checkin contents column family delete status: " +
      str(response.status_code == 200))


# GET payana checkin objects
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: 730665e80500a504eb0caab7a15f65c76dc6465efb9090546595e6318694be05'
"""

url = "http://127.0.0.1:8888/entity/checkin/"

headers = {payana_checkin_id: checkin_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana checkin object read status: " + str(response.status_code == 200))

profile_checkin_response = response.json()

print("Profile checkin object delete CF verification status: " +
      str(payana_checkin_metadata not in profile_checkin_response[checkin_id]))

# Delete check in object
"""
curl --location --request DELETE 'http://127.0.0.1:8888/entity/checkin/delete/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: 730665e80500a504eb0caab7a15f65c76dc6465efb9090546595e6318694be05'
"""

url = "http://127.0.0.1:8888/entity/checkin/delete/"
headers = {payana_checkin_id: checkin_id}

response = requests.delete(url, headers=headers)

print("Payana checkin row delete status: " +
      str(response.status_code == 200))


# GET checkin itinerary
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/entity/checkin/' \
--header 'Content-Type: application/json' \
--header 'checkin_id: d5abe50bba3a82383300e46ee14ce283d30d70bc9a4dc855a853011f124b3ba8'
"""

url = "http://127.0.0.1:8888/entity/checkin/"
headers = {payana_checkin_id: checkin_id}

response = requests.get(url, headers=headers)

print("Payana checkin row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
