import utils
from argh import arg
from swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi
from pprint import pprint

running_api = RunningbuildrecordsApi(utils.get_api_client())


def list_running_builds():
    """
    List all running builds
    """
    response = utils.checked_api_call(running_api,'get_all')
    if response:
        return response.content


@arg("id", help="ID of the running build to retrieve.")
def get_running_build(id):
    """
    Get info about a specific running build
    """
    response = utils.checked_api_call(running_api,'get_specific', id=id)
    if response:
        return response.content
