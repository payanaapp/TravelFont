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

payana_sign_up_mail_id_list_profile_id = bigtable_constants.payana_sign_up_mail_id_list_profile_id
payana_sign_up_mail_id_list_column_family = bigtable_constants.payana_sign_up_mail_id_list_column_family
payana_sign_up_mail_id_list_profile_name = bigtable_constants.payana_sign_up_mail_id_list_profile_name

# POST write
# CURL request
"""
curl --location 'http://127.0.0.1:8888/entity/signup/' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--data-raw '{
    "profile_name": "abkr",
    "sign_up_mail_id_list": [
        "payanaapp@gmail.com"
    ],
    "itinerary_id": "12345",
    "itinerary_name": "Seattle itinerary!"
}'
"""

url = "http://127.0.0.1:8888/entity/signup/"

payana_sign_up_mail_id_notification_json = {
    "profile_name": "abkr",
    "sign_up_mail_id_list": [
        "payanaapp@gmail.com"
    ],
    "itinerary_id": "12345",
    "itinerary_name": "Seattle itinerary!"
}

profile_id = "1235"

headers = {payana_sign_up_mail_id_list_profile_id: profile_id,
           'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(
    payana_sign_up_mail_id_notification_json), headers=headers)


print("Payana mail id sign up notification creation status: " +
      str(response.status_code == 201))

payana_sign_up_mail_id_notification_response_json = response.json()
