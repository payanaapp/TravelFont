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
from payana.payana_bl.bigtable_utils.PayanaGlobalCityItineraryTable import PayanaGlobalCityItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalStateItineraryTable import PayanaPersonalStateItineraryTable
from payana.payana_bl.bigtable_utils.PayanaPersonalCountryItineraryTable import PayanaPersonalCountryItineraryTable
from payana.payana_bl.bigtable_utils.PayanaCityInfluencerTable import PayanaCityInfluencerTable


client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

payana_bigtable_init(client_config_file_path, bigtable_tables_schema_path)

global_city_influencer_obj = {
    "city": "cupertino##california##usa##november##2022",
    "city_global_influencers": {"12345678": "0.48"},
    "activities": ["generic", "hiking", "romantic"]
}

payana_global_city_influencer_obj = PayanaCityInfluencerTable(
    **global_city_influencer_obj)

payana_global_city_influencer_obj_write_status = payana_global_city_influencer_obj.update_city_influencers_bigtable()
print("payana_global_city_influencer_obj write status: " +
      str(payana_global_city_influencer_obj_write_status))

payana_global_city_influencer_table = bigtable_constants.payana_city_to_influencers_table
# We could use regular expression to exclude the year part while querying
row_id = payana_global_city_influencer_obj.row_id
payana_global_city_influencer_read_obj = PayanaBigTable(
    payana_global_city_influencer_table)
payana_global_city_influencer_read_row_obj = payana_global_city_influencer_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of add global city influencer: " +
      str(payana_global_city_influencer_read_row_obj is not None))

payana_city_to_influencers_table_global_influencers_column_family = bigtable_constants.payana_city_to_influencers_table_global_influencers_column_family

# Add another influencer to the same city
new_city_global_influencers = {"4567891023": "0.48"}
new_activities = ["generic", "hiking", "romantic"]

for new_activity in new_activities:
    for new_city_global_influencer, rating in new_city_global_influencers.items():

        activity_city_influencer_column_family_id = "_".join(
            [new_activity, payana_city_to_influencers_table_global_influencers_column_family])

        payana_global_city_influencer_table_write_object = bigtable_write_object_wrapper(
            row_id, activity_city_influencer_column_family_id, new_city_global_influencer, rating)

        payana_global_city_influencer_read_obj_update_status = payana_global_city_influencer_read_obj.insert_column(
            payana_global_city_influencer_table_write_object)
        print("payana_global_city_influencer_read_obj_update_status: " +
              str(payana_global_city_influencer_read_obj_update_status))

payana_global_city_influencer_read_row_obj = payana_global_city_influencer_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of update global city influencer: " +
      str(new_city_global_influencer in payana_global_city_influencer_read_row_obj[row_id][activity_city_influencer_column_family_id]))

print("Status of update global city influencer rating: " +
      str(rating == payana_global_city_influencer_read_row_obj[row_id][activity_city_influencer_column_family_id][new_city_global_influencer]))

# Edit existing activity object influencer rating
rating_new = "0.8765"
payana_global_city_influencer_table_write_object = bigtable_write_object_wrapper(
    row_id, activity_city_influencer_column_family_id, new_city_global_influencer, rating_new)

payana_global_city_influencer_read_obj_update_status = payana_global_city_influencer_read_obj.insert_column(
    payana_global_city_influencer_table_write_object)
print("payana_global_city_influencer_read_obj_update_status: " +
      str(payana_global_city_influencer_read_obj_update_status))

payana_global_city_influencer_read_row_obj = payana_global_city_influencer_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of update global city influencer: " +
      str(rating_new == payana_global_city_influencer_read_row_obj[row_id][activity_city_influencer_column_family_id][new_city_global_influencer]))

# Remove an influencer
for new_city_global_influencer, rating in new_city_global_influencers.items():
    new_activity = new_activities[0]

    activity_city_influencer_column_family_id = "_".join(
        [new_activity, payana_city_to_influencers_table_global_influencers_column_family])

    payana_global_city_influencer_table_write_object = bigtable_write_object_wrapper(
        row_id, activity_city_influencer_column_family_id, new_city_global_influencer, "")
    payana_global_city_influencer_table_delete_object_status = payana_global_city_influencer_read_obj.delete_bigtable_row_column(
        payana_global_city_influencer_table_write_object)
    print("payana_global_city_influencer_table_delete_object_status: " +
          str(payana_global_city_influencer_table_delete_object_status))
    payana_global_city_influencer_read_row_obj = payana_global_city_influencer_read_obj.get_row_dict(
        row_id, include_column_family=True)
    removed_itinerary_row = payana_global_city_influencer_read_row_obj[
        row_id][activity_city_influencer_column_family_id]

    print("Status of influencer remove: " +
          str(new_city_global_influencer not in removed_itinerary_row))

# Delete the whole row
payana_global_city_influencer_delete_object = bigtable_write_object_wrapper(
    row_id, "", "", "")
payana_global_city_influencer_read_obj_delete_status = payana_global_city_influencer_read_obj.delete_bigtable_row(
    payana_global_city_influencer_delete_object)
print("payana_global_city_influencer_read_obj_delete_status: " +
      str(payana_global_city_influencer_read_obj_delete_status))

payana_global_city_read_influencer_row_obj = payana_global_city_influencer_read_obj.get_row_dict(
    row_id, include_column_family=True)

print("Status of payana_global_city_read_influencer_row_obj delete row: " +
      str(len(payana_global_city_read_influencer_row_obj) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)
