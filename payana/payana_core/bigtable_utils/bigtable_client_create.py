#!/usr/bin/env python

"""Demonstrates how to connect to Cloud Bigtable instance

Documentation:

- Create a Cloud Bigtable cluster.
  https://cloud.google.com/bigtable/docs/creating-cluster
"""
import yaml
import argparse

from google.cloud.bigtable import Client
from google.cloud.bigtable import enums
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.bigtable_utils.constants import bigtable_constants


@payana_generic_exception_handler
def bigtable_client_create(cluster_config_file):
    # [START bigtable_client_create]

    # read config file for cluster
    with open(cluster_config_file, "r") as ymlfile:
        cluster_config = yaml.safe_load(ymlfile)

    instance_id = cluster_config[bigtable_constants.bigtable_instance_id]
    cluster_id = cluster_config[bigtable_constants.bigtable_cluster_id]
    location_id = cluster_config[bigtable_constants.bigtable_location_id]
    serve_nodes = cluster_config[bigtable_constants.bigtable_serve_nodes]
    production_flag = cluster_config[bigtable_constants.bigtable_production_flag]
    storage_type = bigtable_constants.bigtable_storage_type
    production = bigtable_constants.bigtable_production

    labels = {bigtable_constants.bigtable_prod_label:
              cluster_config[bigtable_constants.bigtable_labels][bigtable_constants.bigtable_prod_label]}

    client = Client(admin=True)

    if production_flag:
        instance = client.instance(
            instance_id, instance_type=production, labels=labels)
    else:
        instance = client.instance(instance_id)

    cluster = instance.cluster(
        cluster_id,
        location_id=location_id,
        serve_nodes=serve_nodes,
        default_storage_type=storage_type,
    )

    if not cluster.exists():
        operation = instance.create(clusters=[cluster])

        # We want to make sure the operation completes.
        operation.result(timeout=150)
        print("BigTable client created.")
    else:
        print("cluster exists")

    # [END bigtable_client_create]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('cluster_config_file',
                        help='Your BigTable cluster config file.')

    args = parser.parse_args()
    bigtable_client_create(args.cluster_config_file)
