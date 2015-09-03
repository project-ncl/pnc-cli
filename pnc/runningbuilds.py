import utils
from argh import arg
from swagger_client.apis.runningbuildrecords_api import RunningbuildrecordsApi
from pprint import pprint

running_api = RunningbuildrecordsApi(utils.get_api_client())

def list_running_builds():
    """
    List all running builds
    :return: list of running builds
    """
    running_api.get_all(callback=callback_function)

@arg("id", help="ID of the running build to retrieve.")
def get_running_build(id):
    """
    Get info about a specific running build
    :param id: id of the build
    :return: build information!
    """
    running_api.get_specific(id=id)

def callback_function(response):
    if response:
        pprint(response)
