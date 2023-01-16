#!/usr/bin/env python

"""Contains decorator functions for exception handlers
"""


def payana_generic_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            raise exc
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            raise exc

    return inner_function

def payana_boolean_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as attr_exc:
            attr_exc_message = f"{func.__name__} : " + str(attr_exc)
            print(attr_exc_message)
            # raise AttributeError(attr_exc_message)
            return False
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            # raise Exception(exc_message)
            return False

    return inner_function