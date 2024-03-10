#!/usr/bin/env python

"""Demonstrates how to fetch an API key for Google Places autocomplete API
"""

import argparse

from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler
from payana.payana_bl.autocomplete_utils.constants.PlatformEnums import PlatformEnums
from payana.payana_core.autocomplete_utils.payana_autocomplete_api_key_fetch import payana_autocomplete_api_key_android, payana_autocomplete_api_key_ios, payana_autocomplete_api_key_web


@payana_generic_exception_handler
def fetch_autocomplete_api_key(platform):

    print(__name__)

    # fetches autocomplete api key

    if platform == PlatformEnums.Android:
        return payana_autocomplete_api_key_android()
    elif platform == PlatformEnums.Web:
        return payana_autocomplete_api_key_web()
    elif platform == PlatformEnums.ios:
        return payana_autocomplete_api_key_ios()
    else:
        return None


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'platform', help='Platform specification key. Android or ios or web')

    args = parser.parse_args()

    fetch_autocomplete_api_key(args.platform)
