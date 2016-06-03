from argh import arg

import logging
from pnc_cli import utils
from pnc_cli import buildconfigurations
from pnc_cli import projects
from pnc_cli.swagger_client.apis.buildrecords_api import BuildrecordsApi

records_api = BuildrecordsApi(utils.get_api_client())


def record_exists(id):
    existing = utils.checked_api_call(records_api, 'get_specific', id=id)
    if not existing:
        return False
    return True


@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records(page_size=200, sort="", q=""):
    """
    List all BuildRecords
    """
    response = utils.checked_api_call(records_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="BuildConfiguration ID to retrieve BuildRecords of.")
@arg("-n", "--name", help="BuildConfiguration name to retrieve BuildRecords of.")
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_build_configuration(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildRecords for a given BuildConfiguration
    """
    config_id = buildconfigurations.get_config_id(id, name)
    if not config_id:
        return
    response = utils.checked_api_call(records_api, 'get_all_for_build_configuration', configuration_id=config_id,
                                      page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-i", "--id", help="Project ID to retrieve BuildRecords of.")
@arg("-n", "--name", help="Project name to retrieve BuildRecords of.")
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_project(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all BuildRecords for a given Project
    """
    project_id = projects.get_project_id(id, name)
    if not project_id:
        return
    response = utils.checked_api_call(records_api, 'get_all_for_project', project_id=project_id, page_size=page_size,
                                      sort=sort, q=q)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve.")
def get_build_record(id):
    """
    Get a specific BuildRecord by ID
    """
    if not record_exists(id):
        logging.error("No BuildRecord with ID {} exists.".format(id))
        return
    response = utils.checked_api_call(records_api, 'get_specific', id=id)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve artifacts from.")
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_built_artifacts(id, page_size=200, sort="", q=""):
    """
    List Artifacts associated with a BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_built_artifacts', id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content

def list_dependency_artifacts(id, page_size=200, sort="", q=""):
    """
    List dependency artifacts associated with a BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_dependency_artifacts', id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content

@arg("id", help="BuildRecord ID to retrieve audited BuildConfiguration from.")
def get_audited_configuration_for_record(id):
    """
    Get the BuildConfigurationAudited for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_build_configuration_audited', id=id)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve the log from.")
def get_log_for_record(id):
    """
    Get the log for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_logs', id=id)
    if response:
        return response

@arg("id", help="BuildRecord ID to retrieve artifacts from.")
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def get_artifacts(id, page_size=200, sort="", q=""):
    response = utils.checked_api_call(records_api, 'get_artifacts', id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
