#!/usr/bin/env python

"""Defines BigTable constants
"""

from google.cloud.bigtable import enums

from dotenv import load_dotenv
import os

load_dotenv()
travelfont_home = os.environ.get("travelfont_home")

# client_config.yaml constants
bigtable_client_config_path = os.path.join(travelfont_home, "payana_bl/bigtable_utils/config/client_config.yaml")
bigtable_instance_id = "instance_id"
bigtable_project_id = "project_id"
bigtable_cluster_id = "cluster_id"
bigtable_location_id = "location_id"
bigtable_serve_nodes = "serve_nodes"
bigtable_production_flag = "production_flag"
bigtable_labels = "labels"
bigtable_prod_label = "prod-label"
bigtable_storage_type = enums.StorageType.SSD
bigtable_production = enums.Instance.Type.PRODUCTION

# bigtable table creation schema constants
bigtable_schema_config_file = os.path.join(travelfont_home, "payana/payana_bl/bigtable_utils/config/bigtable_schema.json")
bigtable_schema_column_family_id = "column_family_id"
bigtable_schema_max_versions = "max_versions"
bigtable_schema_description = "description"
bigtable_schema_purpose = "purpose"

# bigtable table names for payana
payana_profile_table = "payana_profile_table"
payana_itinerary_table = "payana_itinerary_table"
payana_friends_list_table = "payana_friends_list_table"
payana_place_search_table = "payana_place_search_table"
payana_global_places_search_activity_table = "payana_global_places_search_activity_table"
payana_friends_places_search_activity_table = "payana_friends_places_search_activity_table"
payana_saved_itinerary_table = "payana_saved_itinerary_table"

# payana_profile_table_field_names
payana_profile_table_personal_info_column_family = "personal_information"
payana_profile_table_profile_name = "profile_name"
payana_profile_table_user_name = "user_name"
payana_profile_table_blog_url = "blog_url"
payana_profile_table_profile_description = "profile_description"
payana_profile_table_profile_id = "profile_id"
payana_profile_table_email = "email"
payana_profile_table_phone = "phone"
payana_profile_table_private_account = "private_account"
payana_profile_table_gender = "gender"
payana_profile_table_date_of_birth = "date_of_birth"
