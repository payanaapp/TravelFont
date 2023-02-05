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
payana_likes_objects_delete_failure_message = "Failed to delete the Payana likes object objects"
payana_likes_objects_delete_success_message = "Payana likes object content successfully deleted!"
payana_missing_likes_object = "Missing Payana likes object in the request body"
payana_entity_id_header = "entity_id"

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
