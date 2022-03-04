from flask_restx import fields
from payana.payana_bl.bigtable_utils.constants import bigtable_constants

profile_name = bigtable_constants.payana_profile_table_profile_name
user_name = bigtable_constants.payana_profile_table_user_name
blog_url = bigtable_constants.payana_profile_table_blog_url
profile_description = bigtable_constants.payana_profile_table_profile_description
profile_id = bigtable_constants.payana_profile_table_profile_id
email = bigtable_constants.payana_profile_table_email
phone = bigtable_constants.payana_profile_table_phone
private_account = bigtable_constants.payana_profile_table_private_account
gender = bigtable_constants.payana_profile_table_gender
date_of_birth = bigtable_constants.payana_profile_table_date_of_birth

profile_table_model_schema = {profile_name: fields.String(required=True,
                                                          description="Name of the profile/person",
                                                          help="Profile Name cannot be blank."),
                              user_name: fields.String(required=True,
                                                       description="User ID/Name of the person for the app",
                                                       help="User ID/Name cannot be blank."),
                              blog_url: fields.String(required=False,
                                                      description="Blogging URL",
                                                      help=""),
                              profile_description: fields.String(required=False,
                                                                 description="A small profile description",
                                                                 help=""),
                              profile_id: fields.String(required=False,
                                                        description="App generated unique identifier",
                                                        help=""),
                              email: fields.String(required=True,
                                                   description="Email of the person",
                                                   help="Email cannot be blank."),
                              phone: fields.String(required=False,
                                                   description="Phone Number",
                                                   help=""),
                              private_account: fields.String(required=True,
                                                             description="Private/Public account flag of the person",
                                                             help="Private/Public account flag cannot be blank."),
                              gender: fields.String(required=False,
                                                    description="Gender",
                                                    help=""),
                              date_of_birth: fields.String(required=True,
                                                           description="Date of Birth",
                                                           help="Date of Birth cannot be blank.")}
