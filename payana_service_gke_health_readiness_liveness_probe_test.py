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

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/health/live' \
--header 'Content-Type: application/json'
"""

url = "http://127.0.0.1:8888/health/live/"

headers = {'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana liveness status check: " +
      str(response.status_code == 200))

# GET read
# CURL request
"""
curl --location 'http://127.0.0.1:8888/health/ready' \
--header 'Content-Type: application/json'
"""

url = "http://127.0.0.1:8888/health/ready/"

headers = {'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)

print("Payana readiness status check: " +
      str(response.status_code == 200))
