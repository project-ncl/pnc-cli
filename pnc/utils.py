import ConfigParser
import json
import client.swagger

__author__ = 'thauser'


config = ConfigParser.ConfigParser()
config.read("pnc-cli.conf")
base_pnc_url = config.get('PNC','restEndpoint')
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

def retrieve_keys(input_json, keys):
    if type(input_json) is list:
        final_dict = [{key : r[key] for key in keys} for r in input_json]
    else:
        final_dict = {key : input_json[key] for key in keys}
    return final_dict

def get_api_client():
    return apiclient