import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class KeycloakConfig():
    def __init__(self, config):
        self.client_id = self.parse_client_id(config)
        self.realm = self.parse_realm(config)
        self.url = self.parse_url(config)

    def parse_url(self, config):
        try:
            url = config.get('PNC', 'keycloakUrl')
        except configparser.noOptionError:
            logging.error('No authentication server defined. Define "keycloakUrl" in pnc-cli.conf')
            return
        return url + '/auth/realms/' + self.realm + '/protocol/openid-connect/token'

    def parse_client_id(self, config):
        try:
            client_id = config.get('PNC', 'keycloakClientId')
        except configparser.NoOptionError:
            logging.error(
                'client_id is missing for the keycloak payload. Define "keycloakClientId" in pnc-cli.conf for authentication.')
            return
        return client_id

    def parse_realm(self, config):
        try:
            realm = config.get('PNC', 'keycloakRealm')
        except configparser.NoOptionError:
            logging.error(
                'No keycloak authentication realm defined. Define "keycloakRealm" in pnc-cli.conf to enable authentication.')
            return
        return realm

    def __eq__(self, other):
        return self.__dict__ == other.__dict__