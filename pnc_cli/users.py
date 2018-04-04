

__author__ = 'thauser'

import pnc_cli.utils as utils
from pnc_cli.pnc_api import pnc_api


def get_logged_user():
    response = utils.checked_api_call(pnc_api.users, 'get_logged_user')
    if response:
        return utils.format_json(response.content)
