from flask_restx import fields
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

payana_profile_table_profile_name = bigtable_constants.payana_profile_table_profile_name
payana_profile_table_user_name = bigtable_constants.payana_profile_table_user_name
payana_profile_table_blog_url = bigtable_constants.payana_profile_table_blog_url
payana_profile_table_profile_description = bigtable_constants.payana_profile_table_profile_description
payana_profile_table_profile_id = bigtable_constants.payana_profile_table_profile_id
payana_profile_table_email = bigtable_constants.payana_profile_table_email
payana_profile_table_phone = bigtable_constants.payana_profile_table_phone
payana_profile_table_private_account = bigtable_constants.payana_profile_table_private_account
payana_profile_table_gender = bigtable_constants.payana_profile_table_gender
payana_profile_table_date_of_birth = bigtable_constants.payana_profile_table_date_of_birth
payana_profile_table_doj = bigtable_constants.payana_profile_table_doj

payana_profile_table_personal_info_column_family = bigtable_constants.payana_profile_table_personal_info_column_family
payana_profile_table_top_activities_tracker_rating = bigtable_constants.payana_profile_table_top_activities_tracker_rating
payana_profile_favorite_places_preference = bigtable_constants.payana_profile_favorite_places_preference
payana_profile_favorite_activities_preference = bigtable_constants.payana_profile_favorite_activities_preference
payana_profile_table_thumbnail_travel_buddies = bigtable_constants.payana_profile_table_thumbnail_travel_buddies


profile_table_personal_information_schema = {payana_profile_table_profile_name: fields.String(required=True,
                                                                                              description="Name of the profile/person",
                                                                                              help="Profile Name cannot be blank."),
                                             payana_profile_table_user_name: fields.String(required=True,
                                                                                           description="User ID/Name of the person for the app",
                                                                                           help="User ID/Name cannot be blank."),
                                             payana_profile_table_blog_url: fields.String(required=False,
                                                                                          description="Blogging URL",
                                                                                          help=""),
                                             payana_profile_table_profile_description: fields.String(required=False,
                                                                                                     description="A small profile description",
                                                                                                     help=""),
                                             payana_profile_table_profile_id: fields.String(required=False,
                                                                                            description="App generated unique identifier",
                                                                                            help=""),
                                             payana_profile_table_email: fields.String(required=True,
                                                                                       description="Email of the person",
                                                                                       help="Email cannot be blank."),
                                             payana_profile_table_phone: fields.String(required=False,
                                                                                       description="Phone Number",
                                                                                       help=""),
                                             payana_profile_table_private_account: fields.String(required=True,
                                                                                                 description="Private/Public account flag of the person",
                                                                                                 help="Private/Public account flag cannot be blank."),
                                             payana_profile_table_gender: fields.String(required=False,
                                                                                        description="Gender",
                                                                                        help=""),
                                             payana_profile_table_date_of_birth: fields.String(required=True,
                                                                                               description="Date of Birth",
                                                                                               help="Date of Birth cannot be blank."),
                                             payana_profile_table_doj: fields.String(required=True,
                                                                                     description="Date of joining",
                                                                                     help="Date of joining cannot be blank.")}

profile_table_personal_information_schema = {payana_profile_table_profile_name: fields.String(required=True,
                                                                                              description="Name of the profile/person",
                                                                                              help="Profile Name cannot be blank."),
                                             payana_profile_table_user_name: fields.String(required=True,
                                                                                           description="User ID/Name of the person for the app",
                                                                                           help="User ID/Name cannot be blank."),
                                             payana_profile_table_blog_url: fields.String(required=False,
                                                                                          description="Blogging URL",
                                                                                          help=""),
                                             payana_profile_table_profile_description: fields.String(required=False,
                                                                                                     description="A small profile description",
                                                                                                     help=""),
                                             payana_profile_table_profile_id: fields.String(required=False,
                                                                                            description="App generated unique identifier",
                                                                                            help="")}


profile_table_model_schema = {

}
