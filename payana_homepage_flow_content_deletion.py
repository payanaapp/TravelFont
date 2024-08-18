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

client_config_file_path = bigtable_constants.bigtable_client_config_path
bigtable_tables_schema_path = bigtable_constants.bigtable_schema_config_file

# Step 2 in payana_homepage_flow.txt 

# delete a neighboring city obj - step 2 in payana_homepage_flow_content_generator
row_key = "sanfrancisco##california##usa"

payana_neighboring_city_delete_object = bigtable_write_object_wrapper(row_key, "", "", "")

payana_neighboring_cities_read_obj = PayanaBigTable(bigtable_constants.payana_neighboring_cities_table)
payana_neighboring_cities_obj_delete_status = payana_neighboring_cities_read_obj.delete_bigtable_row(payana_neighboring_city_delete_object)

print("payana_neighboring_cities_obj_delete_status: " + str(payana_neighboring_cities_obj_delete_status))

# delete excursion obj - step 3A1 in payana_homepage_flow_content_generator
excursion_id_list = []
payana_excursion_read_obj = PayanaBigTable(bigtable_constants.payana_excursion_table)

for excursion_id in excursion_id_list:
    excursion_row_delete_object = bigtable_write_object_wrapper(
        excursion_id, "", "", "")
    payana_excursion_obj_delete_status = payana_excursion_read_obj.delete_bigtable_row(excursion_row_delete_object)

    print("Payana excursion object delete status: " + str(payana_excursion_obj_delete_status))

    excursion_obj_read_activity_update = payana_excursion_read_obj.get_row_dict(
        excursion_id, include_column_family=True)

print("Status of excursion obj delete row:" +
      str(len(excursion_obj_read_activity_update) == 0))

payana_bigtable_cleanup(client_config_file_path, bigtable_tables_schema_path)