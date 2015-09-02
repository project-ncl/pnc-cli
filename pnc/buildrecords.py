import sys

from argh import arg

from swagger_client.apis.buildrecords_api import BuildrecordsApi
import swagger_client
import utils
import buildconfigurations
import projects


@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_build_records(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_record.BuildRecord().attribute_map)

@arg("-i","--id", help="Build configuration ID to retrieve build records of.")
@arg("-n","--name", help="Build configuration name to retrieve build records of.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_records_for_build_config(id=None, name=None, attributes=None):
    config_id = buildconfigurations.get_config_id(id,name)
    if not config_id:
        return

    response = get_all_for_build_configuration(config_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_record.BuildRecord().attribute_map)

@arg("-i","--id", help="Project ID to retrieve build records of.")
@arg("-n","--name", help="Project name to retrieve build records of.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def list_records_for_project(id=None, name=None, attributes=None):
    project_id = projects.get_project_id(id,name)
    if not project_id:
        return

    response = get_all_for_project(project_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_record.BuildRecord().attribute_map)

@arg("id", help="Build record ID to retrieve.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_build_record(id, attributes=None):
    response = get_specific(id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_record.BuildRecord().attribute_map)

@arg("id", help="Build record ID to retrieve artifacts from.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_build_artifacts(id, attributes=None):
    response = get_artifacts(id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.rtifact.Artifact().attribute_map)

@arg("id", help="Build record ID to retrieve audited build configuration from.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_audited_config_for_record(id, attributes=None):
    response = get_audited_build_configuration(id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                       response,
                       attributes,
                       swagger_client.models.BuildConfigurationAudited.BuildConfigurationAudited().attribute_map)

@arg("id", help="Build record ID to retrieve logs from.")
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


