from argh import arg
import client
from client.BuildconfigurationsApi import BuildconfigurationsApi
import utils

__author__ = 'thauser'
def _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url,
                                build_script):
    created_build_configuration = client.models.Configuration.Configuration()
    created_build_configuration.name = name
    created_build_configuration.projectId = project_id
    return created_build_configuration

def _get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    response = BuildconfigurationsApi(utils.get_api_client()).getAll()
    for config in response.json():
        if config["name"] == name:
            return config["id"]
    return None

def _build_configuration_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists
    """
    response = BuildconfigurationsApi(utils.get_api_client()).getSpecific(id=search_id)
    if response.ok:
        return True
    return False

@arg("-n", "--name", help="Name of the build configuration to trigger")
@arg("-i", "--id", help="ID of the build configuration to trigger")
def build(name=None,id=None):
    """Trigger a build configuration giving either the name or ID."""
    if id:
        if _build_configuration_exists(id):
            print(utils.pretty_format_response(BuildconfigurationsApi(utils.get_api_client()).trigger(id=id).json()))
        else:
            print("There is no build configuration with id {0}.".format(id))
    elif name:
        id = _get_build_configuration_id_by_name(name)
        if id:
            print(utils.pretty_format_response(BuildconfigurationsApi(utils.get_api_client()).trigger(id=id).json()))
        else:
            print("There is no build configuration with name {0}.".format(name))
    else:
        print("Build requires either a name or an ID of a build configuration to trigger.")


def create_build_configuration(name, project_id, environment, description="", scm_url="", scm_revision="", patches_url="",
                               build_script=""):
    #check for existing project_ids, fail out if the project id doesn't exist
    build_configuration = _create_build_configuration(name, project_id, environment, description, scm_url, scm_revision, patches_url, build_script)
    response = utils.pretty_format_response(BuildconfigurationsApi(utils.get_api_client()).createNew(body=build_configuration).json())
    print(response)



def list_build_configurations():
    """Get a JSON object containing existing build configurations"""
    response = BuildconfigurationsApi(utils.get_api_client()).getAll()
    print(utils.pretty_format_response(response.json()))