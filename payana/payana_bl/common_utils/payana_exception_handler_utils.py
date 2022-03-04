#!/usr/bin/env python

"""Contains decorator functions for exception handlers
"""


def payana_generic_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as attr_exc:
            attr_exc_message = f"{func.__name__} : " + str(attr_exc)
            print(attr_exc_message)
            raise Exception(attr_exc_message)
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            raise Exception(exc_message)
            

    return inner_function

def payana_none_exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as attr_exc:
            attr_exc_message = f"{func.__name__} : " + str(attr_exc)
            print(attr_exc_message)
            raise Exception(attr_exc_message)
        except TypeError as type_exc:
            type_exc_message = f"{func.__name__} : " + str(type_exc)
            print(type_exc_message)
            raise Exception(type_exc_message)
        except Exception as exc:
            exc_message = f"{func.__name__} : " + str(exc)
            print(exc_message)
            raise Exception(exc_message)
            

    return inner_function