from TravelFont.payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_init import payana_cloud_storage_init
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_cleanup import payana_cloud_storage_cleanup
from payana.payana_bl.cloud_storage_utils.payana_upload_storage_object import payana_profile_picture_upload_storage_object
from payana.payana_bl.cloud_storage_utils.payana_download_storage_object import payana_profile_picture_download_storage_object
from payana.payana_bl.cloud_storage_utils.payana_delete_storage_object import payana_profile_picture_delete_storage_object
from payana.payana_bl.cloud_storage_utils.payana_set_cors_policy_gcs_bucket import payana_set_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.payana_generate_gcs_signed_url import payana_profile_picture_download_signed_url, payana_profile_picture_upload_signed_url, payana_profile_picture_resumable_upload_signed_url
from payana.payana_bl.cloud_storage_utils.payana_set_metadata_gcs_object import payana_profile_picture_set_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.payana_get_metadata_gcs_object import payana_profile_picture_get_metadata_gcs_object

import os

payana_cloud_storage_init(
    os.path.join(bigtable_constants.travelfont_home, "payana/payana_bl/cloud_storage_utils/config/gcs_bucket_schema.json"))

# set a CORS policy
# payana_set_cors_policy_storage_bucket("payana_profile_pictures", [])

# upload a blob
payana_profile_picture_upload_storage_object(
    "/Users/abhinandankelgereramesh/Desktop/sky-diving/Abhinandan_pic/G0021193.JPG", "profile_picture_one")

# Set metadata for an object
payana_profile_picture_set_metadata_gcs_object(
    "profile_picture_one", {'author_name': 'abkr', 'location': 'Cupertino'})

# Get metadata of an object
print(payana_profile_picture_get_metadata_gcs_object("profile_picture_one"))

# print signed URL for dowload
# payana_profile_picture_download_signed_url("profile_picture_one")

# download a blob
# payana_profile_picture_download_storage_object(
#     "profile_picture_one", "image.jpg")

# delete a blob
payana_profile_picture_delete_storage_object("profile_picture_one")

payana_cloud_storage_cleanup(
    os.path.join(bigtable_constants.travelfont_home, "payana/payana_bl/cloud_storage_utils/config/gcs_bucket_schema.json"))
