from google.cloud import bigquery
from google.api_core.exceptions import AlreadyExists, Conflict, NotFound


def create_bigquery_dataset(project_id, dataset_id):

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to create.
    dataset_id_full_path = "{}.{}".format(project_id, dataset_id)

    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id_full_path)

    # TODO(developer): Specify the geographic location where the dataset should reside.
    dataset.location = "US"

    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    try:
        # Make an API request.
        if not dataset_exists(project_id, dataset_id):
            dataset = client.create_dataset(dataset, timeout=30)
    except Conflict:
        print("Dataset {}.{} already exists".format(
            client.project, dataset.dataset_id))

    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

    del client


def list_datasets(project_id):
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project_id)

    datasets = list(client.list_datasets())  # Make an API request.

    if datasets:
        print("Datasets in project {}:".format(project_id))
        for dataset in datasets:
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project_id))

    del client


def dataset_exists(project_id, dataset_id):

    client = bigquery.Client()

    # TODO(developer): Set dataset_id to the ID of the dataset to determine existence.
    dataset_id = "{}.{}".format(project_id, dataset_id)

    try:
        client.get_dataset(dataset_id)  # Make an API request.
        print("Dataset {} already exists".format(dataset_id))
        return True
    except NotFound:
        print("Dataset {} is not found".format(dataset_id))
        return False
    # [END bigquery_dataset_exists]


def get_dataset(project_id, dataset_id):
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project_id)

    dataset = client.get_dataset(dataset_id)  # Make an API request.

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)

    print(
        "Got dataset '{}'.".format(
            full_dataset_id
        )
    )

    del client


def delete_dataset(dataset_id):
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project_id)

    client.delete_dataset(
        dataset_id, delete_contents=True, not_found_ok=True
    )

    print("Deleted dataset '{}'.".format(dataset_id))

    del client


def update_dataset(dataset_id, new_description):
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project_id)

    dataset = client.get_dataset(dataset_id)
    dataset.description = new_description
    dataset = client.update_dataset(dataset, ["description"])

    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    print(
        "Updated dataset '{}' with description '{}'.".format(
            full_dataset_id, dataset.description
        )
    )

    del client


def create_bigquery_table(project_id, dataset_id, table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id_full_path = "{}.{}.{}".format(project_id, dataset_id, table_id)

    schema = [
        bigquery.SchemaField("suggestion", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("frequency", "INTEGER", mode="REQUIRED"),
    ]

    table_id_full_path = bigquery.Table.from_string(table_id_full_path)

    table = bigquery.Table(table_id_full_path, schema=schema)

    try:
        if not table_exists(project_id, dataset_id, table_id):
            table = client.create_table(table)  # Make an API request.
    except Conflict:
        print("Table {}.{}.{} already exists".format(
            table.project, table.dataset_id, table.table_id))

    print(
        "Created table {}.{}.{}".format(
            table.project, table.dataset_id, table.table_id)
    )

    del client


def insert_rows(project_id, dataset_id, table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client(project_id)

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = "{}.{}.{}".format(project_id, dataset_id, table_id)

    rows_to_insert = [
        {"suggestion": "BHAR", "frequency": 31},
        {"suggestion": "RAHB", "frequency": 32}
    ]

    # Make an API request.
    errors = client.insert_rows_json(table_id, rows_to_insert)

    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

    del client


def list_tables(project_id, dataset_id):
    # Construct a BigQuery client object.
    client = bigquery.Client(project_id)
    tables = client.list_tables(dataset_id)

    print("Tables contained in '{}':".format(dataset_id))
    for table in tables:
        print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))

    del client


def table_exists(project_id, dataset_id, table_id):

    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to determine existence.
    table_id = "{}.{}.{}".format(project_id, dataset_id, table_id)

    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
        return True
    except NotFound:
        print("Table {} is not found.".format(table_id))
        return False
    # [END bigquery_table_exists]


def get_table(project_id, dataset_id, table_id):

    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to determine existence.
    table_id = "{}.{}.{}".format(project_id, dataset_id, table_id)

    table = client.get_table(table_id)  # Make an API request.

    # View table properties
    print(
        "Got table '{}.{}.{}'.".format(
            table.project, table.dataset_id, table.table_id)
    )
    print("Table schema: {}".format(table.schema))
    print("Table description: {}".format(table.description))
    print("Table has {} rows".format(table.num_rows))
    # [END bigquery_get_table]


def delete_bigquery_table(project_id, dataset_id, table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    table_id = "{}.{}.{}".format(project_id, dataset_id, table_id)

    table_id = bigquery.Table.from_string(table_id)

    try:
        client.delete_table(table_id, not_found_ok=True)
    except NotFound:
        print("Table not found")

    table_id_name = "{}.{}.{}".format(project_id, dataset_id, table_id)
    print("Deleted table '{}'.".format(table_id_name))

    del client


def query_table(project_id, dataset_id, table_id):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "{}.{}.{}".format(project_id, dataset_id, table_id)

    QUERY = (
        "SELECT * FROM {}".format(table_id)
    )
    query_job = client.query(QUERY)
    rows = query_job.result()
    for row in rows:
        print(row.suggestion)
        print(row.frequency)

    del client


project_id = "project-payana-354422"
dataset_id = "dataset_payana_bq_test"
table_id = "table_payana_bq_test"

if __name__ == "__main__":

    create_bigquery_dataset(project_id, dataset_id)
    list_datasets(project_id)
    get_dataset(project_id, dataset_id)
    update_dataset(dataset_id, new_description="new_description")
    dataset_exists(project_id, dataset_id)

    create_bigquery_table(project_id, dataset_id, table_id)
    table_exists(project_id, dataset_id, table_id)
    get_table(project_id, dataset_id, table_id)
    list_tables(project_id, dataset_id)
    insert_rows(project_id, dataset_id, table_id)
    query_table(project_id, dataset_id, table_id)
    delete_bigquery_table(project_id, dataset_id, table_id)

    delete_dataset(dataset_id)
