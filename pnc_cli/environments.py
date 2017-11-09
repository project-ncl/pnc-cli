import argparse

from argh import arg
from six import iteritems

import pnc_cli.cli_types as types
import pnc_cli.common as common
import pnc_cli.user_config as uc
import pnc_cli.utils as utils
from pnc_cli.swagger_client import BuildEnvironmentRest
from pnc_cli.swagger_client import EnvironmentsApi

envs_api = EnvironmentsApi(uc.user.get_api_client())

__author__ = 'thauser'


def create_environment_object(**kwargs):
    created_environment = BuildEnvironmentRest()
    for key, value in iteritems(kwargs):
        if value:
            setattr(created_environment, key, value)
    return created_environment


def valid_attribute(attributeInput):
    if attributeInput.count("=") == 0:
        raise argparse.ArgumentTypeError("Invalid attribute syntax. Correct syntax: key=value")
    attribute_key, attribute_value = attributeInput.split('=', 1)
    return {attribute_key: attribute_value}


def unique_iid(iidInput):
    response = utils.checked_api_call(envs_api, 'get_all', q='systemImageId==' + iidInput)
    if response.content:
        raise argparse.ArgumentTypeError("systemImageId is already in use")
    return iidInput


@arg("name", help="Unique name of the BuildEnvironment", type=types.unique_environment_name)
@arg("system_image_id", help="ID of the Docker image for this BuildEnvironment.", type=unique_iid)
@arg("system_image_type", help="One of DOCKER_IMAGE, VIRTUAL_MACHINE_RAW, VIRTUAL_MACHINE_QCOW2, LOCAL_WORKSPACE",
     choices=["DOCKER_IMAGE", "VIRTUAL_MACHINE_RAW", "VIRTUAL_MACHINE_QCOW2", "LOCAL_WORKSPACE"])
@arg("-d", "--description", help="Description of the BuildEnvironment.")
@arg("-a", "--attributes", help="Attributes of the BuildEnvironment. Syntax: Key=Value", type=valid_attribute)
@arg("-iru", "--image-repository-url", help="URL for the Docker repository in which the image resides.")
def create_environment(**kwargs):
    """
    Create a new Environment
    """
    environment = create_environment_object(**kwargs)
    response = utils.checked_api_call(envs_api, 'create_new', body=environment)
    if response:
        return utils.format_json(response.content)


@arg("id", help="ID of the environment to update.", type=types.existing_environment_id)
@arg("-s", "--system-image-type", help="Updated system image type for the new BuildEnvironment.")
@arg("-d", "--description", help="Updated description of the BuildEnvironment.")
@arg("-a", "--attributes", help="Attributes of the BuildEnvironment. Syntax: Key=Value", type=valid_attribute)
@arg("-iru", "--image-repository-url", help="Updated URL for the Docker repository in which the image resides.")
@arg("-n", "--name", help="Updated unique name of the BuildEnvironment", type=types.unique_environment_name)
def update_environment(id, **kwargs):
    """
    Update a BuildEnvironment with new information
    """
    to_update = envs_api.get_specific(id=id).content

    for key, value in iteritems(kwargs):
        if value:
            setattr(to_update, key, value)

    response = utils.checked_api_call(
        envs_api, 'update', id=id, body=to_update)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildEnvironment to delete.", type=types.existing_environment_id)
@arg("-n", "--name", help="Name of the BuildEnvironment to delete.", type=types.existing_environment_name)
def delete_environment(id=None, name=None):
    """
    Delete an environment by name or ID
    """
    found_id = common.set_id(envs_api, id, name)
    response = utils.checked_api_call(envs_api, 'delete', id=found_id)
    return response

def get_environment_raw(id=None, name=None):
    """
    Get a specific Environment by name or ID
    """
    search_id = common.set_id(envs_api, id, name)
    response = utils.checked_api_call(envs_api, 'get_specific', id=search_id)
    return response.content

@arg("-i", "--id", help="ID of the BuildEnvironment to retrieve.", type=types.existing_environment_id)
@arg("-n", "--name", help="Name of the BuildEnvironment to retrieve.", type=types.existing_environment_name)
def get_environment(id=None, name=None):
    """
    Get a specific Environment by name or ID
    """
    search_id = common.set_id(envs_api, id, name)
    response = utils.checked_api_call(envs_api, 'get_specific', id=search_id)
    return utils.format_json(response.content)


@arg("-p", "--page-size", help="Limit the amount of BuildEnvironments returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_environments(page_size=200, page_index=0, sort="", q=""):
    """
    List all Environments
    """
    response = utils.checked_api_call(envs_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)

