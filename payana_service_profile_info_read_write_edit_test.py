from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper, bigtable_read_row_key_wrapper
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

from urllib import response
import requests
import json

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

payana_profile_table_personal_info_column_family = bigtable_constants.payana_profile_table_personal_info_column_family
payana_profile_favorite_places_preference = bigtable_constants.payana_profile_favorite_places_preference
payana_profile_favorite_activities_preference = bigtable_constants.payana_profile_favorite_activities_preference
payana_profile_table_thumbnail_travel_buddies = bigtable_constants.payana_profile_table_thumbnail_travel_buddies
payana_profile_table_top_activities_tracker_rating = bigtable_constants.payana_profile_table_top_activities_tracker_rating


payana_profile_table_profile_name = bigtable_constants.payana_profile_table_profile_name
payana_profile_table_user_name = bigtable_constants.payana_profile_table_user_name
payana_profile_table_blog_url = bigtable_constants.payana_profile_table_blog_url
payana_profile_table_profile_description = bigtable_constants.payana_profile_table_profile_description
payana_profile_table_profile_id = bigtable_constants.payana_profile_table_profile_id
payana_profile_table_email = bigtable_constants.payana_profile_table_email
payana_profile_table_phone = bigtable_constants.payana_profile_table_phone
payana_profile_table_private_account = bigtable_constants.payana_profile_table_private_account
payana_profile_table_gender = bigtable_constants.payana_profile_table_gender
payana_profile_table_date_of_birth = bigtable_constants.payana_profile_table_date_of_birth
payana_profile_table_doj = bigtable_constants.payana_profile_table_doj
payana_profile_table_profile_pictures = bigtable_constants.payana_profile_table_profile_pictures

# POST profile info
# CURL request
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "personal_information":
    {
        "profile_name": "abkr",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111",
        "doj" : "11/11/1111",
        "venmo_id": "abkr"
    },
    "top_activities_tracker_rating":
    {
        "hiking": "0.67",
        "adventure": "0.4",
        "fashion": "0.78"
    },
    "favorite_places_preference": {
        "cupertino##california##usa": "1234578",
        "california##usa": "1234578",
        "usa": "1234578",
        "sanfrancisco##california##usa": "1234578",
        "oregon##usa": "1234578",
        "france": "1234578"
    },
    "favorite_activities_preference": {
        "hiking": "1",
        "ski trips": "2",
        "adventures": "3",
        "spring break" : "4",
        "road trips" : "5",
        "food trips" : "6"
    },
    "thumbnail_travel_buddies" : {
        "123456" : "1",
        "234567" : "2",
        "345678" : "3",
        "456789" : "4",
        "567890" : "5",
        "678911" : "6",
        "678921" : "7"
    }
}'
"""

url = "http://127.0.0.1:8888/profile/info/"

profile_info_json = {
    payana_profile_table_personal_info_column_family:
    {
        "profile_name": "abkr",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111",
        "doj": "11/11/1111",
        "venmo_id": "abkr"
    },
    payana_profile_table_top_activities_tracker_rating:
    {
        "hiking": "0.67",
        "adventure": "0.4",
        "fashion": "0.78"
    },
    payana_profile_favorite_places_preference: {
        "cupertino##california##usa": "1234578",  # place ID
        "california##usa": "1234578",
        "usa": "1234578",
        "sanfrancisco##california##usa": "1234578",
        "oregon##usa": "1234578",
        "france": "1234578"
    },
    payana_profile_favorite_activities_preference: {
        "hiking": "1",
        "ski trips": "2",
        "adventures": "3",
        "spring break": "4",
        "road trips": "5",
        "food trips": "6"
    },
    payana_profile_table_thumbnail_travel_buddies: {
        "123456": "1",
        "234567": "2",
        "345678": "3",
        "456789": "4",
        "567890": "5",
        "678911": "6",
        "678921": "7",
    },
    payana_profile_table_profile_pictures: {
        "123456789": "profile_picture_id_1"
    }
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    profile_info_json), headers=headers)


print("Profile creation status: " + str(response.status_code == 201))

profile_info_response_json = response.json()

profile_id = profile_info_response_json['profile_id']

print("Profile creation verification status: " +
      str(profile_id is not None and len(profile_id) > 0))

# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile read status: " + str(response.status_code == 200))

profile_info_response = response.json()
print("Profile creation verification status: " +
      str(profile_info_response[profile_id][payana_profile_table_personal_info_column_family][payana_profile_table_profile_name] == profile_info_json[payana_profile_table_personal_info_column_family][payana_profile_table_profile_name]))


# Edit personal information
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "personal_information":
    {
        "profile_name": "abkr",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111",
        "doj" : "11/11/1111",
        "venmo_id": "abkr"
    }
}'
"""
profile_info_personal_information_json = {
    payana_profile_table_personal_info_column_family:
    {
        "profile_name": "abkr1",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111",
        "doj": "11/11/1111"
    }
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_info_personal_information_json), headers=headers)

print("Profile info update status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info update read status: " + str(response.status_code == 200))

profile_info_update_response = response.json()
print("Profile info update read verification status: " +
      str(profile_info_update_response[profile_id][payana_profile_table_personal_info_column_family][payana_profile_table_profile_name] == profile_info_personal_information_json[payana_profile_table_personal_info_column_family][payana_profile_table_profile_name]))


# Edit top activities tracker rating
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "top_activities_tracker_rating":
    {
        "hiking": "0.67",
        "adventure": "0.4",
        "fashion": "0.78"
    }
}'
"""
profile_info_top_activities_tracker_rating_json = {
    payana_profile_table_top_activities_tracker_rating:
    {
        "hiking": "0.88",
        "adventure": "0.78",
        "fashion": "0.98"
    }
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_info_top_activities_tracker_rating_json), headers=headers)

print("Profile activities tracker update status: " +
      str(response.status_code == 200))

# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info top_activities_tracker_rating update read status: " +
      str(response.status_code == 200))

profile_info_top_activities_tracker_rating_update_response = response.json()

print("Profile info top_activities_tracker_rating update read verification status: " +
      str(profile_info_top_activities_tracker_rating_update_response[profile_id][payana_profile_table_top_activities_tracker_rating]["hiking"] == profile_info_top_activities_tracker_rating_json[payana_profile_table_top_activities_tracker_rating]["hiking"]))

# Edit favorite_places_preference
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "favorite_places_preference": {
        "cupertino##california##usa": "1234578",
        "california##usa": "1234578",
        "usa": "95014",
        "sanfrancisco##california##usa": "1234578",
        "oregon##usa": "1234578",
        "france": "1234578"
    }
}'
"""
profile_info_favorite_places_preference_json = {
    payana_profile_favorite_places_preference:
    {
        "cupertino##california##usa": "1234578",
        "california##usa": "1234578",
        "usa": "1234578",
        "sanfrancisco##california##usa": "1234578",
        "oregon##usa": "1234578",
        "france": "1234578"
    }
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_info_favorite_places_preference_json), headers=headers)

print("Profile favorite places preference update status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info favorite_places_preference update read status: " +
      str(response.status_code == 200))

profile_info_favorite_places_preference_update_response = response.json()
print("Profile info favorite_places_preference update read verification status: " +
      str(profile_info_favorite_places_preference_update_response[profile_id][payana_profile_favorite_places_preference]["usa"] == profile_info_favorite_places_preference_json[payana_profile_favorite_places_preference]["usa"]))

# Edit favorite_activities_preference
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "favorite_activities_preference": {
        "hiking": "1",
        "ski trips": "2",
        "adventures": "3",
        "spring break" : "4",
        "road trips" : "5",
        "food trips" : "6"
    }
}'
"""
profile_info_favorite_activities_preference_json = {
    payana_profile_favorite_activities_preference:
    {
        "hiking": "12",
        "ski trips": "2",
        "adventures": "3",
        "spring break": "4",
        "road trips": "5",
        "food trips": "6"
    }
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_info_favorite_activities_preference_json), headers=headers)

print("Profile favorite activities update status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info favorite_activities_preference update read status: " +
      str(response.status_code == 200))

profile_info_favorite_activities_preference_update_response = response.json()
print("Profile info favorite_activities_preference update read verification status: " +
      str(profile_info_favorite_activities_preference_update_response[profile_id][payana_profile_favorite_activities_preference]["hiking"] == profile_info_favorite_activities_preference_json[payana_profile_favorite_activities_preference]["hiking"]))

# Edit thumbnail_travel_buddies
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 123456' \
--header 'Content-Type: application/json' \
--data-raw '{
    "thumbnail_travel_buddies" : {
        "123456" : "1",
        "234567" : "2",
        "345678" : "3",
        "456789" : "4",
        "567890" : "5",
        "678911" : "6",
        "678921" : "7"
    }
}'
"""
profile_info_thumbnail_travel_buddies_json = {
    payana_profile_table_thumbnail_travel_buddies:
    {
        "123456": "98",
        "234567": "2",
        "345678": "3",
        "456789": "4",
        "567890": "5",
        "678911": "6",
        "678921": "7"
    }
}

headers = {'Content-Type': 'application/json', 'profile_id': profile_id}

response = requests.put(url, data=json.dumps(
    profile_info_thumbnail_travel_buddies_json), headers=headers)

print("Profile thumbnail travel buddies update status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info thumbnail_travel_buddies update read status: " +
      str(response.status_code == 200))

profile_info_thumbnail_travel_buddies_update_response = response.json()
print("Profile info thumbnail_travel_buddies update read verification status: " +
      str(profile_info_thumbnail_travel_buddies_update_response[profile_id][payana_profile_table_thumbnail_travel_buddies]["123456"] == profile_info_thumbnail_travel_buddies_json[payana_profile_table_thumbnail_travel_buddies]["123456"]))

# Delete specific column family and column values
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/delete/values/' \
--header 'profile_id: d6b088551f82508ae569668ce146db6f56a90a762c11eb0901cbe87e9bede637' \
--header 'Content-Type: application/json' \
--data-raw '{
    "thumbnail_travel_buddies" : {
        "123456" : "1",
        "234567" : "2",
        "345678" : "3",
        "456789" : "4",
        "567890" : "5",
        "678911" : "6",
        "678921" : "7"
    }
}'
"""
url = "http://127.0.0.1:8888/profile/info/delete/values/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

profile_info_thumbnail_travel_buddies_json = {
    payana_profile_table_thumbnail_travel_buddies:
    {
        "123456": "98",
        "678921": "7"
    }
}

response = requests.post(url, data=json.dumps(
    profile_info_thumbnail_travel_buddies_json), headers=headers)

print("Profile info contents delete status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info contents delete read status: " +
      str(response.status_code == 200))


profile_info_thumbnail_travel_buddies_delete_response = response.json()

print("Profile info contents delete verification status: " +
      str("678921" not in profile_info_thumbnail_travel_buddies_delete_response[profile_id][payana_profile_table_thumbnail_travel_buddies] and "123456" not in profile_info_thumbnail_travel_buddies_delete_response[profile_id][payana_profile_table_thumbnail_travel_buddies] and "234567" in profile_info_thumbnail_travel_buddies_delete_response[profile_id][payana_profile_table_thumbnail_travel_buddies]))

# Delete thumbnail_travel_buddies - entire column family
"""
curl --location --request POST 'http://127.0.0.1:8888/profile/info/delete/cf/' \
--header 'profile_id: d6b088551f82508ae569668ce146db6f56a90a762c11eb0901cbe87e9bede637' \
--header 'Content-Type: application/json' \
--data-raw '{
    "thumbnail_travel_buddies" : {
        "123456" : "1",
        "234567" : "2",
        "345678" : "3",
        "456789" : "4",
        "567890" : "5",
        "678911" : "6",
        "678921" : "7"
    }
}'
"""
url = "http://127.0.0.1:8888/profile/info/delete/cf/"
headers = {'profile_id': profile_id, 'Content-Type': 'application/json'}

profile_info_thumbnail_travel_buddies_json = {
    payana_profile_table_thumbnail_travel_buddies:
    {
    }
}

response = requests.post(url, data=json.dumps(
    profile_info_thumbnail_travel_buddies_json), headers=headers)

print("Profile info contents delete status: " +
      str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info contents delete read status: " +
      str(response.status_code == 200))

profile_info_thumbnail_travel_buddies_delete_response = response.json()

print("Profile info contents delete verification status: " +
      str(payana_profile_table_thumbnail_travel_buddies not in profile_info_thumbnail_travel_buddies_delete_response[profile_id]))


# Delete profile info
"""
curl --location --request DELETE 'http://127.0.0.1:8888/profile/info/delete/' \
--header 'profile_id: da8fcdcf7ee10d71961fe4251de602e8f42d2a39fd77758176552f229ad32859'
"""
url = "http://127.0.0.1:8888/profile/info/delete/"
headers = {'profile_id': profile_id}

response = requests.delete(url, headers=headers)

print("Profile info delete status: " + str(response.status_code == 200))


# GET profile info
# CURL request
"""
curl --location --request GET 'http://127.0.0.1:8888/profile/info/' \
--header 'profile_id: 6ab6a9d059ab8f9a9e26cb51e27151e62b0e90f3f72b96789b095b8373ff7a2f'
"""

url = "http://127.0.0.1:8888/profile/info/"
headers = {'profile_id': profile_id}

response = requests.get(url, headers=headers)

print("Profile info delete status: " + str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
