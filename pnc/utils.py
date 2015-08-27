import ConfigParser
import json
import client.swagger
import os

__author__ = 'thauser'


config = ConfigParser.ConfigParser()
configfilename = os.path.expanduser("~")+ "/.config/pnc-cli/pnc-cli.conf"
found = config.read(os.path.join(configfilename))
if not found:
    print('wat')
    config.add_section('PNC')
    config.set('PNC', 'restEndpoint', 'http://localhost:8080/pnc-rest/rest')
    with open(os.path.join(configfilename),'wb') as configfile:
        config.write(configfile)
base_pnc_url = config.get('PNC', 'restEndpoint')
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

def print_matching_attribute(json, attributes, valid_attributes):
    attr_list = attributes.split(",")
    for a in attr_list:
        if a not in valid_attributes:
            print("Invalid attribute. Choose from the following list:")
            print('\n'.join(key for key in valid_attributes))
            return
    result = retrieve_keys(json, attr_list)
    print('\n'.join(str(r[attr]) for r in result for attr in attr_list))


def print_by_key(json):
    """
    print json objects in the form "key: dict[key]" on each line for each key
    :param json:
    :return:
    """
    if type(json) is list:
        for item in json:
            print('\n'.join(key + ": " + str(item[key]) for key in item.keys()))
            print('\n')
    else:
        print('\n'.join(key + ": " + str(json[key]) for key in json.keys()))
        print('\n')

def retrieve_keys(input_json, keys):
    if type(input_json) is list:
        final_dict = [{key : r[key] for key in keys} for r in input_json]
    else:
        final_dict = {key : input_json[key] for key in keys}
    return final_dict

def print_error(func_name, reason):
    print(func_name + " failed: " + str(reason))


def get_api_client():
    return apiclient

