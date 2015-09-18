from argh import arg

from pnc_cli import utils
from pnc_cli import buildconfigurations
from pnc_cli import projects
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi

records_api = BuildrecordsApi(utils.get_api_client())

def record_exists(id):
    existing = [str(x.id) for x in records_api.get_all().content]
    return str(id) in existing

def list_build_records():
    """
    List all build records
    """
    response = utils.checked_api_call(records_api, 'get_all')
    if response:
        return response.content


@arg("-i", "--id", help="Build configuration ID to retrieve build records of.")
@arg("-n", "--name", help="Build configuration name to retrieve build records of.")
def list_records_for_build_configuration(id=None, name=None):
    """
    List all BuildRecords for a given BuildConfiguration
    """
    config_id = buildconfigurations.get_config_id(id, name)
    if not config_id:
        return
    response = utils.checked_api_call(records_api, 'get_all_for_build_configuration', configuration_id=config_id)
    if response:
        return response.content


@arg("-i", "--id", help="Project ID to retrieve build records of.")
@arg("-n", "--name", help="Project name to retrieve build records of.")
def list_records_for_project(id=None, name=None):
    """
    List all BuildRecords for a given Project
    """
    project_id = projects.get_project_id(id, name)
    if not project_id:
        return
    response = utils.checked_api_call(records_api, 'get_all_for_project', project_id=project_id)
    if response:
        return response.content


@arg("id", help="Build record ID to retrieve.")
def get_build_record(id):
    """
    Get a specific BuildRecord by ID
    """
    if not record_exists(id):
        print("No BuildRecord with ID {} exists.".format(id))
        return
    response = utils.checked_api_call(records_api, 'get_specific', id=id)
    if response:
        return response.content


@arg("id", help="Build record ID to retrieve artifacts from.")
def list_build_artifacts(id):
    """
    List Artifacts associated with a BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_artifacts', id=id)
    if response:
        return response.content


@arg("id", help="Build record ID to retrieve audited build configuration from.")
def get_audited_configuration_for_record(id):
    """
    Get the BuildConfigurationAudited for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_build_configuration_audited', id=id)
    if response:
        return response.content


@arg("id", help="Build record ID to retrieve the log from.")
def get_log_for_record(id):
    """
    Get the log for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_logs', id=id)
    if response:
        return response
