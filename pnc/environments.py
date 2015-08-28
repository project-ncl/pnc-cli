from argh import arg
import sys
import client
from client.EnvironmentsApi import EnvironmentsApi
import utils

__author__ = 'thauser'
def _create_environment_object(build_type, operational_system):
    created_environment = client.models.Environment.Environment()
    if build_type: created_environment.buildType = build_type.upper()
    if operational_system: created_environment.operationalSystem = operational_system.upper()
    return created_environment


def _environment_exists(search_id):
    response = get_specific(search_id)
    if response.ok:
        return True
    return False

@arg("build-type", help="Type of build for this build environment")
@arg("operating-system", help="Operating system for this build environment")
def create_environment(build_type, operating_system):
    environment = _create_environment_object(build_type, operating_system)
    response = create(environment)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return
    new_env = response.json()
    utils.print_by_key(new_env)

@arg("env-id", help="ID of the environment to replace")
@arg("-bt","--build-type", help="Type of build for the new environment")
@arg("-os","--operating-system", help="Operating system for the new environment")
#TODO: check provided parameters for membership of the enum (expose this type in the swagger docs?)
def update_environment(env_id, build_type=None, operating_system=None):
    environment = _create_environment_object(build_type, operating_system)
    if _environment_exists(env_id):
        response = update(env_id, environment)
        if response.ok:
            print("Successfully updated environment {0}.").format(env_id)
        else:
            print("Updating environment {0} failed.").format(env_id)
    else:
        print("No environment with id {0} exists.").format(env_id)

@arg("env-id", help="ID of the environment to delete")
def delete_environment(env_id):
    if not _environment_exists(env_id):
        print("No environment with id {0} exists.").format(env_id)
        return
    response = delete(env_id)
    if response.ok:
        print("Environment {0} successfully deleted.")
    else:
        utils.print_error(sys._getframe().f_code.co_name,response)

@arg("-i", "--id", help="ID of the environment to retrieve")
@arg("-n", "--name", help="ID of the environment to retrieve")
def get_environment(name=None, id=None):
    response = get_specific(id)
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return
    env = response.json();
    utils.print_by_key(env)

@arg("-a", "--attributes", help="Comma separated list of attributes to return about each environment")
def list_environments(attributes=None):
    response = get_all()
    if not response.ok:
        utils.print_error("list_environments",response)
        return
    environments = response.json()
    if attributes is not None:
        utils.print_matching_attribute(environments, attributes, client.models.Environment.Environment().attributeMap)
    else:
        utils.print_by_key(environments)

def get_all():
    return EnvironmentsApi(utils.get_api_client()).getAll()

def get_specific(env_id):
    return EnvironmentsApi(utils.get_api_client()).getSpecific(id=env_id)

def create(environment):
    return EnvironmentsApi(utils.get_api_client()).createNew(body=environment)

def delete(env_id):
    return EnvironmentsApi(utils.get_api_client()).delete(id=env_id)

def update(env_id, environment):
    return EnvironmentsApi(utils.get_api_client()).update(id=env_id,body=environment)