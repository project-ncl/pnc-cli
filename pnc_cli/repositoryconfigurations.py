from argh import arg
from argh.exceptions import CommandError

import logging
import pnc_cli.cli_types as types
from pnc_cli import utils
from pnc_cli.pnc_api import pnc_api


@arg("id", help="ID of the RepositoryConfiguration to retrieve.", type=types.existing_rc_id)
def get_repository_configuration(id):
    """
    Retrieve a specific RepositoryConfiguration
    """

    response = utils.checked_api_call(pnc_api.repositories, 'get_specific', id=id)
    if response:
        return response.content


@arg("id", help="ID of the RepositoryConfiguration to update.", type=types.existing_rc_id)
@arg("-e", "--external-repository", help="URL to the external sources repository.", type=types.valid_git_url)
@arg("-s", "--prebuild-sync", help="Pre-build source synchronization.", type=types.t_or_f)
def update_repository_configuration(id, external_repository=None, prebuild_sync=None):
    """
    Update an existing RepositoryConfiguration with new information
    """
    to_update_id = id

    rc_to_update = pnc_api.repositories.get_specific(id=to_update_id).content

    if external_repository is None:
        external_repository = rc_to_update.external_url
    else:
        rc_to_update.external_url = external_repository

    if prebuild_sync is not None:
        rc_to_update.pre_build_sync_enabled = prebuild_sync

    if not external_repository and prebuild_sync:
        logging.error("You cannot enable prebuild sync without external repository")
        return

    response = utils.checked_api_call(pnc_api.repositories, 'update', id=to_update_id, body=rc_to_update)
    if response:
        return response.content

@arg("-p", "--page-size", help="Limit the amount of repository configurations returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_repository_configurations(page_size=200, page_index=0, sort="", q=""):
    """
    List all RepositoryConfigurations
    """
    response = utils.checked_api_call(pnc_api.repositories, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)

@arg("url", help="Url part to search for.")
@arg("-p", "--page-size", help="Limit the amount of repository configurations returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
def search_repository_configuration(url, page_size=10, page_index=0, sort=""):
    """
    Search for Repository Configurations based on internal or external url
    """
    content = search_repository_configuration_raw(url, page_size, page_index, sort)
    if content:
        return utils.format_json_list(content)

def search_repository_configuration_raw(url, page_size=10, page_index=0, sort=""):
    """
    Search for Repository Configurations based on internal or external url
    """
    response = utils.checked_api_call(pnc_api.repositories, 'search', page_size=page_size, page_index=page_index, sort=sort, search=url)
    if response:
        return response.content

@arg("url", help="Url to search for.")
@arg("-p", "--page-size", help="Limit the amount of repository configurations returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
def match_repository_configuration(url, page_size=10, page_index=0, sort=""):
    """
    Search for Repository Configurations based on internal or external url with exact match
    """
    content = match_repository_configuration_raw(url, page_size, page_index, sort)
    if content:
        return utils.format_json_list(content)


def match_repository_configuration_raw(url, page_size=10, page_index=0, sort=""):
    """
    Search for Repository Configurations based on internal or external url with exact match
    """
    response = utils.checked_api_call(pnc_api.repositories, 'match', page_size=page_size, page_index=page_index, sort=sort, search=url)
    if response:
        return response.content
