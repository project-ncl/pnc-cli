from pprint import pprint
import logging
from argh import arg
from six import iteritems
from pnc_cli import products
from pnc_cli import utils
from pnc_cli.swagger_client import LicenseRest
from pnc_cli.swagger_client import LicensesApi
import argparse
licenses_api = LicensesApi(utils.get_api_client())


def create_license_object(**kwargs):
    created_license = LicenseRest()
    for key, value in iteritems(kwargs):
        setattr(created_license, key, value)
    return created_license


def existing_license_id(license_id):
    existing = utils.checked_api_call(licenses_api, 'get_specific', id=license_id)
    if not existing:
        raise argparse.ArgumentTypeError("No license with id {} exists".format(license_id))
    return license_id


def existing_license_name(name):
    existing = utils.checked_api_call(licenses_api, 'get_specific', fullName=name)
    if not existing:
        raise argparse.ArgumentTypeError("No license with name {} exists".format(name))
    return name


@arg("full_name", help="Name for the new License")
@arg("full_content", help="Full textual content of the new License")
@arg("-r", "--ref-url", help="URL containing a reference for the License")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the License")
@arg("-pids", "--projects-ids", nargs='+',
     help="List of project ids that should be associated with the new License. IDs must denote existing projects",
     type=products.existing_product_id)
# TODO: read full_content from a file.
def create_license(**kwargs):
    """
    Create a new License
    """
    License = create_license_object(**kwargs)
    response = utils.checked_api_call(licenses_api, 'create_new', body=License)
    if response:
        return response.content


@arg("id", help="ID for the License to retrieve", type= existing_license_id)
def get_license(id):
    """
    Get a specific License by either ID or fullname
    """
    response = utils.checked_api_call(
        licenses_api, 'get_specific', id= id)
    if response:
        return response.content


@arg("license_id", help="ID of the License to delete", type=existing_license_id)
# TODO: delete by name? collisions? Name not unique.
def delete_license(license_id):
    """
    Delete a License by ID
    """

    response = utils.checked_api_call(licenses_api, 'delete', id=license_id)
    if response:
        return response.content


# TODO: preserve existing License fields that aren't supplied by user, to
# make it a true update


@arg("license_id", help="ID of the License to update", type=existing_license_id)
@arg("-n, --full-name", help="Name for the new License")
@arg("-c, --full-content", help="Full textual content of the new License")
@arg("-r", "--ref-url", help="URL containing a reference for the License")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the License")
@arg("-pids", "--projects-ids", nargs='+',
     help="List of project ids that should be associated with the new License. IDs must denote existing projects",
     type=products.existing_product_id)
def update_license(license_id, **kwargs):
    """
    Replace the License with given ID with a new License
    """
    updated_license = create_license_object(**kwargs)
    response = utils.checked_api_call(
        licenses_api,
        'update',
        id=license_id,
        body=updated_license)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of product releases returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_licenses(page_size=200, sort="", q=""):
    """
    List all Licenses
    """
    response = utils.checked_api_call(licenses_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
