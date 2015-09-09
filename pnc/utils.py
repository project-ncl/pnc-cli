import ConfigParser
import random
import string
import swagger_client
import os

__author__ = 'thauser'

config = ConfigParser.ConfigParser()
configfilename = os.path.expanduser("~")+ "/.config/pnc-cli/pnc-cli.conf"
found = config.read(os.path.join(configfilename))
if not found:
    config.add_section('PNC')
    config.set('PNC', 'restEndpoint', 'http://localhost:8080/pnc-rest/rest')
    with open(os.path.join(configfilename),'wb') as configfile:
        config.write(configfile)
pnc_rest_url = config.get('PNC', 'restEndpoint')
apiclient = swagger_client.api_client.ApiClient(pnc_rest_url)

def get_api_client():
    return apiclient

def gen_random_name():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))