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

payana_feed_search_itinerary_cache_profile_id = bigtable_constants.payana_feed_search_itinerary_cache_profile_id

"""
To make a city based search amongst all your followers/influencers/any profile ID -- not needed for Alpha
"""


# POST
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 12345' \
--data '{
    "profile_id": "12345",
    "excursion_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901"
        ]
    },
    "activity_guide_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901"
        ]
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ],
    "category": [
        "rating",
        "timestamp"
    ]
}'
"""

url = "http://127.0.0.1:8888/home/feed/search/"

payana_global_influencer_feed_search_itinerary_cache_object_json = {
    "profile_id": "12345",
    "excursion_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901"
        ]
    },
    "activity_guide_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901"
        ]
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ],
    "category": [
        "rating",
        "timestamp"
    ]
}

profile_id = payana_global_influencer_feed_search_itinerary_cache_object_json[
    payana_feed_search_itinerary_cache_profile_id]

headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_global_influencer_feed_search_itinerary_cache_object_json), headers=headers)


print("Payana global feed search itinerary cache objects creation status: " +
      str(response.status_code == 201))

profile_global_influencer_feed_search_itinerary_cache_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana feed search global itinearry cache object read status: " +
      str(response.status_code == 200))

payana_global_influencer_feed_search_itinerary_cache_object_response = response.json()

print(payana_global_influencer_feed_search_itinerary_cache_object_response)

print("Payana feed search global itinearry cache creation verification status: " +
      str(profile_id in payana_global_influencer_feed_search_itinerary_cache_object_response))

# Edit
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 12345' \
--data '{
    "profile_id": "12345",
    "excursion_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901",
            "3456789012345"
        ]
    },
    "activity_guide_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678901",
            "3456789012345"
        ]
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ],
    "category": [
        "rating",
        "timestamp"
    ]
}'
"""

url = "http://127.0.0.1:8888/home/feed/search/"

payana_global_influencer_feed_search_itinerary_cache_object_edit_json = {
    "profile_id": "12345",
    "excursion_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678012345"
        ],
        "seattle##washington##usa": [
            "123456789",
            "234567891",
            "345678012345"
        ]
    },
    "activity_guide_id": {
        "cupertino##california##usa": [
            "123456789",
            "234567891",
            "345678012345"
        ],
        "seattle##washington##usa": [
            "123456789",
            "234567891",
            "345678012345"
        ]
    },
    "activities": [
        "generic",
        "hiking",
        "romantic",
        "exotic"
    ],
    "category": [
        "rating",
        "timestamp"
    ]
}

new_excursion_id = "345678012345"
new_excursion_id_cf = "exotic_rating_excursion_id"
removed_excursion_id = "345678901"
city = "cupertino##california##usa"

headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.put(url, data=json.dumps(
    payana_global_influencer_feed_search_itinerary_cache_object_edit_json), headers=headers)


print("Payana global influencer feed search itinerary cache object edit status: " +
      str(response.status_code == 200))

profile_global_influencer_feed_search_itinerary_cache_object_response_json = response.json()

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana influencer feed search itinerary cache object read status: " +
      str(response.status_code == 200))

payana_global_influencer_feed_search_itinerary_cache_object_response = response.json()

print("Payana influencer feed search itinerary cache object edit verification status: " +
      str(new_excursion_id in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id][new_excursion_id_cf][city] and removed_excursion_id not in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id][new_excursion_id_cf][city]))

# Delete specific column family and column values
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/delete/values/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 12345' \
--data '{
    "exotic_rating_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_rating_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_timestamp_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_timestamp_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_rating_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_rating_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_timestamp_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    }
}'
"""

url = "http://127.0.0.1:8888/home/feed/search/delete/values/"

headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

payana_global_influencer_feed_search_itinerary_cache_object_delete_cv_json = {
    "exotic_rating_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_rating_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_timestamp_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "exotic_timestamp_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_rating_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_rating_excursion_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    },
    "generic_timestamp_activity_guide_id": {
        "cupertino##california##usa": "123456789##234567891##345678901##3456789012345"
    }
}

removed_city = "cupertino##california##usa"
removed_cf_one = "exotic_rating_activity_guide_id"
removed_cf_two = "generic_timestamp_activity_guide_id"

response = requests.post(url, data=json.dumps(
    payana_global_influencer_feed_search_itinerary_cache_object_delete_cv_json), headers=headers)

print("Payana global influencer feed search itinerary cache object column values delete CV status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana influencer feed search itinerary cache object read status: " +
      str(response.status_code == 200))

payana_global_influencer_feed_search_itinerary_cache_object_response = response.json()

print("Payana influencer feed search itinerary cache object delete CV verification status: " +
      str(removed_city not in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id][removed_cf_one] and removed_city not in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id][removed_cf_two]))

# Delete entire column family
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/delete/cf/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 12345' \
--data '{
    "romantic_rating_activity_guide_id": {},
    "romantic_rating_excursion_id": {},
    "romantic_timestamp_activity_guide_id": {},
    "romantic_timestamp_excursion_id": {}
}'
"""

url = "http://127.0.0.1:8888/home/feed/search/delete/cf/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

profile_feed_search_itinerary_cache_object_delete_cf_json = {
    "romantic_rating_activity_guide_id": {},
    "romantic_rating_excursion_id": {},
    "romantic_timestamp_activity_guide_id": {},
    "romantic_timestamp_excursion_id": {}
}

cf_delete_value_one = "romantic_rating_activity_guide_id"
cf_delete_value_two = "romantic_rating_excursion_id"

response = requests.post(url, data=json.dumps(
    profile_feed_search_itinerary_cache_object_delete_cf_json), headers=headers)

print("Payana global influencer feed search itinerary cache object column family delete CF status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana influencer feed search itinerary cache object read status: " +
      str(response.status_code == 200))

payana_global_influencer_feed_search_itinerary_cache_object_response = response.json()

print("Payana influencer feed search itinerary cache object delete CV verification status: " +
      str(cf_delete_value_one not in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id] and cf_delete_value_one not in payana_global_influencer_feed_search_itinerary_cache_object_response[profile_id]))

# Delete row
"""
curl --location --request DELETE 'http://127.0.0.1:8888/home/feed/search/delete/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/delete/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.delete(url, headers=headers)

print("Payana global influencer feed search itinerary cache object row delete status: " +
      str(response.status_code == 200))

# GET
# CURL request
"""
curl --location 'http://127.0.0.1:8888/home/feed/search/' \
--header 'Content-Type: application/json' \
--header 'city: cupertino##california##usa' \
--data ''
"""

url = "http://127.0.0.1:8888/home/feed/search/"
headers = {payana_feed_search_itinerary_cache_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana global influencer feed search itinerary cache object row delete status: " +
      str(response.status_code == 400))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
