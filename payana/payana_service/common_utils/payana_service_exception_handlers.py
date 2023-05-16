#!/usr/bin/env python

"""Contains decorator functions for exception handlers
"""
from payana.payana_service.constants import payana_service_constants

payana_200_response = payana_service_constants.payana_200_response
payana_201_response = payana_service_constants.payana_201_response
payana_400_response = payana_service_constants.payana_400_response
payana_500_response = payana_service_constants.payana_500_response

payana_200 = payana_service_constants.payana_200
payana_201 = payana_service_constants.payana_201
payana_400 = payana_service_constants.payana_400
payana_500 = payana_service_constants.payana_500

def payana_service_intermediate_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, KeyError) as attr_exc:
            attr_exc_message = f"{func.__name__} : " + str(attr_exc)
            print(attr_exc_message)
            raise Exception(str(attr_exc))
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            raise Exception(str(exc_message))       

    return inner_function

def payana_service_generic_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, KeyError) as exc:
            exc_message, name_space = exc.args
            exc_log_message = f"{func.__name__} : " + str(exc_message)
            print(exc_log_message)
            
            name_space.abort(
                400, exc_message, status=payana_400_response, statusCode="400")
            
        except Exception as exc:
            exc_log_message = f"{func.__name__} : " + str(exc)
            print(exc_log_message)
            
            return {'message': str(exc)}, payana_500        

    return inner_function