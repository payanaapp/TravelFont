from datetime import datetime
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

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
from payana.payana_bl.bigtable_utils.PayanaPersonalInfluencerFeedSearchItineraryCache import PayanaPersonalInfluencerFeedSearchItineraryCache

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)
payana_personal_city_itinerary_table_rating_column_family_id = bigtable_constants.payana_personal_city_itinerary_table_rating_column_family_id

feed_search_itinerary_cache_obj = {
    "profile_id": "12345",
    "excursion_id": {"cupertino##california##usa": ["123456789", "234567891", "345678901"]},
    "activity_guide_id": {"cupertino##california##usa": ["123456789", "234567891", "345678901"]},
    "activities": ["generic", "hiking", "romantic", "exotic"],
    "category": ["rating", "timestamp"]
}

payana_feed_search_itinerary_cache_obj = PayanaPersonalInfluencerFeedSearchItineraryCache(
    **feed_search_itinerary_cache_obj)
payana_feed_search_itinerary_cache_obj_write_status = payana_feed_search_itinerary_cache_obj.update_feed_search_itinerary_bigtable()
print("payana_feed_search_itinerary_cache_obj_write_status: " +
      str(payana_feed_search_itinerary_cache_obj_write_status))

payana_personal_influencer_feed_search_itinerary_cache_table = bigtable_constants.payana_personal_influencer_feed_search_itinerary_cache_table
# We could use regular expression to exclude the year part while querying
row_id = payana_feed_search_itinerary_cache_obj.row_id
payana_feed_search_itinerary_cache_read_obj = PayanaBigTable(
    payana_personal_influencer_feed_search_itinerary_cache_table)
payana_feed_search_itinerary_cache_read_row_obj = payana_feed_search_itinerary_cache_read_obj.get_row_dict(
    row_id, include_column_family=True)

print(payana_feed_search_itinerary_cache_read_row_obj)

print("Status of add feed search itinerary: " +
      str(payana_feed_search_itinerary_cache_read_row_obj is not None))

activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family

# Edit a specific activity based list of excursion IDs
activity = "generic"
excursion_id_list_new = {"cupertino##california##usa": [
    "123456789", "234567891"]}
category = "rating"

payana_feed_search_itinerary_cache_excursion_id_column_family = bigtable_constants.payana_feed_search_itinerary_cache_excursion_id_column_family

payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id = "_".join(
    [activity, category, payana_feed_search_itinerary_cache_excursion_id_column_family])

for city, excursion_id_list in excursion_id_list_new.items():

    payana_feed_search_itinerary_cache_write_object = bigtable_write_object_wrapper(
        row_id, payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id, city, "##".join(excursion_id_list))

    payana_feed_search_itinerary_cache_read_obj_write_status = payana_feed_search_itinerary_cache_read_obj.insert_column(
        payana_feed_search_itinerary_cache_write_object)
    
    print("payana_feed_search_itinerary_cache_read_obj_update_status: " + str(payana_feed_search_itinerary_cache_read_obj_write_status))
    
    payana_feed_search_itinerary_cache_read_row_obj = payana_feed_search_itinerary_cache_read_obj.get_row_dict(
        row_id, include_column_family=True)
    
    print("Payana feed search excursion ID update: " + str("##".join(excursion_id_list) == payana_feed_search_itinerary_cache_read_row_obj[row_id][payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id][city]))

# Add another city excursion list
new_excursion_id = {"phoenix##arizona##usa": ["123456789", "234567891", "345678901"]}
new_activities = ["generic", "hiking", "romantic", "exotic"]
new_category = ["rating", "timestamp"]

for new_activity in new_activities:
    for category in new_category:
        for new_city, new_excursion_id_list in new_excursion_id.items():
            
            payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id = "_".join(
                [new_activity, category, payana_feed_search_itinerary_cache_excursion_id_column_family])
            
            payana_feed_search_itinerary_cache_write_object = bigtable_write_object_wrapper(
                row_id, payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id, new_city, "##".join(new_excursion_id_list))

            payana_feed_search_itinerary_cache_read_obj_write_status = payana_feed_search_itinerary_cache_read_obj.insert_column(
                payana_feed_search_itinerary_cache_write_object)
    
            print("payana_feed_search_itinerary_cache_read_obj_new_write_status: " + str(payana_feed_search_itinerary_cache_read_obj_write_status))
    
            payana_feed_search_itinerary_cache_read_row_obj = payana_feed_search_itinerary_cache_read_obj.get_row_dict(
                row_id, include_column_family=True)
    
            print("Payana feed search excursion ID new city write: " + str("##".join(new_excursion_id_list) == payana_feed_search_itinerary_cache_read_row_obj[row_id][payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id][new_city]))

# Remove a city column
for new_activity in new_activities:
    for category in new_category:
        for new_city, new_excursion_id_list in new_excursion_id.items():

            payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id = "_".join(
                [new_activity, category, payana_feed_search_itinerary_cache_excursion_id_column_family])
            
            payana_feed_search_itinerary_cache_write_object = bigtable_write_object_wrapper(
                row_id, payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id, new_city, "")

            payana_feed_search_itinerary_cache_read_obj_delete_status = payana_feed_search_itinerary_cache_read_obj.delete_bigtable_row_column(
                payana_feed_search_itinerary_cache_write_object)
    
            print("payana_feed_search_itinerary_cache_read_obj_delete_status: " + str(payana_feed_search_itinerary_cache_read_obj_delete_status))
    
            payana_feed_search_itinerary_cache_read_row_obj = payana_feed_search_itinerary_cache_read_obj.get_row_dict(
                row_id, include_column_family=True)
    
            print("Payana feed search excursion ID new city delete: " + str(new_city not in payana_feed_search_itinerary_cache_read_row_obj[row_id][payana_feed_search_itinerary_cache_excursion_activity_generic_column_family_id]))   

# Delete the whole row
payana_feed_search_itinerary_cache_row_delete_object = bigtable_write_object_wrapper(
    row_id, "", "", "")
payana_feed_search_itinerary_cache_read_obj_delete_status = payana_feed_search_itinerary_cache_read_obj.delete_bigtable_row(
    payana_feed_search_itinerary_cache_row_delete_object)
print("payana_feed_search_itinerary_cache_read_obj_delete_status: " +
      str(payana_feed_search_itinerary_cache_read_obj_delete_status))

payana_feed_search_read_row_obj = payana_feed_search_itinerary_cache_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of payana feed search delete row: " +
      str(len(payana_feed_search_read_row_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
