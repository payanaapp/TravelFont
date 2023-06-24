#!/usr/bin/env python

"""Contains big table write utils - status handler functions for bigtable write objects for example
"""
from payana.payana_core.common_utils.payana_core_exception_handler_utils import payana_boolean_exception_handler

@payana_boolean_exception_handler
def payana_bigtable_write_status_handler(table_mutate_response):
    
    for response in table_mutate_response:
        
        if response.code != 0: # 0 is success -- 200
            return False
        
    return True

@payana_boolean_exception_handler
def payana_bigtable_delete_status_handler(response):
            
    if response.code != 0: # 0 is success -- 200
        return False
    
    return True
