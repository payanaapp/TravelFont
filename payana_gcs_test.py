from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_init import payana_cloud_storage_init
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_cleanup import payana_cloud_storage_cleanup
from payana.payana_bl.cloud_storage_utils.payana_upload_storage_object import payana_upload_storage_object
from payana.payana_bl.cloud_storage_utils.payana_download_storage_object import payana_download_storage_object
from payana.payana_bl.cloud_storage_utils.payana_delete_storage_object import payana_delete_storage_object
from payana.payana_bl.cloud_storage_utils.payana_set_cors_policy_gcs_bucket import payana_set_cors_policy_storage_bucket, payana_get_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.payana_generate_gcs_signed_url import payana_generate_upload_signed_url, payana_generate_upload_resumable_signed_url, payana_generate_download_signed_url
from payana.payana_bl.cloud_storage_utils.payana_set_metadata_gcs_object import payana_set_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.payana_get_metadata_gcs_object import payana_get_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.constants.gcs_constants import payana_cors_policy

import os

payana_cloud_storage_init_status = payana_cloud_storage_init(
    bigtable_constants.gcs_client_config_path)

print("Payana Cloud Storage Init Status: " +
      str(payana_cloud_storage_init_status))

payana_gcs_image_upload_path = os.path.join(
    bigtable_constants.travelfont_home, "gcs_upload.jpg")
payana_gcs_video_upload_path = os.path.join(
    bigtable_constants.travelfont_home, "butterfly_flower_insect_nature_515.mp4")
payana_gcs_image_download_path = "downloaded_gcs_image.jpg"
payana_gcs_video_download_path = "downloaded_gcs_video.mp4"

profile_picture_object_name = "profile_picture_one"
profile_video_object_name = "payana_sample_video"

gcs_payana_profile_pictures_bucket_name = "payana_profile_pictures"

metadata_object = {'payana_object_id': '123467QWERTY123467QWERTY123467QWERTY',
                   'author_name': 'abkr', 'location': 'Cupertino'}

# set a CORS policy
# payana_set_cors_policy_status = payana_set_cors_policy_storage_bucket(
#     gcs_payana_profile_pictures_bucket_name, payana_cors_policy)

# print("Payana Cors Policy Status: " + str(payana_set_cors_policy_status))

# Get a CORS policy
payana_get_cors_policy_status = payana_get_cors_policy_storage_bucket(
    gcs_payana_profile_pictures_bucket_name)

print("Payana Cors Policy Read: " + str(payana_get_cors_policy_status))

# upload a blob
payana_profile_picture_upload_storage_object_status = payana_upload_storage_object(
    gcs_payana_profile_pictures_bucket_name, payana_gcs_image_upload_path, profile_picture_object_name)

print("Payana Profile Picture Upload Storage Object Status: " +
      str(payana_profile_picture_upload_storage_object_status))

# Set metadata for an object
payana_profile_picture_set_metadata_gcs_status = payana_set_metadata_gcs_object(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name, metadata_object)

print("Payana Profile Picture Set Metadata GCS Status: " +
      str(payana_profile_picture_set_metadata_gcs_status))

# Get metadata of an object
payana_profile_picture_get_metadata_gcs_object_content = payana_get_metadata_gcs_object(gcs_payana_profile_pictures_bucket_name,
                                                                                        profile_picture_object_name)

print("Payana Profile Picture Metadata GCS Object: " +
      str(payana_profile_picture_get_metadata_gcs_object_content.name) + ", " + str(payana_profile_picture_get_metadata_gcs_object_content.id) + ", " + str(payana_profile_picture_get_metadata_gcs_object_content.md5_hash))

print("Payana Profile Picture Metadata GCS Custom content: " +
      str(payana_profile_picture_get_metadata_gcs_object_content.metadata))

# print signed URL for upload
payana_profile_picture_upload_signed_url_content = payana_generate_upload_signed_url(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name)

print("Payana Profile Picture Upload Signed URL Content: " +
      str(payana_profile_picture_upload_signed_url_content))

# print signed URL for resumable upload
payana_profile_picture_upload_signed_url_content = payana_generate_upload_resumable_signed_url(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name)

print("Payana Profile Picture Resumable Upload Signed URL Content: " +
      str(payana_profile_picture_upload_signed_url_content))

# print signed URL for download
payana_profile_picture_download_signed_url_content = payana_generate_download_signed_url(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name)

print("Payana Profile Picture Download Signed URL Content: " +
      str(payana_profile_picture_download_signed_url_content))

# download a blob - Image
payana_profile_picture_download_storage_object_status = payana_download_storage_object(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name, payana_gcs_image_download_path)

print("Payana Profile Picture Download Storage Object Status: " +
      str(payana_profile_picture_download_storage_object_status))

# delete a blob
payana_profile_picture_delete_storage_object_status = payana_delete_storage_object(
    gcs_payana_profile_pictures_bucket_name, profile_picture_object_name)

print("Payana Profile Picture Delete Storage Object Status: " +
      str(payana_profile_picture_delete_storage_object_status))

# upload a blob - Video
payana_profile_picture_upload_storage_object_status = payana_upload_storage_object(
    gcs_payana_profile_pictures_bucket_name, payana_gcs_video_upload_path, profile_video_object_name)

print("Payana Profile Picture Upload Storage Object Status: " +
      str(payana_profile_picture_upload_storage_object_status))

# download a blob - Video
payana_profile_picture_download_storage_object_status = payana_download_storage_object(
    gcs_payana_profile_pictures_bucket_name, profile_video_object_name, payana_gcs_video_download_path)

print("Payana Profile Picture Download Storage Object Status: " +
      str(payana_profile_picture_download_storage_object_status))

# delete a blob
payana_profile_picture_delete_storage_object_status = payana_delete_storage_object(
    gcs_payana_profile_pictures_bucket_name, profile_video_object_name)

payana_cloud_storage_cleanup_status = payana_cloud_storage_cleanup(
    bigtable_constants.gcs_client_config_path)

print("Payana Cloud Storage Cleanup Status: " +
      str(payana_cloud_storage_cleanup_status))
