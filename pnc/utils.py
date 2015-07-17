import json
import client.swagger

__author__ = 'thauser'

base_pnc_url = "http://localhost:8080/pnc-rest/rest"
apiclient = client.swagger.ApiClient(base_pnc_url)


def _remove_nulls(input_json):
    keys = input_json.keys()
    if keys:
        for k in keys:
            if input_json[k] is None:
                del input_json[k]


def pretty_format_response(function, input_json):
    """
    prints the json dump in a more readable format.
    does not print null values
    :param input_json:
    :return:
    """
    if function is None:
        return pretty_format_response(input_json)
    else:
        return function(input_json)


def pretty_format_response(input_json):
    if type(input_json) is list:
        for item in input_json:
            _remove_nulls(item)
    else:
        _remove_nulls(input_json)
    return json.dumps(input_json, indent=4, separators=[",", ": "], sort_keys=True)

def get_api_client():
    return apiclient