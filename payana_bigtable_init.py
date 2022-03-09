from datetime import datetime

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaCommentsTable import PayanaCommentsTable
from payana.payana_bl.bigtable_utils.PayanaExcursionTable import PayanaExcursionTable
from payana.payana_bl.bigtable_utils.PayanaItineraryTable import PayanaItineraryTable
from payana.payana_bl.bigtable_utils.PayanaCheckinTable import PayanaCheckinTable
from payana.payana_bl.bigtable_utils.PayanaLikesTable import PayanaLikesTable
from payana.payana_bl.bigtable_utils.PayanaTravelBuddyTable import PayanaTravelBuddyTable
from payana.payana_bl.bigtable_utils.PayanaPlaceIdMetadataTable import PayanaPlaceIdMetadataTable
from payana.payana_bl.bigtable_utils.PayanaNeighboringCitiesTable import PayanaNeighboringCitiesTable
from payana.payana_bl.bigtable_utils.PayanaStateTable import PayanaStateTable
from payana.payana_bl.bigtable_utils.PayanaCountryTable import PayanaCountryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalPlaceIdItineraryTable import PayanaPersonalPlaceIdItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCityItineraryTable import PayanaPersonalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

comment_obj = {
    "comment_timestamp": "123456789",
    "profile_id": "abkr",
    "profile_name": "abkr",
    "comment": "Beautiful pic!",
    "likes_count": "11",
    "comment_id": "",
    "entity_id": "image_123"
}

payana_comment_obj = PayanaCommentsTable(**comment_obj)
payana_comment_obj.update_comment_bigtable()
comment_id = payana_comment_obj.entity_id
payana_comment_table = bigtable_constants.payana_comments_table
payana_comment_read_obj = PayanaBigTable(payana_comment_table)
print(payana_comment_read_obj.get_row_dict("image_123", include_column_family=False))

payana_profile_table_personal_info_column_family = bigtable_constants.payana_profile_table_personal_info_column_family
payana_profile_table_top_activities = bigtable_constants.payana_profile_table_top_activities

profile_obj = {
    payana_profile_table_personal_info_column_family :
    {
        "profile_name": "abkr",
        "user_name": "abkr",
        "blog_url": "abkr.com",
        "profile_description": "abkr's profile",
        "profile_id": "",
        "email": "abkr@gmail.com",
        "phone": "123456789",
        "private_account": "true",
        "gender": "male",
        "date_of_birth": "11/11/1111"
    },
    payana_profile_table_top_activities : 
    {
        "hiking": "0.67", 
        "adventure": "0.4", 
        "fashion": "0.78"
    }
}

payana_profile_obj = PayanaProfileTable(**profile_obj)
payana_profile_obj.update_profile_info_bigtable()
profile_id = payana_profile_obj.profile_id
payana_profile_table = bigtable_constants.payana_profile_table
payana_profile_read_obj = PayanaBigTable(payana_profile_table)
payana_profile_obj_read = payana_profile_read_obj.get_row_dict(profile_id, include_column_family=True)
print(payana_profile_obj_read)

itinerary_obj = {
    "excursion_id_list": {
        "1": "12345",
        "2": "23456",
        "3": "34567"
    },
    "activities_list": {"hiking": "1", "roadtrip": "1"},
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "itinerary_metadata": {
        "description": "Summer trip to Montana",
        "visit_timestamp": "123456789",
        "itinerary_id": "",
        "itinerary_owner_profile_id": "1234567",
        "place_id": "123456",
        "place_name": "SF"
    }
}

payana_itinerary_obj = PayanaItineraryTable(**itinerary_obj)
payana_itinerary_obj.update_itinerary_bigtable()
itinerary_id = payana_itinerary_obj.itinerary_id
payana_itinerary_table = bigtable_constants.payana_itinerary_table
payana_itinerary_read_obj = PayanaBigTable(payana_itinerary_table)
print(payana_itinerary_read_obj.get_row_dict(itinerary_id, include_column_family=True))

excursion_obj = {
    "checkin_id_list": {
        "one": "12345",
        "two": "23456",
        "three": "34567"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "4", "roadtrip": "6"},
    "excursion_metadata": {
        "excursion_id": "",
        "transport_mode": "drive",
        "place_id": "1234567",
        "excursion_owner_profile_id": "1234567",
        "visit_timestamp": "123456789",
        "description": "",
        "itinerary_id": "1234",
        "place_name": "SF"
    }
}

payana_excursion_obj = PayanaExcursionTable(**excursion_obj)
payana_excursion_obj.update_excursion_bigtable()
excursion_id = payana_excursion_obj.excursion_id
payana_excursion_table = bigtable_constants.payana_excursion_table
payana_excursion_read_obj = PayanaBigTable(payana_excursion_table)
print(payana_excursion_read_obj.get_row_dict(excursion_id, include_column_family=True))

checkin_obj = {
    "image_id_list": {
        "1": "img_id_1",
        "2": "img_id_2",
        "3": "img_id_3"
    },
    "participants_list": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "activities_list": {"hiking": "8", "roadtrip": "9"},
        "instagram_metadata": {
        "instagram_embed_url": "xyz.com",
        "instagram_post_id": "12345"
    },
    "airbnb_metadata": {
        "airbnb_embed_url": "xyz.com",
        "airbnb_post_id": "12345"
    },
    "checkin_metadata": {
        "transport_mode": "drive",
        "description": "Enjoying the beach!",
        "checkin_owner_profile_id": "1234567",
        "visit_timestamp": "123456789",
        "checkin_id": "",
        "place_id": "1234567",
        "excursion_id": "12345",
        "itinerary_id": "12345",
        "place_name": "SF"
    }
}

payana_checkin_obj = PayanaCheckinTable(**checkin_obj)
payana_checkin_obj.update_checkin_bigtable()
checkin_id = payana_checkin_obj.checkin_id
payana_checkin_table = bigtable_constants.payana_checkin_table
payana_checkin_read_obj = PayanaBigTable(payana_checkin_table)
print(payana_checkin_read_obj.get_row_dict(checkin_id, include_column_family=True))

likes_obj = {
    "payana_likes": {"pf_id_1": "1234567", "pf_id_2": "1234567", "pf_id_3": "1234567"},
    "entity_id": "12345"
}

payana_likes_obj = PayanaLikesTable(**likes_obj)
payana_likes_obj.update_likes_bigtable()
payana_likes_table = bigtable_constants.payana_likes_table
like_object_id = payana_likes_obj.entity_id
payana_likes_read_obj = PayanaBigTable(payana_likes_table)
print(payana_likes_read_obj.get_row_dict(like_object_id, include_column_family=True))



travel_buddy_obj = {
    "profile_id": "1234567",
    "friend_profile_id": "1234567"
}

payana_travel_buddy_obj = PayanaTravelBuddyTable(**travel_buddy_obj)
payana_travel_buddy_obj.update_travel_buddy_bigtable()
payana_travel_buddy_table = bigtable_constants.payana_travel_buddy_list_table
profile_id = payana_travel_buddy_obj.profile_id
friend_profile_id = payana_travel_buddy_obj.friend_profile_id
payana_travel_buddy_read_obj = PayanaBigTable(payana_travel_buddy_table)
print(payana_travel_buddy_read_obj.get_row_dict(profile_id, include_column_family=True))
print(payana_travel_buddy_read_obj.get_row_dict(friend_profile_id, include_column_family=True))

place_id_metadata_obj = {
    "place_id": "1234567",
    "city": "cupertino##california##usa",
    "state": "california##usa",
    "country": "usa",
    "zipcode": "95014"
}

payana_place_id_metadata_obj = PayanaPlaceIdMetadataTable(**place_id_metadata_obj)
payana_place_id_metadata_obj.update_place_metadata_bigtable()
payana_place_id_metadata_table = bigtable_constants.payana_place_metadata_table
place_id = payana_place_id_metadata_obj.place_id
payana_place_id_metadata_read_obj = PayanaBigTable(payana_place_id_metadata_table)
print(payana_place_id_metadata_read_obj.get_row_dict(place_id, include_column_family=False))

neighboring_cities_obj = {
    "city": "cupertino##california##usa",
    "neighboring_city_list": {
        "cupertino##california##usa": "72.56",
        "sanjose##california##usa": "82.56"
    }
}

payana_neighboring_cities_obj = PayanaNeighboringCitiesTable(**neighboring_cities_obj)
payana_neighboring_cities_obj.update_neighboring_city_list_bigtable()
payana_neighboring_cities_table = bigtable_constants.payana_neighboring_cities_table
city = payana_neighboring_cities_obj.city
payana_neighboring_cities_read_obj = PayanaBigTable(payana_neighboring_cities_table)
print(payana_neighboring_cities_read_obj.get_row_dict(city, include_column_family=True))

state_obj = {
    "state": "california##usa",
    "city": "cupertino##california##usa"
}

payana_state_obj = PayanaStateTable(**state_obj)
payana_state_obj.update_state_bigtable()
payana_state_table = bigtable_constants.payana_place_state_table
state = payana_state_obj.state
payana_state_read_obj = PayanaBigTable(payana_state_table)
print(payana_state_read_obj.get_row_dict(state, include_column_family=True))

country_obj = {
    "country": "usa",
    "city": "cupertino##california##usa"
}

payana_country_obj = PayanaCountryTable(**country_obj)
payana_country_obj.update_country_bigtable()
payana_country_table = bigtable_constants.payana_place_country_table
country = payana_country_obj.country
payana_country_read_obj = PayanaBigTable(payana_country_table)
print(payana_country_read_obj.get_row_dict(country, include_column_family=True))

personal_place_id_itinerary_obj = {
    "profile_id": "12345",
    "place_id": "12345",
    "itinerary_id": "12345",
    "excursion_id": "12345",
    "checkin_id": "12345",
    "activities": ["hiking", "romantic", "exotic"]
}

payana_personal_place_id_itinerary_obj = PayanaPersonalPlaceIdItineraryTable(**personal_place_id_itinerary_obj)
payana_personal_place_id_itinerary_obj.update_personal_place_id_itinerary_bigtable()
payana_personal_place_id_itinerary_table = bigtable_constants.payana_personal_place_id_itinerary_table
place_id = payana_personal_place_id_itinerary_obj.place_id
profile_id = payana_personal_place_id_itinerary_obj.profile_id
current_year = str(datetime.now().year)
row_id = profile_id + "##" + place_id + "##" + current_year
payana_personal_place_id_itinerary_read_obj = PayanaBigTable(payana_personal_place_id_itinerary_table)
print(payana_personal_place_id_itinerary_read_obj.get_row_dict(row_id, include_column_family=True))

personal_city_itinerary_obj = {
    "profile_id": "12345",
    "city": "cupertino",
    "itinerary_id": "12345",
    "excursion_id": "12345",
    "checkin_id": "12345",
    "activities": ["hiking", "romantic", "exotic"]
}

payana_personal_city_itinerary_obj = PayanaPersonalCityItineraryTable(**personal_city_itinerary_obj)
payana_personal_city_itinerary_obj.update_personal_city_itinerary_bigtable()
payana_personal_city_itinerary_table = bigtable_constants.payana_personal_city_itinerary_table
city = payana_personal_city_itinerary_obj.city
profile_id = payana_personal_city_itinerary_obj.profile_id
current_year = str(datetime.now().year)
row_id = profile_id + "##" + city + "##" + current_year
payana_personal_city_itinerary_read_obj = PayanaBigTable(payana_personal_city_itinerary_table)
print(payana_personal_city_itinerary_read_obj.get_row_dict(row_id, include_column_family=True))

personal_state_itinerary_obj = {
    "profile_id": "12345",
    "state": "california##usa",
    "itinerary_id": "12345",
    "excursion_id": "12345",
    "checkin_id": "12345",
    "activities": ["hiking", "romantic", "exotic"]
}

payana_personal_state_itinerary_obj = PayanaPersonalStateItineraryTable(**personal_state_itinerary_obj)
payana_personal_state_itinerary_obj.update_personal_state_itinerary_bigtable()
payana_personal_state_itinerary_table = bigtable_constants.payana_personal_state_itinerary_table
state = payana_personal_state_itinerary_obj.state
profile_id = payana_personal_state_itinerary_obj.profile_id
current_year = str(datetime.now().year)
row_id = profile_id + "##" + state + "##" + current_year
payana_personal_state_itinerary_read_obj = PayanaBigTable(payana_personal_state_itinerary_table)
print(payana_personal_state_itinerary_read_obj.get_row_dict(row_id, include_column_family=True))

personal_country_itinerary_obj = {
    "profile_id": "12345",
    "country": "usa",
    "itinerary_id": "12345",
    "excursion_id": "12345",
    "checkin_id": "12345",
    "activities": ["hiking", "romantic", "exotic"]
}

payana_personal_country_itinerary_obj = PayanaPersonalCountryItineraryTable(**personal_country_itinerary_obj)
payana_personal_country_itinerary_obj.update_personal_country_itinerary_bigtable()
payana_personal_country_itinerary_table = bigtable_constants.payana_personal_country_itinerary_table
country = payana_personal_country_itinerary_obj.country
profile_id = payana_personal_country_itinerary_obj.profile_id
current_year = str(datetime.now().year)
row_id = profile_id + "##" + country + "##" + current_year
payana_personal_country_itinerary_read_obj = PayanaBigTable(payana_personal_country_itinerary_table)
print(payana_personal_country_itinerary_read_obj.get_row_dict(row_id, include_column_family=True))

profile_page_itinerary_obj = {
    "profile_id": "",
    "object_id": "",
    "trip_type": "itinerary"
}

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)