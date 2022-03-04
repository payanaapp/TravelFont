from TravelFont.payana.payana_bl.bigtable_utils.constants import bigtable_constants

import os

payana_bucket_creation_config_file = os.path.join(bigtable_constants.travelfont_home, "payana/payana_bl/cloud_storage_utils/config/gcs_bucket_schema.json")

payana_bucket_location = "bucket_location"
payana_bucket_storage_class = "bucket_storage_class"

payana_bucket_profile_pictures = "payana_profile_pictures"
payana_bucket_itinerary_pictures = "payana_itinerary_pictures"


# payana CORS policy
payana_cors_policy = [
    {
        "origin": ["*"],
        "responseHeader": [
            "Content-Type",
            "x-goog-resumable"],
        "method": ['PUT', 'POST', 'GET'],
        "maxAgeSeconds": 3600
    }
]

# payana v4 policy constants
payana_upload_signed_url_expiration_time = 15
payana_download_signed_url_expiration_time = 15
