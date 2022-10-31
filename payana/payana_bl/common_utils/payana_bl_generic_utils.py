#!/usr/bin/env python

"""Contains core generic write utils
"""
import argparse
import random
import json
import time
import hashlib

from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_generic_exception_handler

@payana_generic_exception_handler
def payana_generate_id(id_terms):
    
    current_timestamp_unix = str(time.time())
    
    id_terms.append(current_timestamp_unix)

    random.shuffle(id_terms)

    checkin_id_hash = "".join(id_terms)

    checkin_id_binary = hashlib.sha256(checkin_id_hash.encode())

    return checkin_id_binary.hexdigest()
