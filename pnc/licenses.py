from argh import arg
from client.LicensesApi import LicensesApi
import utils
import client as client

from client.BuildconfigurationsApi import BuildconfigurationsApi

__author__ = 'thauser'

def _create_license_object(name, content, reference_url, abbreviation, project_ids):
    created_license = client.models.License.License()
    created_license.fullName = name
    created_license.fullContent = content
    if reference_url: created_license.refUrl = reference_url
    if abbreviation: created_license.shortName = abbreviation
    if project_ids: created_license.projectsIds = project_ids
    return created_license

def _license_exists(license_id):
    response = LicensesApi(utils.get_api_client()).getSpecific(id=license_id)
    if response.ok:
        return True
    return False

def _get_license_id_by_name(name):
    response = LicensesApi(utils.get_api_client()).getAll()
    for config in response.json():
        if config["fullName"] == name:
            return config["id"]
    return None

@arg("name", help="Name for the new license")
@arg("content", help="Full textual content of the new license")
@arg("-r","--reference-url", help="URL containing a reference for the license")
@arg("-abbr","--abbreviation", help="Abbreviation or \"short name\" for the license")
@arg("-pid","--project-ids", help="List of project ids that should be associated with the new license. IDs must denote existing projects")
def create_license(name, content, reference_url=None, abbreviation=None, project_ids=None):
    """Create a new license"""
    license = _create_license_object(name, content, reference_url, abbreviation, project_ids)
    response = LicensesApi(utils.get_api_client()).createNew(body=license)
    print(utils.pretty_format_response(response.json()))

@arg("-i","--id", help="ID for the license to retrieve")
@arg("-n","--name", help="Name for the license to retrieve")
def get_license(id=None, name=None):
    if id:
        search_id = id
    elif name:
        search_id = _get_license_id_by_name(name)
        if not search_id:
            print("No license with name {0} exists.").format(name)
            return
    else:
        print("get-license requires either a license name or id.")
        return
    response = LicensesApi(utils.get_api_client()).getSpecific(id=search_id)
    if response.ok:
        print(utils.pretty_format_response(response.json()))
    else:
        print("No license with id {0} exists.").format(id)
    pass


@arg("license_id", help="ID of the license to delete")
def delete_license(license_id):
    if license_id:
        response = LicensesApi(utils.get_api_client()).delete(id=license_id)
        if response.ok:
            print("License {0} successfully deleted.").format(license_id)
        else:
            print("Deleting license {0} failed.").format(license_id)
            print(response)
    else:
        print("No license id specified.")

@arg("license_id", help="ID of the license to update")
@arg("-n","--name", help="Name for the new license")
@arg("-c","--content", help="Full textual content of the new license")
@arg("-refurl","--reference-url", help="URL containing a reference for the license")
@arg("-abbr","--abbreviation", help="Abbreviation or \"short name\" for the license")
@arg("-pid","--project-ids", help="List of project ids that should be associated with the new license. IDs must denote existing projects")
def update_license(license_id, name=None, content=None, reference_url=None, abbreviation=None, project_ids=None):
    updated_license = _create_license_object(name, content, reference_url, abbreviation, project_ids)
    if license_id:
        if _license_exists(license_id):
            response = LicensesApi(utils.get_api_client()).update(id=license_id,body=updated_license)
            if response.ok:
                print("Succesfully updated license {0}.").format(license_id)
            else:
                print("Failed to update license {0}.").format(license_id)
        else:
            print("No license with id {0} exists.").format(license_id)
    else:
        print("The license ID is required to perform an update")

def list_licenses():
    """Get a JSON object containing existing licenses"""
    response = LicensesApi(utils.get_api_client()).getAll()
    print(utils.pretty_format_response(response.json()))
