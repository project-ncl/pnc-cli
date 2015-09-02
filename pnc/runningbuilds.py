__author__ = 'thauser'
import sys

from argh import arg

import client
from client.RunningbuildrecordsApi import RunningbuildrecordsApi
import utils


@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_running_builds(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name, response, attributes, client.models.BuildRecord.BuildRecord().attributeMap)

@arg("id", help="ID of the running build to retrieve.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_running_build(id, attributes=None):
    response = get_specific(id)
    utils.print_json_result(sys._getframe().f_code.co_name, response, attributes, client.models.BuildRecord.BuildRecord().attributeMap)

def get_all():
    return RunningbuildrecordsApi(utils.get_api_client()).getAll()

def get_specific(build_id):
    return RunningbuildrecordsApi(utils.get_api_client()).getSpecific(id=build_id)