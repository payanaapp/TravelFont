#!/usr/bin/env python

"""Defines BigTable constants
"""

from google.cloud.bigtable import enums

from dotenv import load_dotenv
import os

load_dotenv()
travelfont_home = os.environ.get("travelfont_home")


# client_config.yaml constants
bigtable_client_config_path = os.path.join(travelfont_home, "payana/payana_bl/bigtable_utils/config/client_config.yaml")
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
payana_excursion_table = "payana_excursion_table"
payana_checkin_table = "payana_checkin_table"
payana_travel_buddy_list_table = "payana_travel_buddy_list_table"
payana_likes_table = "payana_likes_table"
payana_comments_table = "payana_comments_table"
payana_place_metadata_table = "payana_place_metadata_table"
payana_place_state_table = "payana_place_state_table"
payana_place_country_table = "payana_place_country_table"
payana_neighboring_cities_table = "payana_neighboring_cities_table"
payana_personal_place_id_itinerary_table = "payana_personal_place_id_itinerary_table"
payana_personal_city_itinerary_table = "payana_personal_city_itinerary_table"
payana_personal_state_itinerary_table = "payana_personal_state_itinerary_table"
payana_personal_country_itinerary_table = "payana_personal_country_itinerary_table"
payana_profile_page_itinerary_table = "payana_profile_page_itinerary_table"
payana_global_place_id_itinerary_table = "payana_global_place_id_itinerary_table"
payana_global_city_itinerary_table = "payana_global_city_itinerary_table"
payana_global_state_itinerary_table = "payana_global_state_itinerary_table"
payana_global_country_itinerary_table = "payana_global_country_itinerary_table"

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
payana_profile_table_top_activities = "top_activities"

# payana_comments_table_field_names
payana_comments_table_comments_family_id = "payana_comments"
payana_comments_table_timestamp = "comment_timestamp"
payana_comments_table_comment_id = "comment_id"
payana_comments_table_profile_id = "profile_id"
payana_comments_table_profile_name = "profile_name"
payana_comments_table_comment = "comment"
payana_comments_table_likes = "likes"
payana_comments_table_likes_count = "likes_count"
payana_comments_table_entity_id = "entity_id"

# GCS photo object constants
payana_photo_id = "photo_id"

# Payana itinerary table constants
payana_itinerary_column_family_excursion_id_list = "excursion_id_list"
payana_itinerary_column_family_participants_list = "participants_list"
payana_itinerary_column_family_description = "description"
payana_itinerary_column_family_visit_timestamp = "visit_timestamp"
payana_itinerary_column_family_itinerary_owner_profile_id = "itinerary_owner_profile_id"
payana_itinerary_id = "itinerary_id"
payana_itinerary_metadata = "itinerary_metadata"
payana_itinerary_activities_list = "activities_list"
payana_itinerary_place_id = "place_id"
payana_itinerary_place_name = "place_name"

# Payana excursion table constants
payana_excursion_column_family_checkin_id_list = "checkin_id_list"
payana_excursion_column_family_participants_list = "participants_list"
payana_excursion_column_family_description = "description"
payana_excursion_column_family_visit_timestamp = "visit_timestamp"
payana_excursion_column_family_excursion_owner_profile_id = "excursion_owner_profile_id"
payana_excursion_id = "excursion_id"
payana_excursion_metadata = "excursion_metadata"
payana_excursion_transport_mode = "transport_mode"
payana_excursion_place_name = "place_name"
payana_excursion_place_id = "place_id"
payana_excursion_activities_list = "activities_list"
payana_excursion_itinerary_id = "itinerary_id"

# Payana check in table constants
payana_checkin_column_family_image_id_list = "image_id_list"
payana_checkin_column_family_participants_list = "participants_list"
payana_checkin_column_family_description = "description"
payana_checkin_column_family_visit_timestamp = "visit_timestamp"
payana_checkin_column_family_checkin_owner_profile_id = "checkin_owner_profile_id"
payana_checkin_id = "checkin_id"
payana_checkin_metadata = "checkin_metadata"
payana_checkin_transport_mode = "transport_mode"
payana_checkin_place_name = "place_name"
payana_checkin_place_id = "place_id"
payana_checkin_activities_list = "activities_list"
payana_checkin_itinerary_id = "itinerary_id"
payana_checkin_excursion_id = "excursion_id"
payana_checkin_instagram_metadata = "instagram_metadata"
payana_checkin_airbnb_metadata = "airbnb_metadata"
payana_checkin_instagram_embed_url = "instagram_embed_url"
payana_checkin_instagram_post_id = "instagram_post_id"
payana_checkin_airbnb_embed_url = "airbnb_embed_url"
payana_checkin_airbnb_post_id = "airbnb_post_id"

# Payana likes table constants
payana_likes_table_column_family = "payana_likes"
payana_likes_table_like_object_id_qualifier = "like_object_id"
payana_likes_table_metadata_column_family = "likes_metadata"

# Payana travel buddy table constants
payana_travel_buddy_table_column_family = "payana_travel_buddy_list"

# Payana Metadata Table constants
payana_quantifier_place_id = "place_id"
payana_quantifier_city = "city"
payana_quantifier_state = "state"
payana_quantifier_country = "country"
payana_quantifier_zipcode = "zipcode"
payana_column_family_place_metadata = "place_metadata"

# Payana State table constants
payana_state_table_quantifier_city = "city"
payana_state_table_column_family_city_list = "city_list"

# Payana Country table constants
payana_country_table_quantifier_city = "city"
payana_country_table_column_family_city_list = "city_list"

# Payana Neighboring Table constants
payana_neighboring_cities_column_family = "neighboring_city_list"

# Payana activity constants
payana_generic_activity_column_family = "generic"
payana_activity_column_family = ["hiking", "romantic", "exotic"]

# Payana personal place ID itinerary table constants
payana_personal_place_id_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_place_id_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_place_id_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_personal_place_id_itinerary_table_activities = "activities"

# Payana personal city itinerary table constants
payana_personal_city_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_city_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_city_itinerary_table_checkin_id_quantifier_value = "checkin_id"

# Payana personal state itinerary table constants
payana_personal_state_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_state_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_state_itinerary_table_checkin_id_quantifier_value = "checkin_id"

# Payana personal country itinerary table constants
payana_personal_country_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_country_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_country_itinerary_table_checkin_id_quantifier_value = "checkin_id"

# Payana table exception
payana_big_table_exception = "Interval Server Error : Unable to reach the database"
payana_big_table_does_not_exist_exception = "BigTable doesn't exist or none instance returned"

# Payana profile page itineraries
payana_profile_page_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_profile_page_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_profile_page_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_profile_page_itinerary_table_activities = "activities"

# Payana global place ID itinerary table constants
payana_global_place_id_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_place_id_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_place_id_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_global_place_id_itinerary_table_activities = "activities"

# Payana global city itinerary table constants
payana_global_city_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_city_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_city_itinerary_table_checkin_id_quantifier_value = "checkin_id"

# Payana global state itinerary table constants
payana_global_state_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_state_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_state_itinerary_table_checkin_id_quantifier_value = "checkin_id"

# Payana global country itinerary table constants
payana_global_country_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_country_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_country_itinerary_table_checkin_id_quantifier_value = "checkin_id"