#!/usr/bin/env python

"""Defines Payana service constants
"""

# Payana service constants
status = "status"
message = "message"
status_code = "statusCode"

#Payana Profile Table Controller constants
payana_profile_table_write_success_message_post = "Profile successfully created!"
payana_profile_table_write_success_message_put = "Profile successfully updated!"
payana_profile_table_delete_success_message = "Profile successfully deleted!"
payana_profile_table_create_failure_message_post = "Failed to create the profile"
payana_profile_table_delete_failure_message = "Failed to delete the profile"
payana_profile_table_write_failure_message_post = "Failed to update the profile"
payana_profile_table_success_message_put = "Profile Information updated"
payana_profile_id_header = "profile_id"
payana_empty_row_read_exception = "Empty result. Check if it's a valid entity key."
payana_missing_profile_object = "Missing profile object in the request body"
payana_profile_table_objects_delete_failure_message = "Failed to delete the profile objects"
payana_profile_table_objects_delete_success_message = "Profile content successfully deleted!"

#Payana Profile Itinerary Table Controller constants
payana_profile_page_itineraries_write_success_message_post = "Itinerary successfully created!"
payana_profile_page_itineraries_write_success_message_put = "Itinerary successfully updated!"
payana_profile_page_itineraries_delete_success_message_put = "Itinerary successfully deleted!"
payana_profile_page_itineraries_create_failure_message_post = "Failed to create an itinerary"
payana_profile_page_itineraries_write_failure_message_post = "Failed to update an itinerary"
payana_profile_page_itineraries_delete_failure_message_post = "Failed to delete an itinerary"

payana_profile_page_excursions_write_success_message_post = "Excursion successfully created!"
payana_profile_page_excursions_write_success_message_put = "Excursion successfully updated!"
payana_profile_page_excursions_delete_success_message_put = "Excursion successfully deleted!"
payana_profile_page_excursions_create_failure_message_post = "Failed to create an excursion"
payana_profile_page_excursions_write_failure_message_post = "Failed to update an excursion"
payana_profile_page_excursions_delete_failure_message_post = "Failed to delete an excursion"

payana_profile_page_activity_guide_write_success_message_post = "Activity guide successfully created!"
payana_profile_page_activity_guide_write_success_message_put = "Activity guide successfully updated!"
payana_profile_page_activity_guide_delete_success_message_put = "Activity guide successfully deleted!"
payana_profile_page_activity_guide_create_failure_message_post = "Failed to create an activity guide"
payana_profile_page_activity_guide_write_failure_message_post = "Failed to update an activity guide"
payana_profile_page_activity_guide_delete_failure_message_post = "Failed to delete an activity guide"

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
