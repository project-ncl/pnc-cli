

__author__ = 'thauser'

import pnc_cli.utils as utils
import pnc_cli.user_config as uc
from swagger_client.apis.users_api import UsersApi

users_api = UsersApi(uc.user.get_api_client())

def get_logged_user():
    response = utils.checked_api_call(users_api, 'get_logged_user')
    if response:
        return utils.format_json(response.content)