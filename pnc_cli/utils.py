import json
import requests
import sys

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import re
import errno
import os

from pnc_cli import swagger_client
from pnc_cli.swagger_client.rest import ApiException

__author__ = 'thauser'


def get_auth_token(config):
    try:
        server = config.get('PNC', 'authServer')
    except configparser.NoOptionError:
        print('No authentication server defined. Define "authServer" in pnc-cli.conf to enable authentication.')
        return
    server = server + "/auth/realms/pncredhat/tokens/grants/access"
    try:
        username = config.get('PNC', 'username')
        password = config.get('PNC', 'password')
    except configparser.NoOptionError:
        print('Username / password missing. Define "username" and "password" in pnc-cli.conf for authentication.')
        return

    params = {'grant_type': 'password',
              'client_id': 'pncdirect',
              'username': username,
              'password': password}
    r = requests.post(server, params, verify=False)
    if r.status_code == 200:
        reply = json.loads(r.content.decode('utf-8'))
        return str(reply.get('access_token'))


config = configparser.ConfigParser()
configfilename = os.path.expanduser("~") + "/.config/pnc-cli/pnc-cli.conf"
configdirname = os.path.dirname(configfilename)

try:
    os.makedirs(configdirname)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
found = config.read(os.path.join(configfilename))
if not found:
    config.add_section('PNC')
    config.set('PNC', 'restEndpoint', 'http://localhost:8080/pnc-rest/rest/')
    # prompt user for his keycloak username / passwords
    username = input('Username: ')
    password = input('Password: ')
    config.set('PNC', 'username', username)
    config.set('PNC', 'password', password)
    with open(os.path.join(configfilename), 'w') as configfile:
        config.write(configfile)
pnc_rest_url = config.get('PNC', 'restEndpoint').rstrip('/')
authtoken = get_auth_token(config)
if authtoken:
    apiclient = swagger_client.ApiClient(pnc_rest_url, header_name='Authorization',
                                         header_value="Bearer " + authtoken)
else:
    print('Authentication failed. Some operations will be unavailable.')
    apiclient = swagger_client.ApiClient(pnc_rest_url)

def get_api_client():
    return apiclient


def is_valid_version(version):
    pattern = re.compile('\d*\.\w*')
    return pattern.match(version)


def checked_api_call(api, func, **kwargs):
    try:
        response = getattr(api, func)(**kwargs)
    except ApiException as e:
        print(e)
    else:
        return response
