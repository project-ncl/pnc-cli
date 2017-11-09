import logging
from argh import arg

from pnc_cli import utils
from pnc_cli.swagger_client import RunningbuildrecordsApi

import cli_types
import pnc_cli.user_config as uc

running_api = RunningbuildrecordsApi(uc.user.get_api_client())


@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
def list_running_builds(page_size=200, page_index=0, sort=""):
    """
    List all RunningBuilds
    """
    response = utils.checked_api_call(running_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="ID of the RunningBuild to retrieve.", type=cli_types.existing_running_build)
def get_running_build(id):
    """
    Get info about a specific RunningBuild
    """
    response = utils.checked_api_call(running_api, 'get_specific', id=id)
    if response:
        return utils.format_json(response.content)
