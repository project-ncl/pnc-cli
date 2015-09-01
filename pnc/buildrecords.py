from argh import arg
from client.BuildrecordsApi import BuildrecordsApi
import sys
import client
import utils
import buildconfigurations
import projects

@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_build_records(attributes=None):
    response = get_all()
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.BuildRecord.BuildRecord().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

@arg("-i","--id", help="Build configuration ID to retrieve build records of.")
@arg("-n","--name", help="Build configuration name to retrieve build records of.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_records_for_build_config(id=None, name=None, attributes=None):
    config_id = buildconfigurations.get_config_id(id,name)
    if not config_id:
        return

    response = get_all_for_build_configuration(config_id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.BuildRecord.BuildRecord().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

@arg("-i","--id", help="Project ID to retrieve build records of.")
@arg("-n","--name", help="Project name to retrieve build records of.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_records_for_project(id=None, name=None, attributes=None):
    project_id = projects.get_project_id(id,name)
    if not project_id:
        return

    response = get_all_for_project(project_id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.BuildRecord.BuildRecord().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

@arg("id", help="Build record ID to retrieve.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_build_record(id, attributes=None):
    response = get_specific(id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.BuildRecord.BuildRecord().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

@arg("id", help="Build record ID to retrieve artifacts from.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_build_artifacts(id, attributes=None):
    response = get_artifacts(id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.Artifact.Artifact().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

@arg("id", help="Build record ID to retrieve audited build configuration from.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_audited_config_for_record(id, attributes=None):
    response = get_audited_build_configuration(id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    if attributes:
        valid_attributes = client.models.BuildConfigurationAudited.BuildConfigurationAudited().attributeMap
        utils.print_matching_attribute(response.json(), attributes, valid_attributes)
    else:
        utils.print_by_key(response.json())

def get_logs_for_record(id):
    response = get_logs(id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    print response.text

def get_all():
    return BuildrecordsApi(utils.get_api_client()).getAll()

def get_all_for_build_configuration(config_id):
    return BuildrecordsApi(utils.get_api_client()).getAllForBuildConfiguration(configurationId=config_id)

def get_all_for_project(project_id):
    return BuildrecordsApi(utils.get_api_client()).getAllForProject(projectId=project_id)

def get_specific(record_id):
    return BuildrecordsApi(utils.get_api_client()).getSpecific(id=record_id)

def get_artifacts(record_id):
    return BuildrecordsApi(utils.get_api_client()).getArtifacts(id=record_id)

def get_audited_build_configuration(record_id):
    return BuildrecordsApi(utils.get_api_client()).getBuildConfigurationAudited(id=record_id)

def get_logs(record_id):
    return BuildrecordsApi(utils.get_api_client()).getLogs(id=record_id)


