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
        "adventure": {
            "12345": "123456789"
        }   
    }
}'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

payana_activity_guide_thumbnail_json = {
    payana_activity_thumbnail: {
        "hiking": {
            "12345": "123456789"
        },
        "adventure": {
            "12345": "123456789"
        }   
    }
}

activity_id_one = "hiking"
activity_id_two = "adventure"

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
--header 'activity_id: hiking'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {'activity_id': activity_id_one}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()

print("payana_activity_guide_thumbnail creation verification status: " +
      str(activity_id_one_image_id in payana_activity_thumbnail_response[activity_id_one][payana_activity_thumbnail]))


# Edit 
"""
curl --location --request PUT 'http://localhost:8888/home/activity/thumbnail/' \
--header 'Content-Type: application/json' \
--data '{
    "payana_activity_thumbnail": {
        "hiking": {
            "123456": "123456789"
        },
        "adventure": {
            "123456": "123456789"
        }   
    }
}'
"""
payana_activity_guide_thumbnail_json_new = {
    payana_activity_thumbnail: {
        "hiking": {
            "123456": "123456789"
        },
        "adventure": {
            "123456": "123456789"
        }   
    }
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
--header 'activity_id: hiking'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {'activity_id': activity_id_one}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()
print("payana_activity_guide_thumbnail edit verification status: " +
      str(activity_id_one_image_id_new in payana_activity_thumbnail_response[activity_id_one][payana_activity_thumbnail]))


# Delete specific column values
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/delete/values/' \
--header 'activity_id: hiking' \
--header 'Content-Type: application/json' \
--data '{
    "payana_activity_thumbnail": {
        "12345": "123456789"
    }
}'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/values/"
headers = {'activity_id': activity_id_one, 'Content-Type': 'application/json'}

payana_activity_guide_thumbnail_json_delete_values = {
    "payana_activity_thumbnail": {
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
--header 'activity_id: hiking'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {'activity_id': activity_id_one}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail read status: " + str(response.status_code == 200))

payana_activity_thumbnail_response = response.json()
print("payana_activity_guide_thumbnail delete values verification status: " +
      str(activity_id_one_image_id not in payana_activity_thumbnail_response[activity_id_one][payana_activity_thumbnail]))

# Delete entire column family
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/delete/cf/' \
--header 'activity_id: hiking' \
--header 'Content-Type: application/json' \
--data '{
    "payana_activity_thumbnail": ""
}'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/cf/"
headers = {'activity_id': activity_id_one, 'Content-Type': 'application/json'}

payana_activity_guide_thumbnail_json_delete_cf = {
    "payana_activity_thumbnail": {
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
--header 'activity_id: hiking'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {'activity_id': activity_id_one}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail delete CF status: " + str(response.status_code == 400))


# Delete row
"""
curl --location --request DELETE 'http://localhost:8888/home/activity/thumbnail/delete/' \
--header 'activity_id: adventure'
"""
url = "http://localhost:8888/home/activity/thumbnail/delete/"
headers = {'activity_id': activity_id_two}

response = requests.delete(url, headers=headers)

print("payana_activity_guide_thumbnail delete row status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location 'http://localhost:8888/home/activity/thumbnail/' \
--header 'activity_id: adventure'
"""

url = "http://localhost:8888/home/activity/thumbnail/"

headers = {'activity_id': activity_id_two}

response = requests.get(url, headers=headers)

print("payana_activity_guide_thumbnail delete row verification status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
