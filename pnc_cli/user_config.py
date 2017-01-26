import atexit
import json
import logging
import os
import pickle

import iniparse.configparser as configparser
import requests
import swagger_client

import pnc_cli.utils as utils
import keycloak_config as kc
import pnc_server_config as psc

SAVED_USER_FILENAME = "saved-user.p"
SAVED_USER = utils.CONFIG_LOCATION + SAVED_USER_FILENAME


class UserConfig():
    def __init__(self):
        config = utils.get_config()
        self.pnc_config = psc.PncServerConfig(config)
        self.keycloak_config = kc.KeycloakConfig(config)
        self.parse_username(config)
        self.parse_password(config)
        self.retrieve_keycloak_token()
        self.create_api_client()

    def parse_username(self, config):
        try:
            username = config.get('PNC', 'username')
        except configparser.NoOptionError:
            logging.error('Username missing. Define "username" in pnc-cli.conf for authentication.')
            return
        self.username = username

    def parse_password(self, config):
        try:
            password = config.get('PNC', 'password')
        except configparser.NoOptionError:
            logging.error('Username missing. Define "username" in pnc-cli.conf for authentication.')
            return
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def retrieve_keycloak_token(self):
        params = {'grant_type': 'password',
                  'client_id': self.keycloak_config.client_id,
                  'username': self.username,
                  'password': self.password}
        r = requests.post(self.keycloak_config.url, params, verify=False)
        if r.status_code == 200:
            reply = json.loads(r.content.decode('utf-8'))
            self.token = str(reply.get('access_token'))
        else:
            self.token = None


    def create_api_client(self):
        # add time check for the token setting
        # if token has expired
        self.retrieve_keycloak_token()
        self.apiclient = swagger_client.ApiClient(self.pnc_config.url, header_name='Authorization',
                                                  header_value='Bearer ' + self.token)
        # else return the apiclient, since nothing has changed
        # if the token is None, create a client without auth
        # self.apiclient = swagger_client.ApiClient(self.pnc_config.url)

    def get_api_client(self):
        return self.apiclient


if os.path.exists(SAVED_USER):
    user = pickle.load(open(SAVED_USER, "r"), protocol=pickle.HIGHEST_PROTOCOL)
else:
    user = UserConfig()

def save_user():
    # do pickle stuff
    pickle.dump(user, open(SAVED_USER, "w"), protocol=pickle.HIGHEST_PROTOCOL)

atexit.register(save_user)

