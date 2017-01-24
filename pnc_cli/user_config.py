import json
import logging

import iniparse.configparser as configparser
import requests
import swagger_client

import pnc_cli.utils as utils
import keycloak_config as kc
import pnc_server_config as psc


class UserConfig():
    def __init__(self):
        config = utils.get_config()
        self.pnc_config = kc.PncServerConfig(config)
        self.keycloak_config = psc.keycloak_config.KeycloakConfig(config)
        self.parse_username(config)
        self.parse_password(config)

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
        self.token = None


    def set_api_client(self):
        # add time check for the token setting
        # if token has expired
        self.get_keycloak_token()
        self.apiclient = swagger_client.ApiClient(self.pnc_config.url, header_name='Authorization',
                                             header_value='Bearer ' + self.token)
        # else return the apiclient, since nothing has changed
        # if the token is None, create a client without auth
        # self.apiclient = swagger_client.ApiClient(self.pnc_config.url)


obj = UserConfig()

