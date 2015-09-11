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
    records_api.get_all(callback=callback_function)

@arg("-i","--id", help="Build configuration ID to retrieve build records of.")
@arg("-n","--name", help="Build configuration name to retrieve build records of.")
def list_records_for_build_config(id=None, name=None):
    config_id = buildconfigurations.get_config_id(id,name)
    if not config_id:
        return
    records_api.get_all_for_build_configuration(configuration_id=config_id, callback=callback_function)

@arg("-i","--id", help="Project ID to retrieve build records of.")
@arg("-n","--name", help="Project name to retrieve build records of.")
def list_records_for_project(id=None, name=None):
    project_id = projects.get_project_id(id,name)
    if not project_id:
        return
    records_api.get_all_for_project(project_id=project_id, callback=callback_function)

@arg("id", help="Build record ID to retrieve.")
def get_build_record(id):
    records_api.get_specific(id=id,callback=callback_function)

@arg("id", help="Build record ID to retrieve artifacts from.")
def get_build_artifacts(id):
    records_api.get_artifacts(id=id,callback=callback_function)

@arg("id", help="Build record ID to retrieve audited build configuration from.")
def get_audited_config_for_record(id):
    records_api.get_audited_build_configuration(id=id,callback=callback_function)

@arg("id", help="Build record ID to retrieve logs from.")
def get_logs_for_record(id):
    response = records_api.get_logs(id=id)
    print response

def callback_function(response):
    if response.content:
        pprint(response.content)


