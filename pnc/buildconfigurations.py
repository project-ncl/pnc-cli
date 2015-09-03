import utils
import swagger_client
from swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from argh import arg

api = BuildconfigurationsApi(utils.get_api_client())

def create_build_conf_object(**kwargs):
    created_build_configuration = swagger_client.models.configuration.Configuration()
    for key, value in kwargs.iteritems():
        setattr(created_build_configuration, str(key), value)
    return created_build_configuration

def get_build_configuration_id_by_name(name):
    """
    Returns the id of the build configuration matching name
    :param name: name of build configuration
    :return: id of the matching build configuration, or None if no match found
    """
    response = api.get_all()
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
    response = api.get_specific(id=search_id)
    if response.ok:
        return True
    return False

def get_config_id(config_id,name):
    if id:
        return config_id
    elif name:
        return get_build_configuration_id_by_name(name)
    else:
        print("Either a name or an ID of a build configuration is required.")
        return

@arg("-i", "--id", help="ID of the build configuration to trigger.")
@arg("-n", "--name", help="Name of the build configuration to trigger.")
def build(id=None,name=None, attributes=None):
    """Trigger a build configuration giving either the name or ID."""
    trigger_id = get_config_id(id,name)
    if not trigger_id:
        return
    print(api.trigger(id=trigger_id))

@arg("name", help="Name for the new build configuration")
@arg("project-id", help="ID of the project to associate the build configuration with.")
@arg("environment", help="Environment for the new build configuration.")
@arg("-d", "--description" , help="Description of the new build configuration")
@arg("-surl", "--scm-url", help="URL to the sources of the build")
@arg("-rurl", "--scm-revision", help="Revision of the sources in scm-url to build")
@arg("-bs", "--build-script", help="Script to execute for the build")
def create_build_configuration(name, project_id, environment, **kwargs):
    kwargs['name'] = name
    kwargs['project_id'] = project_id
    kwargs['environment'] = environment
    build_configuration = create_build_conf_object(**kwargs)
    response = api.create(build_configuration)
    print (response)

def list_build_configurations():
    print(api.get_all())