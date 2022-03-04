#!/usr/bin/env python

"""Contains decorator functions for exception handlers
"""

def payana_service_generic_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AttributeError, KeyError) as attr_exc:
            attr_exc_message = f"{func.__name__} : " + str(attr_exc)
            print(attr_exc_message)
            return {'message': str(attr_exc)}, getattr(attr_exc, 'code', 400)
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            return {'message': str(exc)}, getattr(exc, 'code', 500)          

    return inner_function
