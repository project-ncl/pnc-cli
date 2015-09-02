import sys

from argh import arg

import swagger_client
from swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
import utils


__author__ = 'thauser'
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

@arg("-i", "--id", help="ID of the build configuration to trigger.")
@arg("-n", "--name", help="Name of the build configuration to trigger.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def build(id=None,name=None, attributes=None):
    """Trigger a build configuration giving either the name or ID."""
    trigger_id = get_config_id(id,name)
    if not trigger_id:
        return
    response = trigger(trigger_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.configuration.Configuration().attribute_map)

@arg("name", help="")
@arg("project-id", help="")
@arg("environment", help="")
@arg("-d", "--description" , help="")
@arg("-surl", "--scm-url", help="")
@arg("-rurl", "--scm-revision", help="")
@arg("-bs", "--build-script", help="")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def create_build_configuration(name, project_id, environment, description=None, scm_url=None, scm_revision=None, build_script=None, attributes=None):
    build_configuration = create_build_conf_object(name=name,
                                                   projectId=project_id,
                                                   environmentId=environment,
                                                   description=description,
                                                   scmRepoUrl=scm_url,
                                                   scmRevision=scm_revision,
                                                   buildScript=build_script)
    response = create(build_configuration)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.configuration.Configuration().attribute_map)

@arg("-a", "--attributes", help="List of attributes to retrieve. Will print given attributes separated by whitespace.")
def list_build_configurations(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.configuration.Configuration().attribute_map)

def get_all():
    return BuildconfigurationsApi(utils.get_api_client()).getAll()

def get_specific(id):
    return BuildconfigurationsApi(utils.get_api_client()).getSpecific(id=id)

def create(build_configuration):
    return BuildconfigurationsApi(utils.get_api_client()).createNew(body=build_configuration)

def trigger(id):
    return BuildconfigurationsApi(utils.get_api_client()).trigger(id=id)
