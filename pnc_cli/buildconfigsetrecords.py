__author__ = 'thauser'
from argh import arg

import pnc_cli.cli_types as types
from pnc_cli import utils
from pnc_cli.swagger_client.apis import BuildconfigurationsetsApi
from pnc_cli.swagger_client.apis import BuildconfigsetrecordsApi
import pnc_cli.user_config as uc

sets_api = BuildconfigurationsetsApi(uc.user.get_api_client())
bcsr_api = BuildconfigsetrecordsApi(uc.user.get_api_client())


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configuration_set_records(page_size=200, page_index=0, sort="", q=""):
    """
    List all build configuration set records.
    """
    response = utils.checked_api_call(bcsr_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("id", help="ID of build configuration set record to retrieve.", type=types.existing_bc_set_record)
def get_build_configuration_set_record(id):
    """
    Get a specific BuildConfigSetRecord
    """
    response = utils.checked_api_call(bcsr_api, 'get_specific', id=id)
    if response:
        return utils.format_json(response.content)


@arg("id", help="ID of BuildConfigSetRecord to retrieve build records from.", type=types.existing_bc_set_record)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_records_for_build_config_set(id, page_size=200, page_index=0, sort="", q=""):
    """
    Get a list of BuildRecords for the given BuildConfigSetRecord
    """
    response = utils.checked_api_call(bcsr_api, 'get_build_records', id=id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)
