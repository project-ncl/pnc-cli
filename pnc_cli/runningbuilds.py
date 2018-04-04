import logging
from argh import arg

from pnc_cli import utils
from pnc_cli.pnc_api import pnc_api

import cli_types


@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
def list_running_builds(page_size=200, page_index=0, sort=""):
    """
    List all RunningBuilds
    """
    content = list_running_builds_raw(page_size, page_index, sort)
    if content:
        return utils.format_json_list(content)


def list_running_builds_raw(page_size=200, page_index=0, sort=""):
    response = utils.checked_api_call(pnc_api.running_builds, 'get_all', page_size=page_size, page_index=page_index, sort=sort)
    if response:
        return response.content


@arg("id", help="ID of the RunningBuild to retrieve.", type=cli_types.existing_running_build)
def get_running_build(id):
    """
    Get info about a specific RunningBuild
    """
    content = get_running_build_raw(id)
    if content:
        return utils.format_json(content)


def get_running_build_raw(id):
    response = utils.checked_api_call(pnc_api.running_builds, 'get_specific', id=id)
    if response:
        return response.content
