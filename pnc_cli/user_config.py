import logging

from argh import arg
import configparser # see https://pypi.org/project/configparser/
from configparser import NoSectionError, NoOptionError
import atexit
import getpass
import json
import os
import pickle
import sys

import requests

from . import swagger_client
import pnc_cli.utils as utils
from . import keycloak_config as kc
from . import pnc_server_config as psc

# make sure that input behaves as expected
try:
    input = raw_input
except NameError:
    pass

SAVED_USER_FILENAME = "saved-user.p"
SAVED_USER = utils.CONFIG_LOCATION + SAVED_USER_FILENAME

trueValues = ['True', 'true', '1']


class UserConfig():
    def __init__(self):
        config, configFileName = utils.get_config()
        self.configFileName = configFileName
        self.username = self.load_username_from_config(config)
        self.password = self.load_password_from_config(config)
        self.pnc_config = psc.PncServerConfig(config)
        self.keycloak_config = kc.KeycloakConfig(config)
        self.refresh_token = None
        self.refresh_token_time = 0
        self.access_token = None
        self.access_token_time = 0
        if self.username and self.password:
            self.retrieve_keycloak_token()
        else:
            logging.info("Commands requiring authentication will fail.")
        self.apiclient = self.create_api_client(True)

    def __getstate__(self):
        return self.keycloak_config, self.username, self.access_token, self.access_token_time, self.refresh_token, self.refresh_token_time

    def __setstate__(self, state):
        # here we need to read the config file again, to check that values for URLs haven't changed. the way to
        # change the username / password will be a login function the user calls. ideally the config file won't need
        # to be changed much once it's in place
        newtoken = False
        refreshtoken = False
        config, configFileName = utils.get_config()
        self.configFileName = configFileName

        if len(state) == 4:
            # old version of saved user_config
            saved_kc_config, saved_username, self.access_token, self.access_token_time = state
            self.refresh_token_time = 0
            refreshtoken = True
        else:
            saved_kc_config, saved_username, self.access_token, self.access_token_time, self.refresh_token, self.refresh_token_time = state

        self.pnc_config = psc.PncServerConfig(config)

        # check for changes in keycloak username; if so, we'll need to get a new token regardless of time
        self.username = self.load_username_from_config(config)
        if self.username is not None and self.username != saved_username:
            sys.stderr.write("Keycloak username has been changed. Retrieving new token...\n")
            newtoken = True
        else:
            self.username = saved_username

        # check for changes in keycloak configuration; if so, we'll need to get a new token regardless of time
        current_keycloak_config = kc.KeycloakConfig(config)
        if not current_keycloak_config == saved_kc_config:
            logging.info("Keycloak server has been reconfigured. Retrieving new token...\n")
            self.keycloak_config = current_keycloak_config
            newtoken = True
        else:
            self.keycloak_config = saved_kc_config


        # if more than a day has passed since we saved the token, and keycloak server configuration is not modified,
        # get a new one
        if not newtoken and utils.current_time_millis() - self.refresh_token_time >= 8640000:
            # input the password again since we no longer cache it
            logging.info("Keycloak token has expired for user {}. Retrieving new token...\n".format(self.username))
            newtoken = True

        # if access_token is more than hour old, refresh it
        if not newtoken and 8640000 >= utils.current_time_millis() - self.access_token_time > 360000:
            logging.info("Refreshing access token for user {}. \n".format(self.username))
            refreshtoken = True

        if not newtoken and refreshtoken:
            self.refresh_access_token()

        if newtoken:
            # if using client auth, we simply get a new token.
            if self.keycloak_config.client_mode in trueValues:
                self.retrieve_keycloak_token()
            else:
                # enter password to get new token, but only if the user has not entered a password in pnc-cli.conf
                password = self.load_password_from_config(config)
                if password:
                    self.password = password
                else:
                    self.password = self.input_password()
                self.retrieve_keycloak_token()
        self.apiclient = self.create_api_client()

    # this function gets input from the user to set the username
    def input_username(self):
        username = input('PNC username: ')
        return username

    # this function gets input from the user to set the password
    def input_password(self):
        password = getpass.getpass('PNC password: ')
        return password

    def load_username_from_config(self, config):
        try:
            username = config.get('PNC', 'username')
            logging.info("Loaded username from pnc-cli.conf: {}\n".format(username))
            return username
        except (NoSectionError, NoOptionError):
            logging.info("Username not specified in section PNC of %s" % self.configFileName)
            return None
        except Exception as e:
            logging.error('Error reading username from section PNC of %s - %s' % (self.configFileName, str(e)))
            return None

    def load_password_from_config(self, config):
        try:
            password = config.get('PNC', 'password')
            logging.info("Loaded password from pnc-cli.conf\n")
            return password
        except (NoSectionError, NoOptionError):
            logging.info("Password not specified in section PNC of %s" % self.configFileName)
            return None
        except Exception as e:
            logging.error('Error reading password from section PNC of %s - %s' % (self.configFileName, str(e)))
            return None

    def refresh_access_token(self):
        params = {'grant_type': 'refresh_token',
                  'client_id': self.keycloak_config.client_id,
                  'refresh_token': self.refresh_token
                  }
        r = requests.post(self.keycloak_config.url,params,verify=False)
        if r.status_code == 200:
            if self.username:
                logging.info("Token refreshed for user {}. \n".format(self.username))
            else:
                logging.info("Token refreshed for client from {}. \n".format(self.keycloak_config.client_id))
            self.access_token_time = utils.current_time_millis()
            reply = json.loads(r.content.decode('utf-8'))
            self.access_token = str(reply.get('access_token'))
    # retrieves a token from the keycloak server using the configured username / password / keycloak server
    def retrieve_keycloak_token(self):
        if self.keycloak_config.client_mode in trueValues:
            params = {'grant_type': 'client_credentials',
                      'client_id': self.keycloak_config.client_id,
                      'client_secret': self.keycloak_config.client_secret,
            }
            r = requests.post(self.keycloak_config.url, params, verify=False)
            if r.status_code == 200:
                logging.info("Token retrieved for client from {}.\n".format(self.keycloak_config.client_id))
                self.access_token_time = utils.current_time_millis()
                self.refresh_token_time = utils.current_time_millis()
                reply = json.loads(r.content.decode('utf-8'))
                self.refresh_token = str(reply.get('refresh_token'))
                self.access_token = str(reply.get('access_token'))
            else:
                logging.error("Failed to retrieve client token:")
                logging.error(r)
                logging.error(r.content)
                exit(1)
        else:
            if self.username and self.password:
                params = {'grant_type': 'password',
                          'client_id': self.keycloak_config.client_id,
                          'username': self.username,
                          'password': self.password}
                r = requests.post(self.keycloak_config.url, params, verify=False)
                if r.status_code == 200:
                    logging.info("Token retrieved for {}.\n".format(self.username))
                    self.access_token_time = utils.current_time_millis()
                    self.refresh_token_time = utils.current_time_millis()
                    reply = json.loads(r.content.decode('utf-8'))
                    self.refresh_token = str(reply.get('refresh_token'))
                    self.access_token = str(reply.get('access_token'))
                else:
                    logging.error("Failed to retrieve token:")
                    logging.error(r)
                    logging.error(r.content)
                    exit(1)
            else:
                logging.error("No credentials. Authentication is not possible.")

    def create_api_client(self, allow_anonymous_access = False):
        if self.access_token:
            return swagger_client.ApiClient(self.pnc_config.url, header_name='Authorization',
                                            header_value='Bearer ' + self.access_token)
        else:
            if not allow_anonymous_access:
                logging.error("No Keycloak token is present. Commands requiring authentication will fail.")
            return swagger_client.ApiClient(self.pnc_config.url)

    def get_api_client(self):
        return self.apiclient

user = None

def get_user():
    global user


    if user is None:

        pickled_file_used = False

        if os.path.exists(SAVED_USER):
            try:

                user = pickle.load(open(SAVED_USER, "rb"))
                pickled_file_used = True

                if user.keycloak_config.client_mode in trueValues:
                    logging.info("Command performed using client authorization.\n")
                else:
                    logging.info("Command performed with user: {}\n".format(user.username))
                users_api = swagger_client.UsersApi(user.get_api_client())
                utils.checked_api_call(users_api, 'get_logged_user') # inits the user if it doesn't exist in pnc's db already

            except Exception:
                # Handle cases when we can't read that pickle protocol
                logging.debug("Could not read saved-user pickle file. Loading from config")
                pickled_file_used = False

        if not pickled_file_used:
            user = UserConfig()

    return user


def save():
    if user is not None and user.access_token:
        pickle.dump(user, open(SAVED_USER, "wb"), protocol=pickle.HIGHEST_PROTOCOL)


atexit.register(save)


@arg("-u", "--username", help="Username for the new user")
@arg("-p", "--password", help="Password for the specified user")
def login(username=None, password=None):
    """
    Log in to PNC using the supplied username and password. The keycloak token will
    be saved for all subsequent pnc-cli operations until login is called again
    :return:
    """
    global user
    user = UserConfig()
    if username:
        user.username = username
    else:
        user.username = user.input_username()

    if password:
        user.password = password
    else:
        user.password = user.input_password()

    if (not ( user.username and user.password) ):
        logging.error("Username and password must be provided for login")
        return;
    user.retrieve_keycloak_token()
    user.apiclient = user.create_api_client()
    save()
