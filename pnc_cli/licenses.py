from pprint import pprint

from argh import arg
from six import iteritems

from pnc_cli import utils
from pnc_cli.swagger_client import LicenseRest
from pnc_cli.swagger_client import LicensesApi

licenses_api = LicensesApi(utils.get_api_client())


def _create_license_object(**kwargs):
    created_license = LicenseRest()
    for key, value in iteritems(kwargs):
        setattr(created_license, key, value)
    return created_license


def get_license_id(id, name):
    if id:
        l_id = id
        if not _license_exists(l_id):
            print("No license with ID {} exists.".format(l_id))
            return
    elif name:
        l_id = _get_license_id_by_name(name)
        if not l_id:
            print("No license with name {0} exists.".format(name))
            return
    else:
        print("A license ID or name is required.")
        return
    return l_id


def _license_exists(license_id):
    existing_ids = [str(x.id) for x in licenses_api.get_all().content]
    return str(license_id) in existing_ids


def _get_license_id_by_name(name):
    licenses = licenses_api.get_all().content
    for license in licenses:
        if license.full_name == name:
            return license.id
    return None


@arg("full_name", help="Name for the new license")
@arg("full_content", help="Full textual content of the new license")
@arg("-r", "--ref-url", help="URL containing a reference for the license")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the license")
@arg("-pids", "--projects-ids", type=int, nargs='+',
     help="List of project ids that should be associated with the new license. IDs must denote existing projects")
# TODO: read full_content from a file.
def create_license(**kwargs):
    """
    Create a new License
    """
    license = _create_license_object(**kwargs)
    response = utils.checked_api_call(licenses_api, 'create_new', body=license)
    if response:
        return response.content


@arg("-i", "--id", help="ID for the license to retrieve")
@arg("-n", "--name", help="Name for the license to retrieve")
def get_license(id=None, name=None):
    """
    Get a specific License by either ID or fullname
    """
    search_id = get_license_id(id, name)
    if not search_id:
        return
    response = utils.checked_api_call(
        licenses_api, 'get_specific', id=search_id)
    if response:
        return response.content


@arg("license_id", help="ID of the license to delete")
# TODO: delete by name? collisions? Name not unique.
def delete_license(license_id):
    """
    Delete a License by ID
    """

    response = utils.checked_api_call(licenses_api, 'delete', id=license_id)
    if response:
        return response.content


# TODO: preserve existing license fields that aren't supplied by user, to
# make it a true update


@arg("license_id", help="ID of the license to update")
@arg("full_name", help="Name for the new license")
@arg("full_content", help="Full textual content of the new license")
@arg("-r", "--ref-url", help="URL containing a reference for the license")
@arg("-sn", "--short-name", help="Abbreviation or \"short name\" for the license")
@arg("-pids", "--projects-ids", type=int, nargs='+',
     help="List of project ids that should be associated with the new license. IDs must denote existing projects")
def update_license(license_id, **kwargs):
    """
    Replace the License with given ID with a new License
    """
    updated_license = _create_license_object(**kwargs)
    if not _license_exists(license_id):
        print("No license with id {0} exists.".format(license_id))
        return
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
