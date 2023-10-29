from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_init import payana_cloud_storage_init
from payana.payana_bl.cloud_storage_utils.payana_cloud_storage_cleanup import payana_cloud_storage_cleanup
from payana.payana_bl.cloud_storage_utils.payana_upload_storage_object import payana_upload_storage_object
from payana.payana_bl.cloud_storage_utils.payana_download_storage_object import payana_download_storage_object
from payana.payana_bl.cloud_storage_utils.payana_delete_storage_object import payana_delete_storage_object
from payana.payana_bl.cloud_storage_utils.payana_set_cors_policy_gcs_bucket import payana_set_cors_policy_storage_bucket
from payana.payana_bl.cloud_storage_utils.payana_generate_gcs_signed_url import payana_generate_upload_signed_url, payana_generate_upload_resumable_signed_url, payana_generate_download_signed_url
from payana.payana_bl.cloud_storage_utils.payana_set_metadata_gcs_object import payana_set_metadata_gcs_object
from payana.payana_bl.cloud_storage_utils.payana_get_metadata_gcs_object import payana_get_metadata_gcs_object

import os
import io
import base64

from urllib import response
import requests
import json

payana_cloud_storage_init_status = payana_cloud_storage_init(
    bigtable_constants.gcs_client_config_path)

payana_gcs_image_upload_path = os.path.join(
    bigtable_constants.travelfont_home, "G0011163.jpg")
payana_gcs_video_upload_path = os.path.join(
    bigtable_constants.travelfont_home, "butterfly_flower_insect_nature_515.mp4")
payana_gcs_image_download_path = "downloaded_gcs_image.jpg"
payana_gcs_video_download_path = "downloaded_gcs_video.mp4"

profile_picture_bucket_name = "profile_picture_one"
profile_video_bucket_name = "payana_sample_video"

gcs_payana_profile_pictures_bucket_name = "payana_profile_pictures"

# Get Signed Upload URL
"""
curl --location --request GET 'http://localhost:8888/entity/signed_url/upload' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one'
"""

url = "http://localhost:8888/entity/signed_url/upload/"

headers = {'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.get(url, headers=headers)

print("Profile signed upload URL GET status: " +
      str(response.status_code == 200))

payana_signed_url = response.json()

print("Profile signed upload URL GET status: " +
      str(response is not None or len(payana_signed_url) > 0))

# image upload using the signed URL
"""
curl --location --request PUT 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230912T043809Z&X-Goog-Expires=900&X-Goog-SignedHeaders=content-type%3Bhost&X-Goog-Signature=03e17da81332b76c7037215a41805b8c987e6987a3b6f36b0e9d649891385473d830eff078cde4a11a78b9e0b9298cff237bcd21ac14e4bb90b9f5c2c49f7f3cb3ade7c491baaf088f486bc1fde7704aac9f6aeb01f2ef34c92216a93611f89714fea33ba2d57bbe3d776447e68906d9fc213dd13dbee6462b8de242fa38fa1958e62b373369c701c873e4eaf3468172ff876154954986aaa8d1b523ed980901e79546598e94cb3ec33e056bc6a26df262394c9974d1391009f1ae88a56fdd9bb690a0bb7f51c09cfa0d4675f7e08d2b577ab8a2f4462f18787113707682cffb4d0d11a6d5bb985568df4c8d5ace036f70f9f61295b86a2f63ac343ed303243c' \
--header 'Content-Type: application/octet-stream' \
--data '@/Users/abhinandankelgereramesh/Documents/payana-github/TravelFont/image.jpg'
"""

url = payana_signed_url

image_path = os.path.join(bigtable_constants.travelfont_home, "image.jpg")

with open(image_path, "rb") as f:
    im_bytes = f.read()

im_b64 = base64.b64encode(im_bytes).decode("utf8")

payload = json.dumps({"image": im_b64})

headers = {'Content-Type': 'application/octet-stream'}

# response = requests.put(
#     url, data={'upload': open(image_path, 'rb')})

# response = requests.put(url, headers=headers, files={
#                          'image': open(image_path, 'rb')})

response = requests.put(url, headers=headers, data=payload)

print("Profile image upload status: " +
      str(response.status_code == 200))

# Get Signed URL for download
"""
curl --location --request GET 'http://localhost:8888/entity/signed_url/download' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one'
"""

url = "http://localhost:8888/entity/signed_url/download/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.get(url, headers=headers)

print("Profile signed download URL GET status: " +
      str(response.status_code == 200))

payana_signed_download_url = response.json()

print("Profile signed download URL GET status: " +
      str(response is not None or len(payana_signed_download_url) > 0))

# image download using the signed URL
"""
curl --location 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230911%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230911T061818Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=05c8395f1b0aa985508f0902efb52b0c1820df95d79b62260a851ee1052a11f1f6af378735c17bb63378cbb7eb677b1b9fbb969273d5b45e9e7dca611348d6dc648204919b1c12585b285e0252372d05e9f8189951ebb410e180c672bf446b9a88b2195d3b91809d97316a9e901618ba1b31df1a5f1b42343668653d6a87a7e253f3e28ce1ce4be2b328a8041824dc9451add8c0536ce39df38b7fd1f8548ed7f9f79961ca8af390fb0f42ea28543865e3d97c4a070e7ce986e3a42c81c3bc8f357bb2a94dd7c85d8f7145c34b30222513d1e6a48e502ab5eb1eed3cbacbddc3af2b4dea8eaca6e9f9a8663129e3c1f1756f12bf2fcf8f0a88c073c17377c5f7'
"""

url = payana_signed_download_url

response = requests.get(url)

print("Profile image download check: " +
      str(response.status_code == 200))

payana_image = response.content

payana_gcs_image_download_path = os.path.join(
    bigtable_constants.travelfont_home, "payana_curl_image_response.jpg")

with open(payana_gcs_image_download_path, 'wb') as f:
    f.write(payana_image)

# Get Resumable Upload Signed URL
"""
curl --location --request GET 'http://localhost:8888/entity/signed_url/upload/resumable' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one'
"""

url = "http://localhost:8888/entity/signed_url/upload/resumable/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.get(url, headers=headers)

print("Profile signed resumable upload URL GET status: " +
      str(response.status_code == 200))

payana_resumable_signed_url = response.json()

print("Profile signed resumable upload URL GET status: " +
      str(response is not None or len(payana_signed_url) > 0))

# image upload using the resumable signed URL initial POST
"""
curl --location --request POST 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230911%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230911T044813Z&X-Goog-Expires=900&X-Goog-SignedHeaders=content-type%3Bhost%3Bx-goog-resumable&X-Goog-Signature=3d0d17dae967227b37e8df052ecaff29b65846c70b892347d1e0ac117f60551cf54230b545af411395e1e89fa6a4618090f942c36a608d7ffcc09812e898562f3b41ff495e4bd97e1e9e8adb2e6a4ede106ec3c817f455e4163777c36a2b36fb011988f4bc4765b37c8afaf68f568e509062fad2b6058e0a7866d3906f024c92cfe27fad560025f5358d13853ab79e9b578e68abb35d384427a46cbac49b6b7419ffb932ab964572ae06bb452716f2193fdb1c51db1e1c3d1749fceb86ce554a8af5c416ff207bf175e045ecf7c28543eaa18aed2ec23122691e4dc13d06d690ec2bb2018f00134e8f7f88d88aedacd595fcc9e2a0c2cf1c8fc97ab4bfe54c4c' \
--header 'Content-Type: application/octet-stream' \
--header 'x-goog-resumable: start'
"""

url = str(payana_resumable_signed_url)

image_path = os.path.join(bigtable_constants.travelfont_home, "image.jpg")

headers = {'Content-Type': 'application/octet-stream',
           'x-goog-resumable': 'start'}

response = requests.post(url, headers=headers)

print("Profile image resumable upload signed URL POST initial status: " +
      str(response.status_code == 201))

payana_resumable_signed_url = response.headers['Location']

# image upload using the resumable signed URL PUT
"""
curl --location --request PUT 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230911%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230911T044813Z&X-Goog-Expires=900&X-Goog-SignedHeaders=content-type%3Bhost%3Bx-goog-resumable&X-Goog-Signature=3d0d17dae967227b37e8df052ecaff29b65846c70b892347d1e0ac117f60551cf54230b545af411395e1e89fa6a4618090f942c36a608d7ffcc09812e898562f3b41ff495e4bd97e1e9e8adb2e6a4ede106ec3c817f455e4163777c36a2b36fb011988f4bc4765b37c8afaf68f568e509062fad2b6058e0a7866d3906f024c92cfe27fad560025f5358d13853ab79e9b578e68abb35d384427a46cbac49b6b7419ffb932ab964572ae06bb452716f2193fdb1c51db1e1c3d1749fceb86ce554a8af5c416ff207bf175e045ecf7c28543eaa18aed2ec23122691e4dc13d06d690ec2bb2018f00134e8f7f88d88aedacd595fcc9e2a0c2cf1c8fc97ab4bfe54c4c&upload_id=ADPycdvLN6WvT4s2hj6ONIJXbOqpaWZraEsqHXH4XPAiZsAN7_7V7EbOTS4woPq_MmbkOR_4Dj-zqkQ6s2YWgnbtU3zn4Bb3yPbJ' \
--header 'Content-Length: 4081428' \
--header 'Content-Type: image/jpeg' \
--data '@/Users/abhinandankelgereramesh/Documents/payana-github/TravelFont/image.jpg'
"""

url = payana_resumable_signed_url

image_path = os.path.join(bigtable_constants.travelfont_home, "image.jpg")

headers = {'Content-Type': 'image/jpeg', 'Content-Length': '4081428'}

with open(image_path, "rb") as f:
    im_bytes = f.read()

im_b64 = base64.b64encode(im_bytes).decode("utf8")

payload = json.dumps({"image": im_b64})

response = requests.put(url, headers=headers, data=payload)

# response = requests.put(
#     url, data={'upload': open(image_path, 'rb')})

response = requests.put(url, headers=headers, files={
    'image': open(image_path, 'rb')})

print("Profile image resumable upload signed URL PUT status: " +
      str(response.status_code == 200))

# image upload using the resumable signed URL PUT status
"""
curl --location --request PUT 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230911%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230911T044813Z&X-Goog-Expires=900&X-Goog-SignedHeaders=content-type%3Bhost%3Bx-goog-resumable&X-Goog-Signature=3d0d17dae967227b37e8df052ecaff29b65846c70b892347d1e0ac117f60551cf54230b545af411395e1e89fa6a4618090f942c36a608d7ffcc09812e898562f3b41ff495e4bd97e1e9e8adb2e6a4ede106ec3c817f455e4163777c36a2b36fb011988f4bc4765b37c8afaf68f568e509062fad2b6058e0a7866d3906f024c92cfe27fad560025f5358d13853ab79e9b578e68abb35d384427a46cbac49b6b7419ffb932ab964572ae06bb452716f2193fdb1c51db1e1c3d1749fceb86ce554a8af5c416ff207bf175e045ecf7c28543eaa18aed2ec23122691e4dc13d06d690ec2bb2018f00134e8f7f88d88aedacd595fcc9e2a0c2cf1c8fc97ab4bfe54c4c&upload_id=ADPycdvLN6WvT4s2hj6ONIJXbOqpaWZraEsqHXH4XPAiZsAN7_7V7EbOTS4woPq_MmbkOR_4Dj-zqkQ6s2YWgnbtU3zn4Bb3yPbJ' \
--header 'Content-Type: application/json' \
--header 'data-binary: /Users/abhinandankelgereramesh/Documents/payana-github/TravelFont/image.jpg' \
--header 'Content-Length: 0' \
--header 'Content-Range: bytes */*'
"""

url = payana_resumable_signed_url

image_path = os.path.join(bigtable_constants.travelfont_home, "image.jpg")

headers = {'Content-Type': 'application/json',
           'Content-Range': 'bytes */*', 'Content-Length': '0'}

response = requests.put(url, headers=headers)

print("Profile image resumable upload signed URL PUT status check: " +
      str(response.status_code == 200))

# Get Signed URL for download
"""
curl --location --request GET 'http://localhost:8888/entity/signed_url/download' \
--header 'Content-Type: application/json' \
--header 'profile_id: 123456789' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one'
"""

url = "http://localhost:8888/entity/signed_url/download/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.get(url, headers=headers)

print("Profile signed download URL GET status: " +
      str(response.status_code == 200))

payana_signed_download_url = response.json()

print("Profile signed download URL GET status: " +
      str(response is not None or len(payana_signed_download_url) > 0))

# image download using the resumable signed URL
"""
curl --location 'https://storage.googleapis.com/payana_profile_pictures/profile_picture_one?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=payana-project%40project-payana-395305.iam.gserviceaccount.com%2F20230911%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230911T061818Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=05c8395f1b0aa985508f0902efb52b0c1820df95d79b62260a851ee1052a11f1f6af378735c17bb63378cbb7eb677b1b9fbb969273d5b45e9e7dca611348d6dc648204919b1c12585b285e0252372d05e9f8189951ebb410e180c672bf446b9a88b2195d3b91809d97316a9e901618ba1b31df1a5f1b42343668653d6a87a7e253f3e28ce1ce4be2b328a8041824dc9451add8c0536ce39df38b7fd1f8548ed7f9f79961ca8af390fb0f42ea28543865e3d97c4a070e7ce986e3a42c81c3bc8f357bb2a94dd7c85d8f7145c34b30222513d1e6a48e502ab5eb1eed3cbacbddc3af2b4dea8eaca6e9f9a8663129e3c1f1756f12bf2fcf8f0a88c073c17377c5f7'
"""

url = payana_signed_download_url

response = requests.get(url)

print("Profile image download check resumable URL: " +
      str(response.status_code == 200))

payana_image = response.content

payana_gcs_image_download_path = os.path.join(
    bigtable_constants.travelfont_home, "payana_curl_image_response_resumable.jpg")

with open(payana_gcs_image_download_path, 'wb') as f:
    f.write(payana_image)

# metadata update POST
"""
curl --location 'http://localhost:8888/entity/gcs/object/metadata/' \
--header 'Content-Type: application/json' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one' \
--data '{
    "location": "Seattle",
    "payana_object_id": "123467QWERTY123467QWERTY123467QWERTY",
    "author_name": "abkr"
}'
"""

metadata_obj = {
    "location": "Seattle",
    "payana_object_id": "123467QWERTY123467QWERTY123467QWERTY",
    "author_name": "abkr"
}

url = "http://localhost:8888/entity/gcs/object/metadata/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.post(url, data=json.dumps(metadata_obj), headers=headers)

print("Metadata update status: " +
      str(response.status_code == 201))

# metadata GET
"""
curl --location 'http://localhost:8888/entity/gcs/object/metadata/' \
--header 'Content-Type: application/json' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one' 
"""

url = "http://localhost:8888/entity/gcs/object/metadata/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.get(url, headers=headers)

print("Metadata read status: " +
      str(response.status_code == 200))

metadata_content = response.json()

print("Metadata GET status: " +
      str(metadata_content['location'] == metadata_obj['location']))

# CORS update POST
"""
curl --location 'http://localhost:8888/entity/gcs/object/cors/' \
--header 'Content-Type: application/json' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--data '[
    {
        "origin": [
            "*"
        ],
        "responseHeader": [
            "Content-Type",
            "x-goog-resumable"
        ],
        "method": [
            "PUT",
            "POST",
            "GET",
            "DELETE"
        ],
        "maxAgeSeconds": 3600
    }
]'
"""

cors_obj = [
    {
        "origin": [
            "*"
        ],
        "responseHeader": [
            "Content-Type",
            "x-goog-resumable"
        ],
        "method": [
            "PUT",
            "POST",
            "GET",
            "DELETE"
        ],
        "maxAgeSeconds": 3600
    }
]

url = "http://localhost:8888/entity/gcs/object/cors/"

headers = {'Content-Type': 'application/json',
           'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name}

response = requests.post(url, data=json.dumps(cors_obj), headers=headers)

print("Metadata CORS update status: " +
      str(response.status_code == 201))

# metadata GET
"""
curl --location 'http://localhost:8888/entity/gcs/object/cors/' \
--header 'Content-Type: application/json' \
--header 'payana_storage_bucket: payana_profile_pictures' 
"""

url = "http://localhost:8888/entity/gcs/object/cors/"

headers = {'Content-Type': 'application/json',
           'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name}

response = requests.get(url, headers=headers)

print("Metadata CORS read status: " +
      str(response.status_code == 200))

metadata_cors_content = response.json()

print("Metadata CORS GET status: " +
      str(metadata_cors_content["payana_cors_metadata"][0]["origin"][0] == cors_obj[0]["origin"][0]))

# Delete object
"""
curl --location --request DELETE 'http://localhost:8888/entity/gcs/object/' \
--header 'Content-Type: application/json' \
--header 'payana_storage_bucket: payana_profile_pictures' \
--header 'payana_storage_object: profile_picture_one'
"""

url = "http://localhost:8888/entity/gcs/object/"

headers = {'Content-Type': 'application/json', 'payana_storage_bucket': gcs_payana_profile_pictures_bucket_name,
           'payana_storage_object': profile_picture_bucket_name}

response = requests.delete(url, headers=headers)

print("Payana excursion object row delete status: " +
      str(response.status_code == 200))


payana_cloud_storage_cleanup_status = payana_cloud_storage_cleanup(
    bigtable_constants.gcs_client_config_path)

print("Payana Cloud Storage Cleanup Status: " +
      str(payana_cloud_storage_cleanup_status))
