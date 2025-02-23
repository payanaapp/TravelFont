#!/usr/bin/env python

"""Defines BigTable constants
"""

from google.cloud.bigtable import enums

from dotenv import load_dotenv
import os

load_dotenv()
travelfont_home = os.environ.get("travelfont_home")


# client_config.yaml constants
bigtable_client_config_path = os.path.join(
    travelfont_home, "payana/payana_bl/bigtable_utils/config/client_config.yaml")
gcs_client_config_path = os.path.join(
    travelfont_home, "payana/payana_bl/cloud_storage_utils/config/gcs_bucket_schema.json")
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
bigtable_schema_config_file = os.path.join(
    travelfont_home, "payana/payana_bl/bigtable_utils/config/bigtable_schema.json")
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
payana_entity_to_comments_table = "payana_entity_to_comments_table"
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
payana_city_to_influencers_table = "payana_city_to_influencers_table"
payana_state_to_influencers_table = "payana_state_to_influencers_table"
payana_country_to_influencers_table = "payana_country_to_influencers_table"
payana_excursion_checkin_permission_table = "payana_excursion_checkin_permission_table"
payana_global_influencer_feed_search_itinerary_cache_table = "payana_global_influencer_feed_search_cache_table"
payana_personal_influencer_feed_search_itinerary_cache_table = "payana_personal_influencer_feed_search_cache_table"
payana_personal_travel_buddy_feed_search_itinerary_cache_table = "payana_travel_buddy_feed_search_cache_table"
payana_profile_to_search_places_activities_table = "payana_profile_to_search_places_activities_table"
payana_city_autocomplete_table = "payana_city_autocomplete_table"
payana_users_autocomplete_table = "payana_users_autocomplete_table"
payana_mail_sign_up_notification_table = "payana_mail_sign_up_notification_table"
payana_mail_share_itinerary_notification_table = "payana_mail_share_itinerary_notification_table"
payana_profile_auth_table = "payana_profile_auth_table"
payana_activity_guide_thumbnail_table = "payana_activity_guide_thumbnail_table"

# payana gcs bucket names
payana_gcs_itinerary_pictures = "payana_itinerary_pictures"
payana_gcs_profile_pictures = "payana_profile_pictures"

# payana_auth_profile_table
payana_auth_information = "auth_information"
payana_auth_mail_id = "mail_id"
payana_auth_profile_name = "profile_name"
payana_auth_profile_picture_id = "profile_picture_id"
payana_auth_profile_id = "profile_id"

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
payana_profile_table_doj = "doj"  # date of joining
payana_profile_table_date_of_birth = "date_of_birth"
payana_profile_table_top_activities_tracker_rating = "top_activities_tracker_rating"
payana_profile_favorite_places_preference = "favorite_places_preference"
payana_profile_favorite_activities_preference = "favorite_activities_preference"
payana_profile_table_thumbnail_travel_buddies = "thumbnail_travel_buddies"
payana_profile_table_profile_pictures = "payana_profile_pictures"
payana_profile_table_cover_pictures = "payana_cover_pictures"
payana_profile_table_payment_id = "payana_payment_id"
payana_profile_table_payment_type = "payana_payment_type"

# payana_activity_guide_thumbnail_table
payana_activity_thumbnail = "payana_activity_thumbnail"
payana_activity_thumbnail_city = "city"

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

# payana entity comments table
payana_entity_to_comments_table_comment_id_list = "payana_comment_id_list"

# GCS photo object constants
payana_photo_id = "photo_id"

# Payana itinerary table constants
payana_itinerary_column_family_excursion_id_list = "excursion_id_list"
payana_itinerary_column_family_participants_list = "participants_list"
payana_itinerary_column_family_description = "description"
payana_itinerary_column_family_visit_timestamp = "visit_timestamp"
payana_itinerary_column_family_itinerary_owner_profile_id = "itinerary_owner_profile_id"
payana_itinerary_column_family_last_updated_timestamp = "last_updated_timestamp"
payana_itinerary_id = "itinerary_id"
payana_itinerary_metadata = "itinerary_metadata"
payana_itinerary_activities_list = "activities_list"
payana_itinerary_place_id = "place_id"
payana_itinerary_place_name = "place_name"
payana_itinerary_city = "city"
payana_itinerary_state = "state"
payana_itinerary_country = "country"
payana_itinerary_last_updated_timestamp = "last_updated_timestamp"
payana_itinerary_column_family_cities_list = "cities_list"

# Payana excursion table constants
payana_excursion_column_family_checkin_id_list = "checkin_id_list"
payana_excursion_column_family_cities_checkin_id_list = "cities_checkin_id_list"
payana_excursion_column_family_image_id_list = "image_id_list"
payana_excursion_image_id_signed_url_mapping = "image_id_signed_url_list"
payana_excursion_column_family_participants_list = "participants_list"
payana_excursion_column_family_description = "description"
payana_excursion_column_family_create_timestamp = "create_timestamp"
payana_excursion_column_family_last_updated_timestamp = "last_updated_timestamp"
payana_excursion_column_family_excursion_owner_profile_id = "excursion_owner_profile_id"
payana_excursion_id = "excursion_id"
payana_excursion_name = "excursion_name"
payana_excursion_metadata = "excursion_metadata"
payana_excursion_transport_mode = "transport_mode"
payana_excursion_place_name = "place_name"
payana_excursion_place_id = "place_id"
payana_excursion_activities_list = "activities_list"
# The above code appears to be a Python variable declaration. It is creating a variable named
# "payana_excursion_itinerary_id" and assigning it a value or placeholder. The triple hash symbols "
payana_excursion_itinerary_id = "itinerary_id"
payana_excursion_itinerary_name = "itinerary_name"
payana_excursion_city = "city"
payana_excursion_state = "state"
payana_excursion_country = "country"
payana_excursion_activity_guide = "activity_guide"
payana_excursion_itinerary_position = "excursion_object_position_itinerary"
payana_excursion_clone_parent_id = "excursion_clone_parent_id"
payana_excursion_checkin_objects = "payana_excursion_checkin_objects"

# Payana check in table constants
payana_checkin_column_family_image_id_list = "image_id_list"
payana_checkin_column_family_participants_list = "participants_list"
payana_checkin_column_family_description = "description"
payana_checkin_column_family_create_timestamp = "create_timestamp"
payana_checkin_column_family_last_updated_timestamp = "last_updated_timestamp"
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
payana_checkin_city = "city"
payana_checkin_state = "state"
payana_checkin_country = "country"
payana_checkin_excursion_position = "checkin_object_position_excursion"

# Payana likes table constants
payana_likes_table_column_family = "payana_likes"
payana_likes_table_like_object_id_qualifier = "like_object_id"
payana_likes_table_metadata_column_family = "likes_metadata"
payana_likes_table_entity_id = "entity_id"

# Payana travel buddy table constants
payana_travel_buddy_table_column_family_travel_buddy_list = "payana_travel_buddy_list"
payana_travel_buddy_table_column_family_travel_buddy_list_timestamp = "payana_travel_buddy_list_timestamp"
payana_travel_buddy_table_column_family_favorite_travel_buddy_list = "payana_favorite_buddy_list"
payana_travel_buddy_table_column_family_top_travel_buddy_list = "payana_top_buddy_list"
payana_travel_buddy_table_column_family_global_influencers_travel_buddy_list = "payana_global_influencers_travel_buddy_list"
payana_travel_buddy_table_column_family_pending_sent_requests_travel_buddy_list = "payana_pending_sent_requests_travel_buddy_list"
payana_travel_buddy_table_column_family_pending_received_requests_travel_buddy_list = "payana_pending_received_requests_travel_buddy_list"
payana_travel_buddy_table_column_family_profile_id = "profile_id"
payana_travel_buddy_table_column_family_travel_buddy_profile_id = "travel_buddy_profile_id"
payana_travel_buddy_table_column_family_global_influencer = "global_influencer"
payana_travel_buddy_table_column_family_favorite = "favorite"
payana_travel_buddy_table_column_family_sent_pending_request = "sent_pending_request"
payana_travel_buddy_table_column_family_received_pending_request = "received_pending_request"
payana_travel_buddy_table_friend_id = "friend_id"

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
payana_activity_column_family = ["generic", "hiking", "aerial_activities", "bar_hopping", "city_culture", "clubbing", "coffee_bar", "fashion_trips", "food_trips", "instagrammable_locations",
                                 "island_beaches", "kid_friendly", "land_adventures", "live_events", "road_trips", "romantic", "rooftop_bars", "spring_break", "staycation", "water_activities", "weekend_getaway"]

# Payana personal place ID itinerary table constants
payana_personal_place_id_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_place_id_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_place_id_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_personal_place_id_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_personal_place_id_itinerary_table_activities = "activities"
payana_personal_place_id_itinerary_table_rating_column_family_id = "rating"
payana_personal_place_id_itinerary_table_timestamp_column_family_id = "timestamp"

# Payana personal city itinerary table constants
payana_personal_city_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_city_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_city_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_personal_city_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_personal_city_itinerary_table_activities = "activities"
payana_personal_city_itinerary_table_rating_column_family_id = "rating"
payana_personal_city_itinerary_table_timestamp_column_family_id = "timestamp"

# Payana personal state itinerary table constants
payana_personal_state_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_state_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_state_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_personal_state_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_personal_state_itinerary_table_activities = "activities"
payana_personal_city_itinerary_table_activities = "activities"
payana_personal_state_itinerary_table_rating_column_family_id = "rating"
payana_personal_state_itinerary_table_timestamp_column_family_id = "timestamp"

# Payana personal country itinerary table constants
payana_personal_country_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_personal_country_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_personal_country_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_personal_country_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_personal_country_itinerary_table_activities = "activities"
payana_personal_city_itinerary_table_activities = "activities"
payana_personal_country_itinerary_table_rating_column_family_id = "rating"
payana_personal_country_itinerary_table_timestamp_column_family_id = "timestamp"

# Payana table exception
payana_big_table_exception = "Interval Server Error : Unable to reach the database"
payana_big_table_does_not_exist_exception = "BigTable doesn't exist or none instance returned"

# Payana profile page itineraries
payana_profile_page_itinerary_table_saved_itinerary_id_list_quantifier_value = "saved_itinerary_id_list"
payana_profile_page_itinerary_table_profile_id = "profile_id"
payana_profile_page_itinerary_table_saved_excursion_id_list_quantifier_value = "saved_excursion_id_list"
payana_profile_page_itinerary_table_saved_activity_guide_id_list_quantifier_value = "saved_activity_guide_id_list"
payana_profile_page_itinerary_table_created_itinerary_id_list_quantifier_value = "created_itinerary_id_list"
payana_profile_page_itinerary_table_created_excursion_id_list_quantifier_value = "created_excursion_id_list"
payana_profile_page_itinerary_table_created_activity_guide_id_list_quantifier_value = "created_activity_guide_id_list"
payana_profile_page_itinerary_table_saved_itinerary_id_mapping_quantifier_value = "saved_itinerary_id_mapping"
payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value = "saved_excursion_id_mapping"
payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value = "saved_activity_guide_id_mapping"
payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value = "created_itinerary_id_mapping"
payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value = "created_excursion_id_mapping"
payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value = "created_activity_guide_id_mapping"
payana_profile_page_itinerary_table_activities = "activities"

# Payana global place ID itinerary table constants
payana_global_place_id_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_place_id_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_place_id_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_global_place_id_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_global_place_id_itinerary_table_activities = "activities"
payana_global_place_id_itinerary_table_itinerary_id_rating_quantifier_value = "rating"
payana_global_place_id_itinerary_table_itinerary_id_timestamp_quantifier_value = "timestamp"

# Payana global city itinerary table constants
payana_global_city_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_city_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_city_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_global_city_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_global_city_itinerary_table_activities = "activities"
payana_global_city_itinerary_table_itinerary_id_rating_quantifier_value = "rating"
payana_global_city_itinerary_table_itinerary_id_timestamp_quantifier_value = "timestamp"

# Payana global state itinerary table constants
payana_global_state_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_state_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_state_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_global_state_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_global_state_itinerary_table_activities = "activities"
payana_global_state_itinerary_table_itinerary_id_rating_quantifier_value = "rating"
payana_global_state_itinerary_table_itinerary_id_timestamp_quantifier_value = "timestamp"

# Payana global country itinerary table constants
payana_global_country_itinerary_table_itinerary_id_quantifier_value = "itinerary_id"
payana_global_country_itinerary_table_excursion_id_quantifier_value = "excursion_id"
payana_global_country_itinerary_table_activity_guide_id_quantifier_value = "activity_guide_id"
payana_global_country_itinerary_table_checkin_id_quantifier_value = "checkin_id"
payana_global_country_itinerary_table_activities = "activities"
payana_global_country_itinerary_table_itinerary_id_rating_quantifier_value = "rating"
payana_global_country_itinerary_table_itinerary_id_timestamp_quantifier_value = "timestamp"

# Payana profile page travel footprint constants
payana_profile_page_travel_footprint_profile_id = "profile_id"
payana_profile_page_travel_footprint_place_id = "place_id"
payana_profile_page_travel_footprint_excursion_id = "excursion_id"
payana_profile_page_travel_footprint_latitude = "latitude"
payana_profile_page_travel_footprint_longitude = "longitude"
payana_profile_page_travel_footprint_column_family = "travel_footprint"
payana_profile_travel_footprint_table = "payana_travel_footprint_table"
payana_profile_travel_footprint_obj_list = "travelfont_obj_list"

# Payana city to influencers constants
payana_city_to_influencers_table_global_influencers_column_family = "city_global_influencers"

# Payana state to influencers constants
payana_state_to_influencers_table_global_influencers_column_family = "state_global_influencers"

# Payana country to influencers constants
payana_country_to_influencers_table_global_influencers_column_family = "country_global_influencers"

# payana_excursion_checkin_permission_table constants
payana_excursion_checkin_permission_participants_column_family = "participants_list"
payana_excursion_checkin_permission_edit_participants_column_family = "edit_participants_list"
payana_excursion_checkin_permission_table_admin_column_family = "admin"

# payana_feed_search_itinerary_cache_table constants
payana_feed_search_itinerary_cache_excursion_id_column_family = "excursion_id"
payana_feed_search_itinerary_cache_activity_guide_id_column_family = "activity_guide_id"
payana_feed_search_itinerary_cache_rating_column_family = "rating"
payana_feed_search_itinerary_cache_timestamp_column_family = "timestamp"
payana_feed_search_itinerary_cache_profile_id = "profile_id"

# payana_profile_to_search_cities_activities_table constants
payana_profile_to_search_places_activities_searched_cities_activities = "searched_cities_activities"
payana_profile_to_search_places_activities_searched_state_activities = "searched_state_activities"
payana_profile_to_search_places_activities_searched_place_id_activities = "searched_place_id_activities"
payana_profile_to_search_places_activities_searched_country_activities = "searched_country_activities"

# payana_users_autocomplete_table constants
payana_users_autocomplete_column_family = "payana_autocomplete_users_list"

# payana_city_autocomplete_table constants
payana_city_autocomplete_column_family = "payana_autocomplete_cities_list"
payana_city_autocomplete_row_key = "city"
payana_city_autocomplete_personal_travel_buddies = "personal_travel_buddies"
payana_city_autocomplete_city_travel_buddies = "city_travel_buddies"

# payana_mail_sign_up_notification
payana_sign_up_mail_id_list_column_family = "sign_up_mail_id_list"
payana_sign_up_mail_id_list_profile_id = "profile_id"
payana_sign_up_mail_id_list_profile_name = "profile_name"
payana_share_itinerary_id_mail_id_list_column_family = "itinerary_id",
payana_share_itinerary_name_mail_id_list_column_family = "itinerary_name"
