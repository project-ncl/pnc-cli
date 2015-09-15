import ConfigParser
import random
import string
import re
import errno
import swagger_client
import os

__author__ = 'thauser'

config = ConfigParser.ConfigParser()
configfile = os.path.expanduser("~")+"/.config/pnc-cli/pnc-cli.conf"
configdir = os.path.dirname(configfile)
try:
    os.makedirs(configdir)
except OSError, e:
    if e.errno != errno.EEXIST:
        raise
found = config.read(os.path.join(configfile))
if not found:
    config.add_section('PNC')
    config.set('PNC', 'restEndpoint', 'http://localhost:8080/pnc-rest/rest')
    with open(os.path.join(configfile),'wb') as configfile:
        config.write(configfile)
pnc_rest_url = config.get('PNC', 'restEndpoint')
apiclient = swagger_client.api_client.ApiClient(pnc_rest_url)

def get_api_client():
    return apiclient

def is_valid_version(version):
    pattern = re.compile('\d*\.\w*')
    return pattern.match(version)
