#!/usr/bin/env python

"""Demonstrates how to fetch an API key for Google Places autocomplete API
"""

from payana.payana_bl.autocomplete_utils.fetch_autocomplete_api_key import fetch_autocomplete_api_key

print(fetch_autocomplete_api_key("android"))
print(fetch_autocomplete_api_key("darwin"))
print(fetch_autocomplete_api_key("web"))
print(fetch_autocomplete_api_key("ghf"))
