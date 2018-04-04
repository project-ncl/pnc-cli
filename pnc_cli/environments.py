import argparse

from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.common as common
import pnc_cli.utils as utils
from pnc_cli.swagger_client import BuildEnvironmentRest
from pnc_cli.pnc_api import pnc_api


__author__ = 'thauser'


@arg("-i", "--id", help="ID of the BuildEnvironment to retrieve.", type=types.existing_environment_id)
@arg("-n", "--name", help="Name of the BuildEnvironment to retrieve.", type=types.existing_environment_name)
def get_environment(id=None, name=None):
    """
    Get a specific Environment by name or ID
    """
    data = get_environment_raw(id, name)
    if data:
        return utils.format_json_list(data)

def get_environment_raw(id=None, name=None):
    search_id = common.set_id(pnc_api.environments, id, name)
    response = utils.checked_api_call(pnc_api.environments, 'get_specific', id=search_id)
    return response.content


@arg("-p", "--page-size", help="Limit the amount of BuildEnvironments returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_environments(page_size=200, page_index=0, sort="", q=""):
    data = list_environments_raw(page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)


def list_environments_raw(page_size=200, page_index=0, sort="", q=""):
    """
    List all Environments
    """
    response = utils.checked_api_call(pnc_api.environments, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content

