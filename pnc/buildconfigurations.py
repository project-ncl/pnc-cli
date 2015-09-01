from argh import arg
import sys
import client
from client.BuildconfigurationsApi import BuildconfigurationsApi
import utils

__author__ = 'thauser'
#must be a better way to do this.
def create_build_conf_object(name, project_id, environment, description=None, scm_url=None, scm_revision=None, patches_url=None,
                                build_script=None):
    created_build_configuration = client.models.Configuration.Configuration()
    created_build_configuration.name = name
    created_build_configuration.projectId = project_id
    created_build_configuration.environmentId = environment
    return created_build_configuration

def get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    response = get_all()
    for config in response.json():
        if config["name"] == name:
            return config["id"]
    return None

def build_configuration_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists
    """
    response = get_specific(search_id)
    if response.ok:
        return True
    return False

def get_config_id(id,name):
    if id:
        config_id = id
        if not build_configuration_exists(config_id):
            print("There is no build configuration with id {0}.".format(config_id))
            return
    elif name:
        config_id = get_build_configuration_id_by_name(name)
        if not config_id:
            print("There is no build configuration with name {0}.".format(name))
            return
    else:
        print("Either a name or an ID of a build configuration is required.")
        return
    return config_id

@arg("-i", "--id", help="ID of the build configuration to trigger")
@arg("-n", "--name", help="Name of the build configuration to trigger")
def build(id=None,name=None):
    """Trigger a build configuration giving either the name or ID."""
    trigger_id = get_config_id(id,name)
    if not trigger_id:
        return

    response = trigger(trigger_id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    triggered_build = response.json()
    utils.print_by_key(triggered_build)

def create_build_configuration(name, project_id, environment, description=None, scm_url=None, scm_revision=None, patches_url=None,
                               build_script=None):
    build_configuration = create_build_conf_object(name, project_id, environment, description, scm_url, scm_revision, patches_url, build_script)
    response = create(build_configuration)
    new_bc = response.json()
    utils.print_by_key(new_bc)

@arg("-a", "--attributes", help="List of attributes to retrieve. Will print given attributes separated by whitespace.")
def list_build_configurations(attributes=None):
    response = get_all()
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return
    build_configurations = response.json()
    if attributes is not None:
        utils.print_matching_attribute(build_configurations, attributes, client.models.Configuration.Configuration().attributeMap)
    else:
        utils.print_by_key(build_configurations)

def get_all():
    return BuildconfigurationsApi(utils.get_api_client()).getAll()

def get_specific(id):
    return BuildconfigurationsApi(utils.get_api_client()).getSpecific(id=id)

def create(build_configuration):
    return BuildconfigurationsApi(utils.get_api_client()).createNew(body=build_configuration)

def trigger(id):
    return BuildconfigurationsApi(utils.get_api_client()).trigger(id=id)
