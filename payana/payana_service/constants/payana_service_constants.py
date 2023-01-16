#!/usr/bin/env python

"""Defines Payana service constants
"""

# Payana service constants
status = "status"
message = "message"
status_code = "statusCode"
payana_empty_row_read_exception = "Empty result. Check if it's a valid entity key."


#Payana Profile Table Controller constants
payana_profile_table_write_success_message_post = "Profile successfully created!"
payana_profile_table_write_success_message_put = "Profile successfully updated!"
payana_profile_table_create_failure_message_post = "Failed to create the profile"
payana_profile_table_write_failure_message_post = "Failed to update the profile"
success_message_put = "Profile Information updated"
payana_profile_id_header = "profile_id"

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