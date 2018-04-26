from argh import arg

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli.pnc_api import pnc_api


@arg("-p", "--page-size", help="Limit the amount of BuildRecords returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records(page_size=200, page_index=0, sort="", q=""):
    """
    List all BuildRecords
    """
    data = list_build_records_raw(page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_build_records_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.builds, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


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
    data = list_records_for_build_configuration_raw(id, name, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_records_for_build_configuration_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    config_id = common.set_id(pnc_api.build_configs, id, name)
    response = utils.checked_api_call(pnc_api.builds, 'get_all_for_build_configuration', configuration_id=config_id,
                                      page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


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
    data = list_records_for_project_raw(id, name, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_records_for_project_raw(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    project_id = common.set_id(pnc_api.projects, id, name)
    response = utils.checked_api_call(pnc_api.builds, 'get_all_for_project_1', project_id=project_id, page_size=page_size, page_index=page_index,
                                      sort=sort, q=q)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve.", type=types.existing_build_record)
def get_build_record(id):
    """
    Get a specific BuildRecord by ID
    """
    data = get_build_record_raw(id)
    if data:
        return utils.format_json(data)

def get_build_record_raw(id):
    response = utils.checked_api_call(pnc_api.builds, 'get_specific', id=id)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve artifacts from.", type=types.existing_build_record)
@arg("-p", "--page-size", help="Limit the amount of Artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_built_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    """
    List Artifacts associated with a BuildRecord
    """
    data = list_built_artifacts_raw(id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_built_artifacts_raw(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.builds, 'get_built_artifacts', id=id,
            page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve dependency Artifacts from.", type=types.existing_build_record)
@arg("-p", "--page-size", help="Limit the amount of Artifacts returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_dependency_artifacts(id, page_size=200, page_index=0, sort="", q=""):
    """
    List dependency artifacts associated with a BuildRecord
    """
    data = list_dependency_artifacts_raw(id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)

def list_dependency_artifacts_raw(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.builds, 'get_dependency_artifacts', id=id, page_size=page_size, page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve audited BuildConfiguration from.", type=types.existing_build_record)
def get_audited_configuration_for_record(id):
    """
    Get the BuildConfigurationAudited for a given BuildRecord
    """
    data = get_audited_configuration_for_record_raw(id)
    if data:
        return utils.format_json(data)

def get_audited_configuration_for_record_raw(id):
    response = utils.checked_api_call(pnc_api.builds, 'get_build_configuration_audited', id=id)
    if response:
        return response.content


@arg("id", help="BuildRecord ID to retrieve the log from.", type=types.existing_build_record)
def get_log_for_record(id):
    """
    Get the log for a given BuildRecord
    """
    data = get_log_for_record_raw(id)
    if data:
        return utils.format_json(data)

def get_log_for_record_raw(id):
    response = utils.checked_api_call(pnc_api.builds, 'get_logs', id=id)
    if response:
        return response


@arg("id", help="BuildRecord ID to add an Attribute to.", type=types.existing_build_record)
@arg("key", help="Key for the Attribute.")
@arg("value", help="Value for the Attribute.")
def put_attribute(id, key, value):
    utils.checked_api_call(pnc_api.builds, 'put_attribute', id=id, key=key, value=value)


@arg("id", help="BuildRecord ID to remove an Attribute from.", type=types.existing_build_record)
@arg("key", help="Key of the Attribute to remove.")
def remove_attribute(id, key):
    utils.checked_api_call(pnc_api.builds, 'remove_attribute', id=id, key=key)


@arg("key", help="Key of the Attribute to query BuildRecords for.")
@arg("value", help="Value of the Attribute to query BuildRecords for.")
def query_by_attribute(key, value):
    data = query_by_attribute_raw(key, value)
    if data:
        return utils.format_json(data)

def query_by_attribute_raw(key, value):
    response = utils.checked_api_call(pnc_api.builds, "query_by_attribute", key=key, value=value)
    if response:
        return response


@arg("id", help="BuildRecord ID to list Attributes of.", type=types.existing_build_record)
def list_attributes(id):
    data = list_attributes_raw(id)
    if data:
        return utils.format_json_list(data)

def list_attributes_raw(id,):
    response = utils.checked_api_call(pnc_api.builds, 'get_attributes', id=id)
    if response:
        return response.content
