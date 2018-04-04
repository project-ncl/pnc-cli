from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.utils as utils

from pnc_cli.swagger_client import LicenseRest
from pnc_cli.pnc_api import pnc_api


def create_license_object(**kwargs):
    created_license = LicenseRest()
    for key, value in iteritems(kwargs):
        setattr(created_license, key, value)
    return created_license


@arg("full_name", help="Name for the new License")
@arg("full_content", help="Full textual content of the new License")
@arg("-r", "--ref-url", help="URL containing a reference for the License")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the License")
def create_license(**kwargs):
    """
    Create a new License
    """
    License = create_license_object(**kwargs)
    response = utils.checked_api_call(pnc_api.licenses, 'create_new', body=License)
    if response:
        return utils.format_json(response.content)


@arg("id", help="ID for the License to retrieve", type=types.existing_license)
def get_license(id):
    """
    Get a specific License by either ID or fullname
    """
    response = utils.checked_api_call(
        pnc_api.licenses, 'get_specific', id= id)
    if response:
        return utils.format_json(response.content)


@arg("license_id", help="ID of the License to delete", type=types.existing_license)
# TODO: delete by name? collisions? Name not unique.
def delete_license(license_id):
    """
    Delete a License by ID
    """

    response = utils.checked_api_call(pnc_api.licenses, 'delete', id=license_id)
    if response:
        return utils.format_json(response.content)


@arg("license_id", help="ID of the License to update", type=types.existing_license)
@arg("-n", "--full-name", help="Name for the new License")
@arg("-c", "--full-content", help="Full textual content of the new License")
@arg("-r", "--ref-url", help="URL containing a reference for the License")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the License")
def update_license(license_id, **kwargs):
    """
    Replace the License with given ID with a new License
    """
    updated_license = pnc_api.licenses.get_specific(id=license_id).content

    for key, value in iteritems(kwargs):
        if value:
            setattr(updated_license, key, value)

    response = utils.checked_api_call(
        pnc_api.licenses,
        'update',
        id=int(license_id),
        body=updated_license)
    if response:
        return utils.format_json(response.content)


@arg("-p", "--page-size", help="Limit the amount of product releases returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_licenses(page_size=200, page_index=0, sort="", q=""):
    """
    List all Licenses
    """
    response = utils.checked_api_call(pnc_api.licenses, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)
