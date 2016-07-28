import getpass
import json
import logging

import requests

requests.packages.urllib3.disable_warnings()

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import re
import errno
import os
import datetime

try:
    input = raw_input
except NameError:
    pass

from pnc_cli import swagger_client
from pnc_cli.swagger_client.rest import ApiException

__author__ = 'thauser'


def get_auth_token(config):
    try:
        server = config.get('PNC', 'keycloakUrl')
        if server is None:
            raise configparser.NoOptionError
    except configparser.NoOptionError:
        logging.error(
            'No authentication server defined. Define "keycloakUrl" in pnc-cli.conf to enable authentication.')
        return
    try:
        realm = config.get('PNC', 'keycloakRealm')
    except configparser.NoOptionError:
        logging.error(
            'No keycloak authentication realm defined. Define "keycloakRealm" in pnc-cli.conf to enable authentication.')
        return
    server = server + "/auth/realms/" + realm + "/protocol/openid-connect/token"
    try:
        username = config.get('PNC', 'username')
        password = config.get('PNC', 'password')
    except configparser.NoOptionError:
        logging.error(
            'Username / password missing. Define "username" and "password" in pnc-cli.conf for authentication.')
        return

    try:
        client_id = config.get('PNC', 'keycloakClientId')
    except configparser.NoOptionError:
        logging.error(
            'client_id is missing for the keycloak payload. Define "keycloakClientId" in pnc-cli.conf for authentication.')
        return

    params = {'grant_type': 'password',
              'client_id': client_id,
              'username': username,
              'password': password}
    r = requests.post(server, params, verify=False)
    if r.status_code == 200:
        reply = json.loads(r.content.decode('utf-8'))
        return str(reply.get('access_token'))


config = configparser.ConfigParser(allow_no_value=False)
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
    config.set('PNC', 'pncUrl', 'http://localhost:8080/')
    # prompt user for his keycloak username / passwords
    config.set('PNC', 'keycloakUrl', '')
    config.set('PNC', 'keycloakRealm', 'pncredhat')
    config.set('PNC', 'keycloakClientId', 'pncdirect')
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    config.set('PNC', 'username', username)
    config.set('PNC', 'password', password)
    with open(os.path.join(configfilename), 'w') as configfile:
        config.write(configfile)
    logging.warning(
        "New config file written to ~/.config/pnc-cli/pnc-cli.conf. Configure pncUrl and keycloakUrl values.")
    exit(0)
global authtoken
authtoken = get_auth_token(config)


def get_api_client():
    pnc_rest_url = config.get('PNC', 'pncUrl').rstrip('/') + '/pnc-rest/rest'
    if authtoken:
        apiclient = swagger_client.ApiClient(pnc_rest_url, header_name='Authorization',
                                             header_value="Bearer " + authtoken)
    else:
        logging.warning('Authentication failed. Some operations will be unavailable.')
        apiclient = swagger_client.ApiClient(pnc_rest_url)
    return apiclient


def is_valid_version(version, regex):
    if version is not None:
        pattern = re.compile(regex)
        return pattern.match(version)


def checked_api_call(api, func, **kwargs):
    try:
        response = getattr(api, func)(**kwargs)
    except ApiException as e:
        print(e)
    else:
        return response


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    millis = int((dt - epoch).total_seconds() * 1000.0)
    return millis


def contains_only_none_values(dictionary):
    for key in dictionary.keys():
        if dictionary[key] is not None:
            return False
    return True
