from pprint import pprint
import sys

from argh import arg

import swagger_client
from swagger_client.apis.environments_api import EnvironmentsApi
import utils

envs_api = EnvironmentsApi(utils.get_api_client())

__author__ = 'thauser'
def _create_environment_object(**kwargs):
    created_environment = swagger_client.EnvironmentRest()
    for key, value in kwargs.iteritems():
        setattr(created_environment, key, value.upper())
    return created_environment

def _environment_exists(search_id):
    existing_ids = [x.id for x in envs_api.get_all()]
    return search_id in existing_ids

@arg("build-type", help="Type of build for this build environment")
@arg("operating-system", help="Operating system for this build environment")
def create_environment(build_type, operating_system):
    """
    Create a new environment
    :param build_type: one of JAVA, DOCKER, NATIVE
    :param operating_system: one of WINDOWS, LINUX, OSX
    :return:
    """
    environment = _create_environment_object(build_type=build_type, operational_system=operating_system)
    envs_api.create_new(body=environment,callback=callback_function)

@arg("env-id", help="ID of the environment to replace")
@arg("-bt","--build-type", help="Type of build for the new environment")
@arg("-os","--operating-system", help="Operating system for the new environment")
#TODO: check provided parameters for membership of the enum (expose this type in the swagger docs?)
def update_environment(env_id, build_type=None, operating_system=None):
    """
    Replace an environment with ID env-id with a new environment
    :param env_id:
    :param build_type:
    :param operating_system:
    :return:
    """
    environment = _create_environment_object(build_type=build_type, operational_system=operating_system)
    if _environment_exists(env_id):
        envs_api.update(id=env_id, body=environment,callback=callback_function)
    else:
        print("No environment with id {0} exists.").format(env_id)

@arg("env-id", help="ID of the environment to delete")
def delete_environment(env_id):
    """
    Delete an environment by ID
    :param env_id:
    :return:
    """
    if not _environment_exists(env_id):
        print("No environment with id {0} exists.").format(env_id)
        return

    envs_api.delete(env_id,callback=callback_function)

@arg("id", help="ID of the environment to retrieve")
def get_environment(id):
    """
    Get a specific environment by ID
    :param id:
    :return:
    """
    envs_api.get_specific(id,callback=callback_function)

def list_environments():
    """
    List all environments
    :return:
    """
    envs_api.get_all(callback=callback_function)

def callback_function(response):
    if response:
        pprint(response.content)