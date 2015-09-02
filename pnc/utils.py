import ConfigParser
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
pnc_rest_url = config.get('PNC', 'restEndpoint')
apiclient = client.swagger.ApiClient(pnc_rest_url)

def print_json_result(caller, response, attributes=None, valid_attributes=None):
    if not response.ok:
        print_error(caller, response)
        return
    if attributes:
        print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        print_by_key(response.json())

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
            print('\n'.join(key + ": " + str(item[key]) for key in item.keys()))+"\n"
    else:
        print('\n'.join(key + ": " + str(json[key]) for key in json.keys()))+'\n'

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

