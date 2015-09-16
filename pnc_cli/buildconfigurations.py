from pprint import pprint
import utils
import swagger_client
from swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from argh import arg

configs_api = BuildconfigurationsApi(utils.get_api_client())

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.BuildConfigurationRest()
    for key, value in kwargs.iteritems():
        setattr(created_build_configuration, str(key), value)
    if "build_status" not in kwargs.keys():
        setattr(created_build_configuration, "build_status", "UNKNOWN")
    return created_build_configuration

def get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    for config in configs_api.get_all().content:
        if config.name == name:
            return config.id
    return None

def config_id_exists(search_id):
    """
    Test if a build configuration matching search_id exists
    :param search_id: id to test for
    :return: True if a build configuration with search_id exists
    """
    existing_ids = [str(x.id) for x in configs_api.get_all().content]
    return search_id in existing_ids

def get_config_id(search_id,name):
    """
    Given an ID or name, checks for existence then returns an ID
    :param search_id: ID to check for existence
    :param name: name to map to ID
    :return: Valid ID if it exists. None otherwise
    """
    if id:
        if not config_id_exists(search_id):
            print("No build configuration with ID {} exists.").format(search_id)
            return
        config_id = search_id
    elif name:
        config_id = get_build_configuration_id_by_name(name)
        if not config_id:
            print("No build configuration with the name {} exists.").format(name)
            return
    else:
        print("Either a name or an ID of a build configuration is required.")
        return
    return config_id

@arg("-i", "--id", help="ID of the build configuration to trigger.")
@arg("-n", "--name", help="Name of the build configuration to trigger.")
def build(id=None,name=None):
    """Trigger a build configuration giving either the name or ID."""
    trigger_id = get_config_id(id,name)
    if not trigger_id:
        return
    configs_api.trigger(id=trigger_id,callback=callback_function)

@arg("name", help="Name for the new build configuration")
@arg("project-id", help="ID of the project to associate the build configuration with.")
@arg("environment", help="Environment for the new build configuration.")
@arg("-d", "--description" , help="Description of the new build configuration")
@arg("-surl", "--scm-url", help="URL to the sources of the build")
@arg("-rurl", "--scm-revision", help="Revision of the sources in scm-url to build")
@arg("-bs", "--build-script", help="Script to execute for the build")
def create_build_configuration(**kwargs):
    build_configuration = create_build_conf_object(**kwargs)
    configs_api.create_new(body=build_configuration, callback=callback_function)

def list_build_configurations():
    configs_api.get_all(callback=callback_function)

def callback_function(response):
    if response:
        pprint(response)
        if response.content:
            pprint(response.content)