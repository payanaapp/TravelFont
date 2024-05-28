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

payana_activity_thumbnail = bigtable_constants.payana_activity_thumbnail
payana_activity_guide_thumbnail_table = bigtable_constants.payana_activity_guide_thumbnail_table
payana_activity_thumbnail_city = bigtable_constants.payana_activity_thumbnail_city

# POST 
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'Content-Type: application/json' \
--data '{
    "payana_activity_thumbnail": {
        "hiking": {
            "12345": "123456789"
        },
        "romantic": {
            "12345": "123456789"
        }   
    },
    "city": "cupertino##california##usa"
}'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

payana_activity_guide_thumbnail_json = {
    payana_activity_thumbnail: {
        "hiking": {
            "12345": "123456789"  # image ID: timestamp
        },
        "romantic": {
            "12345": "123456789"
        }   
    },
    payana_activity_thumbnail_city: "cupertina##california##usa"
}

city = payana_activity_guide_thumbnail_json[payana_activity_thumbnail_city]

activity_one = "_".join(["hiking", payana_activity_thumbnail])
activity_two = "_".join(["romantic", payana_activity_thumbnail])

activity_id_one_image_id = "12345"
activity_id_two_image_id = "12345"

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_activity_guide_thumbnail_json), headers=headers)


print("payana_activity_guide_thumbnail creation status: " + str(response.status_code == 201))

# GET
# CURL request 
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'city: cupertino##california##usa'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {payana_activity_thumbnail_city: city}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()

print("payana_activity_guide_thumbnail creation verification status: " +
      str(activity_id_one_image_id in payana_activity_thumbnail_response[city][activity_one]))

print(payana_activity_thumbnail_response)


# Edit 
"""
curl --location --request PUT 'http://localhost:8888/home/activity/thumbnail/' \
--header 'Content-Type: application/json' \
--data '{
    "payana_activity_thumbnail": {
        "hiking": {
            "123456": "123456789"
        },
        "romantic": {
            "123456": "123456789"
        }   
    },
    "city": "cupertino##california##usa"
}'
"""
payana_activity_guide_thumbnail_json_new = {
    payana_activity_thumbnail: {
        "hiking": {
            "123456": "123456789"
        },
        "romantic": {
            "123456": "123456789"
        }   
    },
    payana_activity_thumbnail_city: "cupertina##california##usa"
}

activity_id_one_image_id_new = "123456"
activity_id_two_image_id_new = "123456"

headers = {'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_activity_guide_thumbnail_json_new), headers=headers)

print("payana_activity_guide_thumbnail update status: " + str(response.status_code == 200))


# GET
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'city: cupertino##california##usa'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {payana_activity_thumbnail_city: city}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()
print("payana_activity_guide_thumbnail edit verification status: " +
      str(activity_id_one_image_id_new in payana_activity_thumbnail_response[city][activity_one]))


# Delete specific column values
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/delete/values/' \
--header 'city: cupertino##california##usa' \
--header 'Content-Type: application/json' \
--data '{
    "hiking_payana_activity_thumbnail": {
        "12345": "123456789"
    }
}'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/values/"
headers = {payana_activity_thumbnail_city: city, 'Content-Type': 'application/json'}

payana_activity_guide_thumbnail_json_delete_values = {
    "hiking_payana_activity_thumbnail": {
        "12345": "123456789"
    }
}

response = requests.post(url, data=json.dumps(
    payana_activity_guide_thumbnail_json_delete_values), headers=headers)

print("payana_activity_guide_thumbnail delete values status: " +
      str(response.status_code == 200))


# GET
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'city: cupertino##california##usa'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {payana_activity_thumbnail_city: city}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()
print("payana_activity_guide_thumbnail delete values verification status: " +
      str(activity_id_one_image_id not in payana_activity_thumbnail_response[city][activity_one]))

# Delete entire column family
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/delete/cf/' \
--header 'city: cupertino##california##usa' \
--header 'Content-Type: application/json' \
--data '{
    "hiking_payana_activity_thumbnail": ""
}'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/cf/"
headers = {payana_activity_thumbnail_city: city, 'Content-Type': 'application/json'}

payana_activity_guide_thumbnail_json_delete_cf = {
    activity_one: {
    }
}

response = requests.post(url, data=json.dumps(
    payana_activity_guide_thumbnail_json_delete_cf), headers=headers)

print("payana_activity_guide_thumbnail delete CF status: " +
      str(response.status_code == 200))


# GET
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'city: cupertino##california##usa'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {payana_activity_thumbnail_city: city}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail delete CF status: " + str(response.status_code == 200))

print("payana_activity_guide_thumbnail delete values verification status: " +
      str(activity_two not in payana_activity_thumbnail_response[city]))


# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/home/activity/thumbnail/delete/' \
--header 'city: cupertino##california##usa'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/"
headers = {payana_activity_thumbnail_city: city}

response = requests.delete(url, headers=headers)

print("payana_activity_guide_thumbnail delete row status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'city: cupertino##california##usa'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {payana_activity_thumbnail_city: city}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail delete row verification status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
