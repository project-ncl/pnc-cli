class PncServerConfig():
    PNC_REST_LOCATION = '/pnc-rest/rest'

    def __init__(self, config):
        self.url = config.get('PNC', 'pncUrl').rstrip('/') + self.PNC_REST_LOCATION
