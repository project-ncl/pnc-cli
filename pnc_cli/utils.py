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
import time

try:
    input = raw_input
except NameError:
    pass

from pnc_cli.swagger_client.rest import ApiException

__author__ = 'thauser'

envconfig = os.environ.get('PNC_CONFIG_LOCATION')
if envconfig is not None:
    if not envconfig.endswith("/"):
        envconfig += "/"
    CONFIG_LOCATION = envconfig
else:
    CONFIG_LOCATION = os.path.expanduser("~") + "/.config/pnc-cli/"
CONFIG_FILENAME = "pnc-cli.conf"
CONFIG = CONFIG_LOCATION + CONFIG_FILENAME


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


def format_json_list(page_model):
    if page_model is not None:
        json_list = []
        for element in page_model:
            json_list.append(format_json(element))
        return "[" + ",".join(json_list) + "]"
    else:
        return None


def format_json(rest_model):
    return json.dumps(rest_model.to_dict(), sort_keys=True, indent=4, separators=(',', ': '))

def format_dict(rest_model):
    return json.dumps(rest_model, sort_keys=True, indent=4, separators=(',', ': '))



epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    millis = int((dt - epoch).total_seconds() * 1000.0)
    return millis


def current_time_millis():
    millis = int(round(time.time() * 1000))
    return millis


def contains_only_none_values(dictionary):
    for key in dictionary.keys():
        if dictionary[key] is not None:
            return False
    return True


def get_config():
    config = configparser.ConfigParser(allow_no_value=False)
    configparser.ConfigParser(allow_no_value=False)
    configfilename = CONFIG
    configdirname = CONFIG_LOCATION

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
        config.set('PNC', 'username', username)
        with open(os.path.join(configfilename), 'w') as configfile:
            config.write(configfile)
        logging.warning("New config file written to %s. Configure pncUrl and keycloakUrl values." % configfilename)
        exit(1)
    return config


def get_internal_repo_start(environment):
    ### Devel urls ###
    # http://pnc-orch-master-autodeploy.cloud.pnc.devel.engineering.redhat.com/
    # http://pnc-orch-branch-autodeploy.cloud.pnc.devel.engineering.redhat.com/
    ### Stage URLS ###
    # http://pnc-orch-branch-nightly.cloud.pnc.stage.engineering.redhat.com/
    # http://pnc-orch-branch-autodeploy.cloud.pnc.stage.engineering.redhat.com/
    if "stage" in environment:
        return 'git+ssh://pnc-gerrit-stage@code-stage.eng.nay.redhat.com:29418/'
    elif "devel" in environment:
        return 'git+ssh://user-pnc-gerrit@pnc-gerrit.pnc.dev.eng.bos.redhat.com:29418/'
