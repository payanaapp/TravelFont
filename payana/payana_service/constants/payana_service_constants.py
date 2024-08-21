#!/usr/bin/env python

"""Defines Payana service constants
"""

# Payana service constants
status = "status"
message = "message"
status_code = "statusCode"

#Payana generic constants
payana_profile_id_header = "profile_id"
payana_mail_id_header = "mail_id"
payana_empty_row_read_exception = "Empty result. Check if it's a valid entity key."
payana_activity_id_header = "activity_id"

# Payana GKE Readiness probe controller constants
payana_readiness_probe_success_message = "Payana Service Layer Ready!"

# Payana GKE Liveness probe controller constants
payana_liveness_probe_success_message = "Payana Service Layer Live!"

#Payana Profile Table Controller constants
payana_profile_table_write_success_message_post = "Profile successfully created!"
payana_profile_table_write_success_message_put = "Profile successfully updated!"
payana_profile_table_delete_success_message = "Profile successfully deleted!"
payana_profile_table_create_failure_message_post = "Failed to create the profile"
payana_profile_table_delete_failure_message = "Failed to delete the profile"
payana_profile_table_write_failure_message_post = "Failed to update the profile"
payana_profile_table_objects_delete_failure_message = "Failed to delete the profile objects"
payana_profile_table_objects_delete_success_message = "Profile content successfully deleted!"
payana_missing_profile_object = "Missing profile info object in the request body"


#Payana Activity Guide Thumbnail Controller constants
payana_activity_guide_thumbnail_table_write_success_message_post = "Activity guide thumbnail successfully created!"
payana_activity_guide_thumbnail_table_write_success_message_put = "Activity guide thumbnail successfully updated!"
payana_activity_guide_thumbnail_table_delete_success_message = "Activity guide thumbnail successfully deleted!"
payana_activity_guide_thumbnail_table_create_failure_message_post = "Failed to create the Activity guide thumbnail"
payana_activity_guide_thumbnail_table_delete_failure_message = "Failed to delete the Activity guide thumbnail"
payana_activity_guide_thumbnail_table_write_failure_message_post = "Failed to update the Activity guide thumbnail"
payana_activity_guide_thumbnail_table_objects_delete_failure_message = "Failed to delete the Activity guide thumbnail objects"
payana_activity_guide_thumbnail_table_objects_delete_success_message = "Activity guide thumbnail content successfully deleted!"
payana_activity_guide_thumbnail_profile_object = "Missing Activity guide thumbnail object in the request body"

#Payana Auth Profile Table Controller constants
payana_auth_profile_table_write_success_message_post = "Auth Profile successfully created!"
payana_auth_profile_table_write_success_message_put = "Auth Profile successfully updated!"
payana_auth_profile_table_delete_success_message = "Auth Profile successfully deleted!"
payana_auth_profile_table_create_failure_message_post = "Failed to create the Auth profile"
payana_auth_profile_table_delete_failure_message = "Failed to delete the Auth profile"
payana_auth_profile_table_write_failure_message_post = "Failed to update the Auth profile"
payana_auth_profile_table_objects_delete_failure_message = "Failed to delete the Auth profile objects"
payana_auth_profile_table_objects_delete_success_message = "Auth Profile content successfully deleted!"
payana_auth_missing_profile_object = "Missing Auth profile info object in the request body"

# Payana Travel footprint controller constants
payana_profile_page_travelfont_write_success_message_post = "Travel Footprint successfully created!"
payana_profile_page_travelfont_write_success_message_put = "Travel Footprint successfully updated!"
payana_profile_page_travelfont_delete_success_message = "Travel Footprint successfully deleted!"
payana_profile_page_travelfont_create_failure_message_post = "Failed to create the Travel Footprint"
payana_profile_page_travelfont_delete_failure_message = "Failed to delete the Travel Footprint"
payana_profile_page_travelfont_write_failure_message_post = "Failed to update the Travel Footprint"
payana_profile_page_travelfont_objects_delete_failure_message = "Failed to delete the Travel Footprint objects"
payana_profile_page_travelfont_objects_delete_success_message = "Travel Footprint content successfully deleted!"
payana_missing_profile_page_travelfont_object = "Missing profile page travel footprint object in the request body"

# Payana Likes controller constants
payana_likes_write_success_message_post = "Payana likes object successfully created!"
payana_likes_write_success_message_put = "Payana likes object successfully updated!"
payana_likes_delete_success_message = "Payana likes object successfully deleted!"
payana_likes_create_failure_message_post = "Failed to create the Payana likes object"
payana_likes_delete_failure_message = "Failed to delete the Payana likes object"
payana_likes_write_failure_message_post = "Failed to update the Payana likes object"
payana_likes_objects_delete_failure_message = "Failed to delete the Payana likes object contents"
payana_likes_objects_delete_success_message = "Payana likes object content successfully deleted!"
payana_missing_likes_object = "Missing Payana likes object in the request body"
payana_entity_id_header = "entity_id"

# Payana Tables controller constants
payana_tables_create_success_message = "Payana tables successfully created!"
payana_tables_create_failure_message = "Payana tables failed to create!"
payana_tables_delete_success_message = "Payana tables  successfully deleted!"
payana_tables_delete_failure_message = "Failed to delete the Payana tables"

# Payana signed URL controller constants
payana_signed_url_success_message_get = "Payana Signed URL successfully fetched!"
payana_signed_url_storage_bucket_header = "payana_storage_bucket"
payana_signed_url_storage_object_header = "payana_storage_object"
payana_signed_url_storage_bucket_header_missing_exception = "Payana storage bucket entity header missing"
payana_signed_url_storage_object_header_missing_exception  = "Payana storage object entity header missing"

# Payana GCS object controller constants
payana_gcs_object_success_message_delete = "Payana GCS object successfully deleted!"
payana_gcs_object_failure_message_delete = "Failed to delete Payana GCS object"
payana_gcs_object_metadata_success_message_update = "Payana GCS metadata successfully updated!"
payana_gcs_object_metadata_failure_message_update = "Failed to update Payana GCS metadata"
payana_gcs_object_cors_policy_success_message_update = "Payana GCS object CORS policy successfully updated!"
payana_gcs_object_cors_policy_failure_message_update = "Failed to update Payana GCS object CORS policy"
payana_gcs_object_metadata_success_message_get = "Payana GCS metadata successfully fetched!"
payana_gcs_object_metadata_failure_message_get = "Failed to fetch Payana GCS metadata"
payana_gcs_bucket_header = "payana_storage_bucket"
payana_gcs_object_header = "payana_storage_object"
payana_gcs_object_metadata_header = "payana_storage_object_metadata"
payana_gcs_cors_header = "payana_cors_metadata"
payana_gcs_object_header_missing_exception = "Payana storage object entity header missing"
payana_gcs_bucket_header_missing_exception  = "Payana storage bucket entity header missing"
payana_gcs_metadata_header_missing_exception  = "Payana storage object metadata header missing"
payana_gcs_cors_metadata_missing_exception  = "Payana CORS metadata object missing"

# Payana Travel Buddy controller constants
payana_travel_buddy_write_success_message_post = "Payana travel buddy object successfully created!"
payana_travel_buddy_write_success_message_put = "Payana travel buddy object successfully updated!"
payana_travel_buddy_delete_success_message = "Payana travel buddy object successfully deleted!"
payana_travel_buddy_create_failure_message_post = "Failed to create the Payana travel buddy object"
payana_travel_buddy_delete_failure_message = "Failed to delete the Payana travel buddy object"
payana_travel_buddy_write_failure_message_post = "Failed to update the Payana travel buddy object"
payana_travel_buddy_objects_delete_failure_message = "Failed to delete the Payana travel buddy object contents"
payana_travel_buddy_objects_delete_success_message = "Payana travel buddy object content successfully deleted!"
payana_missing_travel_buddy_object = "Missing Payana travel buddy object in the request body"
payana_missing_travel_buddy_profile_id_header_exception = "Missing Payana travel buddy object header in the request body"
payana_friend_id_header = "friend_id"

# Payana City Influencer controller constants
payana_city_influencers_write_success_message_post = "Payana city influencers object successfully created!"
payana_city_influencers_write_success_message_put = "Payana city influencers object successfully updated!"
payana_city_influencers_delete_success_message = "Payana city influencers object successfully deleted!"
payana_city_influencers_create_failure_message_post = "Failed to create the Payana city influencers object"
payana_city_influencers_delete_failure_message = "Failed to delete the Payana city influencers object"
payana_city_influencers_write_failure_message_post = "Failed to update the Payana city influencers object"
payana_city_influencers_objects_delete_failure_message = "Failed to delete the Payana city influencers object contents"
payana_city_influencers_objects_delete_success_message = "Payana city influencers object content successfully deleted!"
payana_missing_city_influencers_object = "Missing Payana city influencers object in the request body"
payana_city_header = "city"

# Payana country cities controller constants
payana_country_cities_write_success_message_post = "Payana country cities object successfully created!"
payana_country_cities_write_success_message_put = "Payana country cities object successfully updated!"
payana_country_cities_delete_success_message = "Payana country cities object successfully deleted!"
payana_country_cities_create_failure_message_post = "Failed to create the Payana country cities object"
payana_country_cities_delete_failure_message = "Failed to delete the Payana country cities object"
payana_country_cities_write_failure_message_post = "Failed to update the Payana country cities object"
payana_country_cities_objects_delete_failure_message = "Failed to delete the Payana country cities object contents"
payana_country_cities_objects_delete_success_message = "Payana country cities object content successfully deleted!"
payana_missing_country_cities_object = "Missing Payana country cities object in the request body"
payana_country_header = "country"
payana_missing_country_header_exception = "Missing Payana country header in the request body"

# Payana neighboring cities controller constants
payana_neighboring_cities_write_success_message_post = "Payana neighboring cities object successfully created!"
payana_neighboring_cities_write_success_message_put = "Payana neighboring cities object successfully updated!"
payana_neighboring_cities_delete_success_message = "Payana neighboring cities object successfully deleted!"
payana_neighboring_cities_create_failure_message_post = "Failed to create the Payana neighboring cities object"
payana_neighboring_cities_delete_failure_message = "Failed to delete the Payana neighboring cities object"
payana_neighboring_cities_write_failure_message_post = "Failed to update the Payana neighboring cities object"
payana_neighboring_cities_objects_delete_failure_message = "Failed to delete the Payana neighboring cities object contents"
payana_neighboring_cities_objects_delete_success_message = "Payana neighboring cities object content successfully deleted!"
payana_neighboring_cities_missing_object = "Missing Payana neighboring cities object in the request body"
payana_neighboring_city_header = "city"
payana_missing_neighboring_cities_header_exception = "Missing Payana neighboring cities header in the request body"

# Payana autocomplete cities controller constants
payana_autocomplete_cities_write_success_message_post = "Payana autocomplete cities object successfully created!"
payana_autocomplete_cities_write_success_message_put = "Payana autocomplete cities object successfully updated!"
payana_autocomplete_cities_delete_success_message = "Payana autocomplete cities object successfully deleted!"
payana_autocomplete_cities_create_failure_message_post = "Failed to create the Payana autocomplete cities object"
payana_autocomplete_cities_delete_failure_message = "Failed to delete the Payana autocomplete cities object"
payana_autocomplete_cities_write_failure_message_post = "Failed to update the Payana autocomplete cities object"
payana_autocomplete_cities_objects_delete_failure_message = "Failed to delete the Payana autocomplete cities object contents"
payana_autocomplete_cities_objects_delete_success_message = "Payana autocomplete cities object content successfully deleted!"
payana_autocomplete_cities_missing_object = "Missing Payana autocomplete cities object in the request body"
payana_autocomplete_city_header = "city"
payana_missing_autocomplete_cities_header_exception = "Missing Payana autocomplete cities header in the request body"

# Payana mail sign up notification controller constants
payana_mail_id_sign_up_notification_write_success_message_post = "Payana mail id sign up notification successfully sent!"
payana_mail_id_sign_up_notification_write_failure_message_post = "Payana mail id sign up notification failure to send. Please try again."
payana_mail_id_sign_up_notification_profile_id_header = "profile_id"
payana_missing_mail_id_sign_up_notification_header_exception = "Missing Payana mail id sign up notification header in the request body"

# Payana autocomplete users controller constants
payana_autocomplete_users_write_success_message_post = "Payana autocomplete users object successfully created!"
payana_autocomplete_users_write_success_message_put = "Payana autocomplete users object successfully updated!"
payana_autocomplete_users_delete_success_message = "Payana autocomplete users object successfully deleted!"
payana_autocomplete_users_create_failure_message_post = "Failed to create the Payana autocomplete users object"
payana_autocomplete_users_delete_failure_message = "Failed to delete the Payana autocomplete users object"
payana_autocomplete_users_write_failure_message_post = "Failed to update the Payana autocomplete users object"
payana_autocomplete_users_objects_delete_failure_message = "Failed to delete the Payana autocomplete users object contents"
payana_autocomplete_users_objects_delete_success_message = "Payana autocomplete users object content successfully deleted!"
payana_autocomplete_users_missing_object = "Missing Payana autocomplete users object in the request body"
payana_autocomplete_users_header = "user"
payana_missing_autocomplete_users_header_exception = "Missing Payana autocomplete users header in the request body"
payana_autocomplete_header = "autocomplete"

# Payana excursion chekc in objects controller constants
payana_excursion_checkin_objects_permission_write_success_message_post = "Payana excursion checkin permission object successfully created!"
payana_excursion_checkin_objects_permission_write_success_message_put = "Payana excursion checkin permission object successfully updated!"
payana_excursion_checkin_objects_permission_delete_success_message = "Payana excursion checkin permission object successfully deleted!"
payana_excursion_checkin_objects_permission_create_failure_message_post = "Failed to create the Payana excursion checkin permission object"
payana_excursion_checkin_objects_permission_delete_failure_message = "Failed to delete the Payana excursion checkin permission object"
payana_excursion_checkin_objects_permission_write_failure_message_post = "Failed to update the Payana excursion checkin permission object"
payana_excursion_checkin_objects_permission_objects_delete_failure_message = "Failed to delete the Payana excursion checkin permission object contents"
payana_excursion_checkin_objects_permission_objects_delete_success_message = "Payana excursion checkin permission object content successfully deleted!"
payana_missing_excursion_checkin_objects_permission_object = "Missing Payana excursion checkin permission object in the request body"
payana_missing_excursion_checkin_objects_permission_header_exception = "Missing Payana excursion checkin permission header in the request body"

# Payana excursion objects controller constants
payana_excursion_objects_write_success_message_post = "Payana excursion checkin object successfully created!"
payana_excursion_objects_write_success_message_put = "Payana excursion checkin object successfully updated!"
payana_excursion_objects_delete_success_message = "Payana excursion checkin object successfully deleted!"
payana_excursion_objects_create_failure_message_post = "Failed to create the Payana excursion checkin object"
payana_excursion_objects_delete_failure_message = "Failed to delete the Payana excursion checkin object"
payana_excursion_objects_write_failure_message_post = "Failed to update the Payana excursion checkin object"
payana_excursion_objects_values_delete_failure_message = "Failed to delete the Payana excursion checkin object contents"
payana_excursion_objects_values_delete_success_message = "Payana excursion checkin object content successfully deleted!"
payana_missing_excursion_object = "Missing Payana excursion checkin object in the request body"
payana_missing_excursion_objects_header_exception = "Missing Payana excursion checkin header in the request body"
payana_excursion_id_header = "excursion_id"
payana_excursion_id_missing_exception_message = "Payana excursion in ID missing in the headers"

# Payana itinerary objects controller constants
payana_itinerary_objects_write_success_message_post = "Payana itinerary checkin object successfully created!"
payana_itinerary_objects_write_success_message_put = "Payana itinerary checkin object successfully updated!"
payana_itinerary_objects_delete_success_message = "Payana itinerary checkin object successfully deleted!"
payana_itinerary_objects_create_failure_message_post = "Failed to create the Payana itinerary checkin object"
payana_itinerary_objects_delete_failure_message = "Failed to delete the Payana itinerary checkin object"
payana_itinerary_objects_write_failure_message_post = "Failed to update the itinerary checkin object"
payana_itinerary_objects_values_delete_failure_message = "Failed to delete the Payana itinerary checkin object contents"
payana_itinerary_objects_values_delete_success_message = "Payana itinerary checkin object content successfully deleted!"
payana_missing_itinerary_object = "Missing Payana itinerary checkin object in the request body"
payana_missing_itinerary_objects_header_exception = "Missing Payana itinerary checkin header in the request body"
payana_itinerary_id_header = "itinerary_id"
payana_itinerary_name_header = "itinerary_name"

# Payana global city itinerary rating controller constants
payana_global_city_rating_itinerary_objects_write_success_message_post = "Payana global city itinerary rating object successfully created!"
payana_global_city_rating_itinerary_objects_write_success_message_put = "Payana global city itinerary rating object successfully updated!"
payana_global_city_rating_itinerary_objects_delete_success_message = "Payana global city itinerary rating object successfully deleted!"
payana_global_city_rating_itinerary_objects_create_failure_message_post = "Failed to create the Payana global city itinerary rating object"
payana_global_city_rating_itinerary_objects_delete_failure_message = "Failed to delete the Payana global city itinerary rating object"
payana_global_city_rating_itinerary_objects_write_failure_message_post = "Failed to update the Payana global city itinerary rating object"
payana_global_city_rating_itinerary_objects_values_delete_failure_message = "Failed to delete the Payana global city itinerary rating object contents"
payana_global_city_rating_itinerary_objects_values_delete_success_message = "Payana global city itinerary rating object content successfully deleted!"
payana_missing_global_city_rating_itinerary_object = "Missing Payana global city itinerary rating object in the request body"
payana_missing_global_city_rating_itinerary_objects_header_exception = "Missing Payana global city itinerary rating header in the request body"
payana_global_city_rating_itinerary_id_header = "city"

# Payana global city itinerary timestamp controller constants
payana_global_city_timestamp_itinerary_objects_write_success_message_post = "Payana global city itinerary timestamp object successfully created!"
payana_global_city_timestamp_itinerary_objects_write_success_message_put = "Payana global city itinerary timestamp object successfully updated!"
payana_global_city_timestamp_itinerary_objects_delete_success_message = "Payana global city itinerary timestamp object successfully deleted!"
payana_global_city_timestamp_itinerary_objects_create_failure_message_post = "Failed to create the Payana global city itinerary timestamp object"
payana_global_city_timestamp_itinerary_objects_delete_failure_message = "Failed to delete the Payana global city itinerary timestamp object"
payana_global_city_timestamp_itinerary_objects_write_failure_message_post = "Failed to update the Payana global city itinerary timestamp object"
payana_global_city_timestamp_itinerary_objects_values_delete_failure_message = "Failed to delete the Payana global city itinerary timestamp object contents"
payana_global_city_timestamp_itinerary_objects_values_delete_success_message = "Payana global city itinerary timestamp object content successfully deleted!"
payana_missing_global_city_timestamp_itinerary_object = "Missing Payana global city itinerary timestamp object in the request body"
payana_missing_global_city_timestamp_itinerary_objects_header_exception = "Missing Payana global city itinerary timestamp header in the request body"
payana_global_city_timestamp_itinerary_id_header = "city"

# Payana global influencer feed search itinerary cache controller constants
payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_post = "Payana global influencers feed search itinerary cache object successfully created!"
payana_global_influencers_feed_search_itinerary_cache_objects_write_success_message_put = "Payana global influencers feed search itinerary cache object successfully updated!"
payana_global_influencers_feed_search_itinerary_cache_objects_delete_success_message = "Payana influencers feed search itinerary cache object successfully deleted!"
payana_global_influencers_feed_search_itinerary_cache_objects_create_failure_message_post = "Failed to create the Payana influencers feed search itinerary cache object"
payana_global_influencers_feed_search_itinerary_cache_objects_delete_failure_message = "Failed to delete the Payana influencers feed search itinerary cache object"
payana_global_influencers_feed_search_itinerary_cache_objects_write_failure_message_post = "Failed to update the Payana influencers feed search itinerary cache object"
payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_failure_message = "Failed to delete the Payana influencers feed search itinerary cache object contents"
payana_global_influencers_feed_search_itinerary_cache_objects_values_delete_success_message = "Payana influencers feed search itinerary cache content successfully deleted!"
payana_missing_influencers_feed_search_itinerary_cache_itinerary_object = "Missing Payana influencers feed search itinerary cache object in the request body"
payana_missing_influencers_feed_search_itinerary_cache_objects_header_exception = "Missing Payana influencers feed search itinerary cache header in the request body"
payana_influencers_feed_search_itinerary_profile_id_header = "profile_id"

# Payana Comments controller constants
payana_comments_write_success_message_post = "Payana comments object successfully created!"
payana_comments_write_success_message_put = "Payana comments object successfully updated!"
payana_comments_delete_success_message = "Payana comments object successfully deleted!"
payana_comments_create_failure_message_post = "Failed to create the Payana comments object"
payana_comments_delete_failure_message = "Failed to delete the Payana comments object"
payana_comments_write_failure_message_post = "Failed to update the Payana comments object"
payana_comments_objects_delete_failure_message = "Failed to delete the Payana comments object contents"
payana_comments_objects_delete_success_message = "Payana comments object content successfully deleted!"
payana_missing_comments_object = "Missing Payana comments object in the request body"
payana_comment_id_header = "comment_id"
payana_comment_id_list_header = "comment_id_list"
payana_comment_id_missing_exception_message = "Payana comment ID missing"

# Payana Entity Comments controller constants
payana_entity_comments_write_success_message_post = "Payana entity comments object successfully created!"
payana_entity_comments_write_success_message_put = "Payana entity comments object successfully updated!"
payana_entity_comments_delete_success_message = "Payana entity comments object successfully deleted!"
payana_entity_comments_create_failure_message_post = "Failed to create the Payana entity comments object"
payana_entity_comments_delete_failure_message = "Failed to delete the Payana entity comments object"
payana_entity_comments_write_failure_message_post = "Failed to update the Payana entity comments object"
payana_entity_comments_objects_delete_failure_message = "Failed to delete the Payana entity comments object objects"
payana_entity_comments_objects_delete_success_message = "Payana entity comments object content successfully deleted!"
payana_missing_entity_comments_object = "Missing Payana entity comments object in the request body"
payana_missing_entity_comment_id_list_object = "Missing Payana entity comment ID list object in the request body"

# Payana check in objects controller constants
payana_check_in_write_success_message_post = "Payana check in object successfully created!"
payana_check_in_write_success_message_put = "Payana check in object successfully updated!"
payana_check_in_delete_success_message = "Payana check in object successfully deleted!"
payana_check_in_create_failure_message_post = "Failed to create the Payana check in object"
payana_check_in_delete_failure_message = "Failed to delete the Payana check in object"
payana_check_in_write_failure_message_post = "Failed to update the Payana check in object"
payana_check_in_objects_delete_failure_message = "Failed to delete the Payana check in object objects"
payana_check_in_objects_delete_success_message = "Payana check in object content successfully deleted!"
payana_missing_check_in_object = "Missing Payana check in object in the request body"
payana_check_in_id_header = "checkin_id"
payana_check_in_id_missing_exception_message = "Payana check in ID missing in the headers"
payana_check_in_id_empty_exception_message = "Payana check in ID is empty"

#Payana Profile Itinerary Table Controller constants
payana_profile_page_itineraries_write_success_message_post = "Profile Page Itinerary/Excursion/Activity Guide Object successfully created!"
payana_profile_page_itineraries_write_success_message_put = "Profile Page Itinerary/Excursion/Activity Guide successfully updated!"
payana_profile_page_itineraries_delete_success_message_put = "Profile Page Itinerary/Excursion/Activity Guide successfully deleted!"
payana_profile_page_itineraries_create_failure_message_post = "Failed to create a Profile Page Itinerary/Excursion/Activity Guide"
payana_profile_page_itineraries_write_failure_message_post = "Failed to update a Profile Page Itinerary/Excursion/Activity Guide"
payana_profile_page_itineraries_delete_failure_message_post = "Failed to delete a Profile Page Itinerary/Excursion/Activity Guide"
payana_missing_profile_page_itinerary_object = "Missing profile page itinerary/excusrion/activity guide object in the request body"
payana_profile_page_itinerary_objects_delete_failure_message = "Failed to delete the profile page itinerary/excusrion/activity guide object contents"
payana_profile_page_itinerary_objects_delete_success_message = "Profile page itinerary/excusrion/activity guide object content successfully deleted!"

#Payana Service end points response phrase
payana_200_response = "OK"
payana_201_response = "Created" 
payana_400_response = "Invalid Argument" 
payana_500_response = "Internal Server Error"

payana_200 = 200
payana_201 = 201
payana_400 = 400
payana_500 = 500

#Payana exception messages for service layer
payana_missing_profile_id_header_exception = "Missing Profile ID in the headers"
payana_missing_entity_id_header_exception = "Missing Entity ID in the headers"
payana_missing_comment_id_header_exception = "Missing comment ID in the headers"
payana_missing_city_header_exception = "Missing city in the headers"
payana_missing_mail_id_header_exception = "Missing Mail ID in the headers"
payana_missing_activity_guide_header_exception = "Missing activity in the headers"

# Payana not found excpetions
payana_city_not_found_exception = "City not found"
payana_top_excursion_guides_not_found_exception = "Excursion and cativity guides not found for the given city"
payana_invalid_activity_id_exception = "Invalid activity ID"
payana_activity_guide_header = "activity_guide"
payana_excursion_guide_header = "excursion"