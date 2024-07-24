from payana.payana_bl.bigtable_utils.constants import bigtable_constants

payana_excursion_object_model = {
    bigtable_constants.payana_excursion_column_family_checkin_id_list: {},
    bigtable_constants.payana_excursion_column_family_image_id_list: {},
    bigtable_constants.payana_excursion_column_family_cities_checkin_id_list: {},
    bigtable_constants.payana_excursion_column_family_participants_list: {},
    bigtable_constants.payana_excursion_activities_list: {},
    bigtable_constants.payana_excursion_metadata: {
        bigtable_constants.payana_excursion_id: "",
        bigtable_constants.payana_excursion_activity_guide: "",
        bigtable_constants.payana_excursion_transport_mode: "",
        bigtable_constants.payana_excursion_place_id: "",
        bigtable_constants.payana_excursion_column_family_excursion_owner_profile_id: "",
        bigtable_constants.payana_excursion_column_family_create_timestamp: "",
        bigtable_constants.payana_excursion_column_family_last_updated_timestamp: "",
        bigtable_constants.payana_excursion_column_family_description: "",
        bigtable_constants.payana_excursion_itinerary_id: "",
        bigtable_constants.payana_excursion_itinerary_name: "",
        bigtable_constants.payana_excursion_place_name: "",
        bigtable_constants.payana_excursion_city: "",
        bigtable_constants.payana_excursion_state: "",
        bigtable_constants.payana_excursion_country: ""
    }
}

payana_itinerary_object_model = {
    bigtable_constants.payana_itinerary_column_family_excursion_id_list: {},
    bigtable_constants.payana_itinerary_activities_list: {},
    bigtable_constants. payana_itinerary_metadata: {
        bigtable_constants.payana_itinerary_column_family_description: "",
        bigtable_constants.payana_itinerary_column_family_visit_timestamp: "",
        bigtable_constants.payana_itinerary_id: "",
        bigtable_constants.payana_itinerary_column_family_itinerary_owner_profile_id: "", 
        bigtable_constants.payana_itinerary_place_id: "",
        bigtable_constants.payana_itinerary_place_name: "",
        # Useful when search happens on a specific profile for a given city/state/country
        bigtable_constants.payana_itinerary_city: "",
        bigtable_constants.payana_itinerary_state: "",
        bigtable_constants.payana_itinerary_country: "",
        bigtable_constants.payana_itinerary_last_updated_timestamp: ""
    },
    bigtable_constants.payana_itinerary_column_family_cities_list: {}
}

profile_page_itinerary_model = {
    bigtable_constants.payana_profile_table_profile_id: "",
    bigtable_constants.payana_profile_page_itinerary_table_saved_itinerary_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_saved_excursion_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_saved_activity_guide_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_created_itinerary_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_created_activity_guide_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_created_excursion_id_mapping_quantifier_value: {},
    bigtable_constants.payana_profile_page_itinerary_table_activities: []
}