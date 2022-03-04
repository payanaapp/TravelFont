#!/usr/bin/env python

"""Defines Payana service constants
"""

#Payana Profile Table Controller constants
success_message_post = "Profile created"
success_message_put = "Profile Information updated"
payana_profile_id_header = "X-Profile-Id"

#Payana Service end points response phrase
payana_200_response = "OK" 
payana_400_response = "Invalid Argument" 
payana_500_response = "Internal Server Error"

#Payana exception messages for service layer
payana_missing_profile_id_header_exception = "Missing Profile ID in the headers"