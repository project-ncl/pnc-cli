import argparse

from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.common as common
import pnc_cli.utils as utils
from pnc_cli.swagger_client import BannerRest
from pnc_cli.pnc_api import pnc_api


__author__ = 'dcheung'

def get_announcement_banner():
    """
    Get announcement banner
    """
    data = get_banner_raw()
    if data:
        return data.banner

@arg("banner", help="Text for the banner")
def set_announcement_banner(banner):
    """
    Set the announcement banner
    """
    banner_rest = BannerRest()
    banner_rest.banner = banner
    response = utils.checked_api_call(pnc_api.generic_setting,
                                      'set_announcement_banner',
                                      body=banner_rest)
    if response:
        return response

def get_banner_raw():
    response = utils.checked_api_call(pnc_api.generic_setting, 'get_announcement_banner')
    if response:
        return response

def in_maintenance_mode():
    """
    Check if we are in maintenance_mode
    """
    data = in_maintenance_mode_raw()
    if data:
        return data
    else:
        return False

@arg("banner", help="Text for the banner")
def activate_maintenance_mode(banner):
    """
    activate maintenance_mode
    """
    response = utils.checked_api_call(pnc_api.generic_setting,
                                      'activate_maintenance_mode',
                                      body=banner)
    if response:
        return response

def deactivate_maintenance_mode():
    """
    deactivate maintenance_mode
    """
    response = utils.checked_api_call(pnc_api.generic_setting,
                                      'deactivate_maintenance_mode')
    if response:
        return response


def in_maintenance_mode_raw():
    response = utils.checked_api_call(pnc_api.generic_setting, 'is_in_maintenance_mode')
    if response:
        return response
