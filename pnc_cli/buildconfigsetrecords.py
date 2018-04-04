__author__ = 'thauser'
from argh import arg

import pnc_cli.cli_types as types
from pnc_cli import utils
from pnc_cli.pnc_api import pnc_api

def list_build_configuration_set_records_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.build_groups, 'get_all', page_size=page_size,
                                      page_index=page_index, sort=sort, q=q)

    if response:
        return response.content
    else:
        return None


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configuration_set_records(page_size=200, page_index=0, sort="", q=""):
    """
    List all build configuration set records.
    """
    data = list_build_configuration_set_records_raw(page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)


def get_build_configuration_set_record_raw(id):
    response = utils.checked_api_call(pnc_api.build_groups, 'get_specific', id=id)
    if response:
        return response.content
    else:
        return None


@arg("id", help="ID of build configuration set record to retrieve.", type=types.existing_bc_set_record)
def get_build_configuration_set_record(id):
    """
    Get a specific BuildConfigSetRecord
    """
    data = get_build_configuration_set_record_raw(id)
    if data:
        return utils.format_json(data)


def list_records_for_build_config_set_raw(id, page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.build_groups, 'get_build_records', id=id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content
    else:
        return None


@arg("id", help="ID of BuildConfigSetRecord to retrieve build records from.", type=types.existing_bc_set_record)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_build_config_set(id, page_size=200, page_index=0, sort="", q=""):
    """
    Get a list of BuildRecords for the given BuildConfigSetRecord
    """
    data = list_records_for_build_config_set_raw(id, page_size, page_index, sort, q)
    if data:
        return utils.format_json_list(data)
