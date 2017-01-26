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
        self.token_time = 0
        self.username = ""
        self.password = ""
        self.token = None
        self.apiclient = None
        self.pnc_config = psc.PncServerConfig(config)
        self.keycloak_config = kc.KeycloakConfig(config)
        self.parse_username(config)
        self.parse_password(config)
        self.token = self.retrieve_keycloak_token()
        self.token_time = utils.current_time_millis()
        self.apiclient = self.create_api_client()

    def __getstate__(self):
        return (self.keycloak_config, self.username, self.password, self.token, self.token_time)

    def __setstate__(self, state):
        # here we need to read the config file again, to check that values for URLs haven't changed. the way to
        # change the username / password will be a login function the user calls. ideally the config file won't need
        # to be changed much once it's in place
        newtoken = False
        config = utils.get_config()
        saved_kc_config, self.username, self.password, self.token, self.token_time = state
        self.pnc_config = psc.PncServerConfig(config)

        # check for changes in keycloak configuration; if so, we'll need to get a new token regardless of time
        current_keycloak_config = kc.KeycloakConfig(config)
        if not current_keycloak_config == saved_kc_config:
            self.keycloak_config = current_keycloak_config
            newtoken = True
        # if more than a day has passed since we saved the token, or if the urls have changed, get a new one
        if utils.current_time_millis() - self.token_time > 86400000:
            newtoken = True

        if newtoken:
            self.token = self.retrieve_keycloak_token()

        self.apiclient = self.create_api_client()

    # this function gets input from the user to set the username
    def parse_username(self, config):
        try:
            username = config.get('PNC', 'username')
        except configparser.NoOptionError:
            logging.error('Username missing. Define "username" in pnc-cli.conf for authentication.')
            return
        self.username = username

    # this function gets input from the user to set the password
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
            return str(reply.get('access_token'))



    def create_api_client(self):
        # add time check for the token setting
        # if token has expired
        return swagger_client.ApiClient(self.pnc_config.url, header_name='Authorization',
                                                  header_value='Bearer ' + self.token)
        # if the token is None, create a client without auth
        # self.apiclient = swagger_client.ApiClient(self.pnc_config.url)

    def get_api_client(self):
        return self.apiclient


if os.path.exists(SAVED_USER):
    user = pickle.load(open(SAVED_USER, "r"))
else:
    user = UserConfig()

def save():
        # do pickle stuff
        pickle.dump(user, open(SAVED_USER, "w"), protocol=pickle.HIGHEST_PROTOCOL)

atexit.register(save)

