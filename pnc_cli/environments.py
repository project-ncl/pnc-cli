import logging
from argh import arg

from six import iteritems
from pnc_cli.swagger_client import BuildEnvironmentRest
from pnc_cli.swagger_client import EnvironmentsApi
from pnc_cli import utils
import string
import argparse

envs_api = EnvironmentsApi(utils.get_api_client())

__author__ = 'thauser'


def _create_environment_object(**kwargs):
    created_environment = BuildEnvironmentRest()
    for key, value in iteritems(kwargs):
        if value:
            setattr(created_environment, key, value)
    return created_environment

def _environment_exists(id):
    response = utils.checked_api_call(envs_api, 'get_specific', id=str(id))
    if not response:
        return False
    return True


def _get_environment_id_by_name(name):
    """
    Return the ID of a BuildEnvironment given the name
    """
    response = utils.checked_api_call(envs_api, 'get_all', q='name==' + name)
    if not response:
        return None
    else:
        return response.content[0].id

def get_environment_id(search_id, name):
    """
    Given either a name or id, checks for BuildEnvironment existence and returns the valid id, or prints a message otherwise
    """
    if search_id:
        found_env = utils.checked_api_call(envs_api, 'get_specific', id=str(search_id))
        if not found_env:
            logging.error("No environment with ID {} exists.".format(search_id))
            return
        found_id = search_id
    elif name:
        found_id = _get_environment_id_by_name(name)
        if not found_id:
            logging.error("No environment with name {} exists.".format(name))
            return
    else:
        print("Either a BuildEnvironment name or ID is required.")
        return
    return found_id

def _valid_sys_type(sysTypeInput):
    VALID_TYPES=["DOCKER_IMAGE", "VIRTUAL_MACHINE_RAW", "VIRTUAL_MACHINE_QCOW2", "LOCAL_WORKSPACE"]
    sysCaps = sysTypeInput.upper()
    if sysCaps not in VALID_TYPES:
        raise argparse.ArgumentTypeError("Invalid system image type")
    return sysCaps


def _valid_attribute(attributeInput):
    if(attributeInput.count("=") == 0):
        raise argparse.ArgumentTypeError("Invalid attribute syntax. Correct syntax: key=value")
    attribute_key, attribute_value = attributeInput.split('=',1)
    return {attribute_key:attribute_value}


def _unique_iid(iidInput):
    response = utils.checked_api_call(envs_api, 'get_all', q='systemImageId=='+iidInput)
    if response.content:
        raise argparse.ArgumentTypeError("imageId is already in use")
    return iidInput


def _unique_name(nameInput):
    response = utils.checked_api_call(envs_api, 'get_all', q='name=='+nameInput)
    if response.content:
        raise argparse.ArgumentTypeError("name is already in use")
    return nameInput


@arg("name", help="Unique name of the BuildEnvironment", type=_unique_name)
@arg("image_id", help="ID of the Docker image for this BuildEnvironment.", type=_unique_iid)
@arg("system_image_type", help="One of DOCKER_IMAGE, VIRTUAL_MACHINE_RAW, VIRTUAL_MACHINE_QCOW2, LOCAL_WORKSPACE",type=_valid_sys_type)
@arg("-d", "--description", help="Description of the BuildEnvironment.")
@arg("-a", "--attributes", help="Attributes of the BuildEnvironment. Syntax: Key=Value", type=_valid_attribute)
@arg("-iru", "--image-repository-url", help="URL for the Docker repository in which the image resides.")
def create_environment(**kwargs):
    """
    Create a new Environment
    """
    environment = _create_environment_object(**kwargs)
    response = utils.checked_api_call(envs_api, 'create_new', body=environment)
    if response:
        return response.content


@arg("id", help="ID of the environment to update.")
@arg("-bt", "--system-image-type", help="Updated system image type for the new BuildEnvironment.", type=_valid_attribute)
@arg("-d", "--description", help="Updated description of the BuildEnvironment.")
@arg("-a", "--attributes", help="Attributes of the BuildEnvironment. Syntax: Key=Value", type=_valid_attribute)
@arg("-iru", "--image-repository-url", help="Updated URL for the Docker repository in which the image resides.")
@arg("-n", "--name", help="Updated unique name of the BuildEnvironment", type=_unique_name)
def update_environment(id, **kwargs):
    """
    Update a BuildEnvironment with new information
    """
    if not _environment_exists(id):
        print("No environment with id {} exists.".format(id))
        return

    to_update = envs_api.get_specific(id=id).content

    for key, value in iteritems(kwargs):
        if value:
            setattr(to_update, key, value)

    response = utils.checked_api_call(
        envs_api, 'update', id=id, body=to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the environment to delete.")
@arg("-n", "--name", help="Name of the environment to delete.")
def delete_environment(id=None, name=None):
    """
    Delete an environment by name or ID
    """
    found_id = get_environment_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(envs_api, 'delete', id=found_id)
    return response


@arg("-i", "--id", help="ID of the environment to retrieve.")
@arg("-n", "--name", help="Name of the environment to retrieve.")
def get_environment(id=None, name=None):
    """
    Get a specific Environment by name or ID
    """
    search_id = get_environment_id(id, name)
    if not search_id:
        return
    response = utils.checked_api_call(envs_api, 'get_specific', id=search_id)
    if response:
        return response.content


@arg("-p", "--page-size", help="Limit the amount of product releases returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_environments(page_size=200, sort="", q=""):
    """
    List all Environments
    """
    response = utils.checked_api_call(envs_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
