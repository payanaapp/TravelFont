from datetime import datetime
from payana.payana_bl.bigtable_utils.bigtable_read_write_object_wrapper import bigtable_write_object_wrapper

from payana.payana_bl.bigtable_utils.payana_bigtable_init import payana_bigtable_init
from payana.payana_bl.bigtable_utils.payana_bigtable_cleanup import payana_bigtable_cleanup
from payana.payana_bl.bigtable_utils.constants import bigtable_constants
from payana.payana_bl.bigtable_utils.PayanaProfileTable import PayanaProfileTable
from payana.payana_bl.bigtable_utils.PayanaBigTable import PayanaBigTable
from payana.payana_bl.bigtable_utils.PayanaProfilePageItineraryTable import PayanaProfilePageItineraryTable
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

profile_page_itinerary_obj = {
    "profile_id": "12345",
    "itinerary_id": {"12345" : "0.48"},
    "excursion_id": {"12345" : "0.48"},
    "checkin_id": {"12345" : "0.48"},
    "activities": ["hiking", "romantic", "exotic"]
}

payana_profile_page_itinerary_obj = PayanaProfilePageItineraryTable(**profile_page_itinerary_obj)
payana_profile_page_itinerary_obj.update_payana_profile_page_itinerary_bigtable()
payana_profile_page_itinerary_table = bigtable_constants.payana_profile_page_itinerary_table
row_id = payana_profile_page_itinerary_obj.row_id #We could use regular expression to exclude the year part while querying
payana_profile_page_itinerary_read_obj = PayanaBigTable(payana_profile_page_itinerary_table)
payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)

print("Status of add payana_profile_page itinerary: " + str(payana_profile_page_itinerary_read_row_obj is not None))

activity_generic_column_family_id = bigtable_constants.payana_generic_activity_column_family

# generic activity write objects
itinerary_activity_generic_column_family_id = "_".join([activity_generic_column_family_id, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

excursion_activity_generic_column_family_id = "_".join([activity_generic_column_family_id, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

checkin_activity_generic_column_family_id = "_".join([activity_generic_column_family_id, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

payana_profile_page_itinerary_table_itinerary_id_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value
payana_profile_page_itinerary_table_excursion_id_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value
payana_profile_page_itinerary_table_checkin_id_quantifier_value = bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value

#Add another itinerary ID, excursion ID and checkin ID
itinerary_new = {"6789" : "0.48"}
excursion_new =  {"6789" : "0.48"}
checkin_new = {"6789" : "0.48"}

for itinerary_id, rating in itinerary_new.items():
    payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(row_id, itinerary_activity_generic_column_family_id, itinerary_id, rating)
    payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_itinerary_table_write_object)
    payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    updated_rating = payana_profile_page_itinerary_read_row_obj[row_id][itinerary_activity_generic_column_family_id][itinerary_id]

    print("Status of itinerary ID update: " + str(rating == updated_rating))
    
for excursion_id, rating in excursion_new.items():
    payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(row_id, excursion_activity_generic_column_family_id, excursion_id, rating)
    payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_excursion_table_write_object)
    payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    updated_rating = payana_profile_page_excursion_read_row_obj[row_id][excursion_activity_generic_column_family_id][excursion_id]

    print("Status of excursion ID update: " + str(rating == updated_rating))
    
for checkin_id, rating in checkin_new.items():
    payana_profile_page_checkin_table_write_object = bigtable_write_object_wrapper(row_id, checkin_activity_generic_column_family_id, checkin_id, rating)
    payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_checkin_table_write_object)
    payana_profile_page_checkin_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    updated_rating = payana_profile_page_checkin_read_row_obj[row_id][checkin_activity_generic_column_family_id][checkin_id]

    print("Status of checkin ID update: " + str(rating == updated_rating))

#Add another itinerary ID, excursion ID and checkin ID with activities
profile_page_itinerary_update_obj = {
    "itinerary_id": {"34567" : "0.48"},
    "excursion_id": {"34567" : "0.48"},
    "checkin_id": {"34567" : "0.48"},
    "activities": ["hiking", "romantic", "exotic"]
}

itinerary_update = profile_page_itinerary_update_obj[payana_profile_page_itinerary_table_itinerary_id_quantifier_value]
excursion_update =  profile_page_itinerary_update_obj[payana_profile_page_itinerary_table_excursion_id_quantifier_value]
checkin_update = profile_page_itinerary_update_obj[payana_profile_page_itinerary_table_checkin_id_quantifier_value]
activity_update = profile_page_itinerary_update_obj[bigtable_constants.payana_profile_page_itinerary_table_activities]

for itinerary_id, rating in itinerary_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(row_id, itinerary_activity_column_family_id, itinerary_id, rating)
        payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_itinerary_table_write_object)
        payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        updated_rating = payana_profile_page_itinerary_read_row_obj[row_id][itinerary_activity_column_family_id][itinerary_id]

        print("Status of itinerary ID activity update: " + str(rating == updated_rating))
        
for excursion_id, rating in excursion_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(row_id, excursion_activity_column_family_id, excursion_id, rating)
        payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_excursion_table_write_object)
        payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        updated_rating = payana_profile_page_excursion_read_row_obj[row_id][excursion_activity_column_family_id][excursion_id]

        print("Status of excursion ID activity update: " + str(rating == updated_rating))
        
for checkin_id, rating in checkin_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_checkin_table_write_object = bigtable_write_object_wrapper(row_id, checkin_activity_column_family_id, checkin_id, rating)
        payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_checkin_table_write_object)
        payana_profile_page_checkin_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        updated_rating = payana_profile_page_checkin_read_row_obj[row_id][checkin_activity_column_family_id][checkin_id]

        print("Status of checkin ID activity update: " + str(rating == updated_rating))

#Remove an itinerary ID, excursion ID, check ID
for itinerary_id, rating in itinerary_new.items():
    payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(row_id, itinerary_activity_generic_column_family_id, itinerary_id, "")
    payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(payana_profile_page_itinerary_table_write_object)
    payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[row_id][itinerary_activity_generic_column_family_id]

    print("Status of itinerary ID remove: " + str(itinerary_id not in removed_itinerary_row))
    
for excursion_id, rating in excursion_new.items():
    payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(row_id, excursion_activity_generic_column_family_id, excursion_id, "")
    payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(payana_profile_page_excursion_table_write_object)
    payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    removed_excursion_row = payana_profile_page_excursion_read_row_obj[row_id][excursion_activity_generic_column_family_id]

    print("Status of excursion ID remove: " + str(excursion_id not in removed_excursion_row))
    
for checkin_id, rating in checkin_new.items():
    payana_profile_page_checkin_table_write_object = bigtable_write_object_wrapper(row_id, checkin_activity_generic_column_family_id, checkin_id, "")
    payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(payana_profile_page_checkin_table_write_object)
    payana_profile_page_checkin_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
    removed_checkin_row = payana_profile_page_checkin_read_row_obj[row_id][checkin_activity_generic_column_family_id]

    print("Status of checkin ID remove: " + str(checkin_id not in removed_checkin_row))

#Remove the activity based itinerary ID, excursion ID, checkin ID
for itinerary_id, rating in itinerary_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_itinerary_table_write_object = bigtable_write_object_wrapper(row_id, itinerary_activity_column_family_id, itinerary_id, "")
        payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(payana_profile_page_itinerary_table_write_object)
        payana_profile_page_itinerary_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        removed_itinerary_row = payana_profile_page_itinerary_read_row_obj[row_id][itinerary_activity_column_family_id]

        print("Status of itinerary ID activity remove: " + str(itinerary_id not in removed_itinerary_row))
        
for excursion_id, rating in excursion_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_excursion_table_write_object = bigtable_write_object_wrapper(row_id, excursion_activity_column_family_id, excursion_id, "")
        payana_profile_page_itinerary_read_obj.delete_bigtable_row_column(payana_profile_page_excursion_table_write_object)
        payana_profile_page_excursion_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        removed_excursion_row = payana_profile_page_excursion_read_row_obj[row_id][excursion_activity_column_family_id]

        print("Status of excursion ID activity remove: " + str(excursion_id not in removed_excursion_row))
        
for checkin_id, rating in checkin_update.items():
    for activity in activity_update:
        itinerary_activity_column_family_id =  "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_itinerary_id_quantifier_value])

        excursion_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_excursion_id_quantifier_value])

        checkin_activity_column_family_id = "_".join([activity, bigtable_constants.payana_profile_page_itinerary_table_checkin_id_quantifier_value])

        payana_profile_page_checkin_table_write_object = bigtable_write_object_wrapper(row_id, checkin_activity_column_family_id, checkin_id, "")
        payana_profile_page_itinerary_read_obj.insert_column(payana_profile_page_checkin_table_write_object)
        payana_profile_page_checkin_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)
        removed_checkin_row = payana_profile_page_checkin_read_row_obj[row_id][checkin_activity_column_family_id]

        print("Status of checkin ID activity remove: " + str(checkin_id not in removed_checkin_row))

#Delete the whole row 
payana_profile_page_row_delete_object = bigtable_write_object_wrapper(row_id, "", "", "")
payana_profile_page_itinerary_read_obj.delete_bigtable_row(payana_profile_page_row_delete_object)
payana_profile_page_read_row_obj = payana_profile_page_itinerary_read_obj.get_row_dict(row_id, include_column_family=True)

print("Status of profile_page delete row: " + str(len(payana_profile_page_read_row_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)