from argh import arg

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli.swagger_client import BuildrecordsApi
from pnc_cli.swagger_client import BuildconfigurationsApi
from pnc_cli.swagger_client import ProjectsApi
import pnc_cli.user_config as uc

records_api = BuildrecordsApi(uc.user.get_api_client())
configs_api = BuildconfigurationsApi(uc.user.get_api_client())
projects_api = ProjectsApi(uc.user.get_api_client())


@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records(page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildRecords
    """
    response = utils.checked_api_call(records_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="BuildConfiguration ID to retrieve BuildRecords of.", type=types.existing_bc_id)
@arg("-n", "--name", help="BuildConfiguration name to retrieve BuildRecords of.", type=types.existing_bc_name)
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_build_configuration(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildRecords for a given BuildConfiguration
    """
    config_id = common.set_id(configs_api, id, name)
    response = utils.checked_api_call(records_api, 'get_all_for_build_configuration', configuration_id=config_id,
                                      page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="Project ID to retrieve BuildRecords of.")
@arg("-n", "--name", help="Project name to retrieve BuildRecords of.")
@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_project(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildRecords for a given Project
    """
    project_id = common.set_id(projects_api, id, name)
    response = utils.checked_api_call(records_api, 'get_all_for_project_1', project_id=project_id, page_size=page_size, page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="BuildRecord ID to retrieve.", type=types.existing_build_record)
def get_build_record(id):
    """
    Get a specific BuildRecord by ID
    """
    response = utils.checked_api_call(records_api, 'get_specific', id=id)
    if response:
        return utils.format_json(response.content)


@arg("id", help="BuildRecord ID to retrieve artifacts from.", type=types.existing_build_record)
@arg("-p", "--page-size", help="Limit the amount of Artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_built_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    """
    List Artifacts associated with a BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_built_artifacts', id=id,
            page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="BuildRecord ID to retrieve dependency Artifacts from.", type=types.existing_build_record)
@arg("-p", "--page-size", help="Limit the amount of Artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_dependency_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    """
    List dependency artifacts associated with a BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_dependency_artifacts', id=id, page_size=page_size, page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="BuildRecord ID to retrieve audited BuildConfiguration from.", type=types.existing_build_record)
def get_audited_configuration_for_record(id):
    """
    Get the BuildConfigurationAudited for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_build_configuration_audited', id=id)
    if response:
        return utils.format_json(response.content)


@arg("id", help="BuildRecord ID to retrieve the log from.", type=types.existing_build_record)
def get_log_for_record(id):
    """
    Get the log for a given BuildRecord
    """
    response = utils.checked_api_call(records_api, 'get_logs', id=id)
    if response:
        return response


@arg("id", help="BuildRecord ID to retrieve Artifacts from.", type=types.existing_build_record)
@arg("-p", "--page-size", help="Limit the amount of Artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(records_api, 'get_artifacts', id=id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="BuildRecord ID to add an Attribute to.", type=types.existing_build_record)
@arg("key", help="Key for the Attribute.")
@arg("value", help="Value for the Attribute.")
def put_attribute(id, key, value):
    utils.checked_api_call(records_api, 'put_attribute', id=id, key=key, value=value)


@arg("id", help="BuildRecord ID to remove an Attribute from.", type=types.existing_build_record)
@arg("key", help="Key of the Attribute to remove.")
def remove_attribute(id, key):
    utils.checked_api_call(records_api, 'remove_attribute', id=id, key=key)


@arg("key", help="Key of the Attribute to query BuildRecords for.")
@arg("value", help="Value of the Attribute to query BuildRecords for.")
def query_by_attribute(key, value):
    response = utils.checked_api_call(records_api, "query_by_attribute", key=key, value=value)
    if response:
        return utils.format_json(response)


@arg("id", help="BuildRecord ID to list Attributes of.", type=types.existing_build_record)
def list_attributes(id):
    response = utils.checked_api_call(records_api, 'get_attributes', id=id)
    if response:
        return response.content
