from argh import arg

from pnc_cli import utils
from pnc_cli.swagger_client import RunningbuildrecordsApi

running_api = RunningbuildrecordsApi(utils.get_api_client())


def list_running_builds():
    """
    List all running builds
    """
    response = utils.checked_api_call(running_api, 'get_all')
    if response:
        return response.content


@arg("id", help="ID of the running build to retrieve.")
def get_running_build(id):
    """
    Get info about a specific running build
    """
    response = utils.checked_api_call(running_api, 'get_specific', id=id)
    if response:
        return response.content
