#!/usr/bin/env python

"""Demonstrates how to fetch an API key for Google Places autocomplete API
"""

import argparse

from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler
from payana.payana_core.autocomplete_utils.constants import autocomplete_api_key_constants


@payana_generic_exception_handler
def payana_autocomplete_api_key_android():

    # read the apikey from the file
    android_api_key_file_path = autocomplete_api_key_constants.autocomplete_android_api_key_config_file
    return payana_autocomplete_api_key_read(android_api_key_file_path)


@payana_generic_exception_handler
def payana_autocomplete_api_key_web():

    # read the apikey from the file
    web_api_key_file_path = autocomplete_api_key_constants.autocomplete_web_api_key_config_file
    return payana_autocomplete_api_key_read(web_api_key_file_path)


@payana_generic_exception_handler
def payana_autocomplete_api_key_ios():

    # read the apikey from the file
    ios_api_key_file_path = autocomplete_api_key_constants.autocomplete_ios_api_key_config_file
    return payana_autocomplete_api_key_read(ios_api_key_file_path)


@payana_generic_exception_handler
def payana_autocomplete_api_key_read(api_key_filename):

    # read the apikey from the file
    with open(api_key_filename, 'r') as api_key_file:
        api_key = api_key_file.read()
        return api_key

    return None


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()
    parser.add_argument('api_key_file',
                        help='Your api key autocomplete config file.')

    args = parser.parse_args()
    payana_autocomplete_api_key_read(args.api_key_file)
