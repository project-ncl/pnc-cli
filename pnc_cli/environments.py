from pprint import pprint

from argh import arg

import swagger_client
from swagger_client.apis.environments_api import EnvironmentsApi
import utils

envs_api = EnvironmentsApi(utils.get_api_client())

__author__ = 'thauser'
def _create_environment_object(**kwargs):
    created_environment = swagger_client.EnvironmentRest
    for key, value in kwargs.iteritems():
        setattr(created_environment, key, value.upper())
    return created_environment

def _environment_exists(search_id):
    existing_ids = [str(x.id) for x in envs_api.get_all().content]
    return str(search_id) in existing_ids

@arg("build-type", help="Type of build for this build environment. Allowed values: JAVA, DOCKER, NATIVE")
@arg("operational-system", help="Operating system for this build environment. Allowed values: WINDOWS, LINUX, OSX")
def create_environment(**kwargs):
    """
    Create a new Environment
    """
    environment = _create_environment_object(**kwargs)
    response = utils.checked_api_call(envs_api, 'create_new', body=environment)
    if response: return response.content

@arg("env-id", help="ID of the environment to replace")
@arg("-bt","--build-type", help="Type of build for the new environment")
@arg("-os","--operational-system", help="Operating system for the new environment")
def update_environment(env_id, **kwargs):
    """
    Replace an Environment with a new Environment
    """
    environment = _create_environment_object(**kwargs)
    if not _environment_exists(env_id):
        print("No environment with id {0} exists.").format(env_id)
        return
    response = utils.checked_api_call(envs_api, 'update', id=env_id, body=environment)
    if response: return response.content

@arg("env-id", help="ID of the environment to delete")
def delete_environment(env_id):
    """
    Delete an environment by ID
    """
    if not _environment_exists(env_id):
        print("No environment with id {0} exists.").format(env_id)
        return
    response = utils.checked_api_call(envs_api,'delete', id=env_id)
    return response

@arg("id", help="ID of the environment to retrieve.")
def get_environment(id):
    """
    Get a specific Environment by ID
    """
    response = utils.checked_api_call(envs_api,'get_specific',id=id)
    if response: return response.content

def list_environments():
    """
    List all Environments
    """
    response = utils.checked_api_call(envs_api,'get_all')
    if response: return response.content