import json
from collections import namedtuple
from json import JSONEncoder
from payana.payana_bl.common_utils.payana_exception_handler_utils import payana_generic_exception_handler


class PayanaJSONEncoder(JSONEncoder):

    @payana_generic_exception_handler
    def default(self, o):
        return o.__dict__
