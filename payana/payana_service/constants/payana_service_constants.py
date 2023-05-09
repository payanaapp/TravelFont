#!/usr/bin/env python

"""Defines Payana service constants
"""

# Payana service constants
status = "status"
message = "message"
status_code = "statusCode"

#Payana generic constants
payana_profile_id_header = "profile_id"
payana_empty_row_read_exception = "Empty result. Check if it's a valid entity key."

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