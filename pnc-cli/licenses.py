import utils
import swagger_client
from swagger_client.apis.licenses_api import LicensesApi
from pprint import pprint
from argh import arg

licenses_api = LicensesApi(utils.get_api_client())

def _create_license_object(**kwargs):
    created_license = swagger_client.models.license.License()
    for key, value in kwargs.iteritems():
        setattr(created_license, key, value)
    return created_license

def get_license_id(id,name):
    if id:
        return id
    elif name:
        l_id = _get_license_id_by_name(name)
        if not l_id:
            print("No license with name {0} exists.").format(name)
            return
    else:
        print("A license ID or name is required.")
        return
    return l_id


def _license_exists(license_id):
    existing_ids = [x.id for x in licenses_api.get_all()]
    return license_id in existing_ids

def _get_license_id_by_name(name):
    licenses = licenses_api.get_all()
    for license in licenses:
        if license.full_name == name:
            return license.id
    return None

@arg("full_name", help="Name for the new license")
@arg("full_content", help="Full textual content of the new license")
@arg("-r","--ref-url", help="URL containing a reference for the license")
@arg("-sn","--short_name", help="Abbreviation or \"short name\" for the license")
@arg("-pids","--projects-ids", type=int, nargs='+', help="List of project ids that should be associated with the new license. IDs must denote existing projects")
def create_license(**kwargs):
    """Create a new license"""
    license = _create_license_object(**kwargs)
    licenses_api.create_new(body=license, callback=callback_function)

@arg("-i","--id", help="ID for the license to retrieve")
@arg("-n","--name", help="Name for the license to retrieve")
def get_license(id=None, name=None):
    """
    Get a specific license by either id or name
    :param id: id of the license to retrieve
    :param name: full name of the license to retrieve
    :return: JSON with all license attributes
    """
    search_id = get_license_id(id,name)
    if not search_id:
        return
    licenses_api.get_specific(id=search_id, callback=callback_function)

@arg("license_id", help="ID of the license to delete")
def delete_license(license_id):
    """
    Delete a license by id
    :param license_id:
    :return:
    """
    licenses_api.delete(id=license_id,callback=callback_function)

@arg("license_id", help="ID of the license to update")
@arg("-n","--name", help="Name for the new license")
@arg("-c","--content", help="Full textual content of the new license")
@arg("-refurl","--reference-url", help="URL containing a reference for the license")
@arg("-abbr","--abbreviation", help="Abbreviation or \"short name\" for the license")
@arg("-pid","--project-ids", help="List of project ids that should be associated with the new license. IDs must denote existing projects")
def update_license(license_id, **kwargs):
    """
    Replace the license with id license_id with a new license.
    :param license_id:
    :param kwargs:
    :return:
    """
    updated_license = _create_license_object(**kwargs)
    if _license_exists(license_id):
        licenses_api.update(id=license_id, body=updated_license, callback=callback_function)
    else:
        print("No license with id {0} exists.").format(license_id)

def list_licenses():
    """
    List all licenses
    :return:
    """
    licenses_api.get_all(callback=callback_function)

def callback_function(response):
    if response:
        pprint(response.content)


