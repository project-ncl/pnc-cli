from swagger_client.rest import ApiException
import utils
import buildconfigurations
import projects
from pprint import pprint
from argh import arg
from swagger_client.apis.buildrecords_api import BuildrecordsApi

records_api = BuildrecordsApi(utils.get_api_client())

def list_build_records():
    """
    List all build records
    :return:
    """
    response = utils.checked_api_call('get_all')
    if response: pprint(response.content)

@arg("-i","--id", help="Build configuration ID to retrieve build records of.")
@arg("-n","--name", help="Build configuration name to retrieve build records of.")
def list_records_for_build_config(id=None, name=None):
    config_id = buildconfigurations.get_config_id(id,name)
    if not config_id:
        return
    response = utils.checked_api_call('get_all_for_build_configuration', configuration_id=config_id)
    if response: pprint(response.content)

@arg("-i","--id", help="Project ID to retrieve build records of.")
@arg("-n","--name", help="Project name to retrieve build records of.")
def list_records_for_project(id=None, name=None):
    project_id = projects.get_project_id(id,name)
    if not project_id:
        return
    response = utils.checked_api_call('get_all_for_project', project_id=project_id)
    if response: pprint(response)

@arg("id", help="Build record ID to retrieve.")
def get_build_record(id):
    response = utils.checked_api_call('get_specific',id=id)
    if response: pprint(response.content)

@arg("id", help="Build record ID to retrieve artifacts from.")
def get_build_artifacts(id):
    response = utils.checked_api_call('get_artifacts',id=id)
    if response: pprint(response.content)

@arg("id", help="Build record ID to retrieve audited build configuration from.")
def get_audited_config_for_record(id):
    response = utils.checked_api_call('get_build_configuration_audited',id=id)
    if response: pprint(response.content)

@arg("id", help="Build record ID to retrieve logs from.")
def get_logs_for_record(id):
    response = utils.checked_api_call(records_api, 'get_logs',id=id)
    if response: pprint(response)