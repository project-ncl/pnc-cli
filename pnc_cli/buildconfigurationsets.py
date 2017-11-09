from argh import arg
from six import iteritems

import json

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli import swagger_client
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
import pnc_cli.user_config as uc

sets_api = BuildconfigurationsetsApi(uc.user.get_api_client())
configs_api = BuildconfigurationsApi(uc.user.get_api_client())


def _create_build_config_set_object(**kwargs):
    created_build_config_set = swagger_client.BuildConfigurationSetRest()
    for key, value in iteritems(kwargs):
        setattr(created_build_config_set, key, value)
    return created_build_config_set


@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configuration_sets(page_size=200, page_index=0, sort="", q=""):
    """
    List all build configurtion sets
    """
    response = utils.checked_api_call(sets_api, 'get_all', page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)

def create_build_configuration_set_raw(**kwargs):
    """
    Create a new BuildConfigurationSet.
    """
    config_set = _create_build_config_set_object(**kwargs)
    response = utils.checked_api_call(sets_api, 'create_new', body=config_set)
    if response:
        return response.content

@arg("name", help="Name for the new BuildConfigurationSet.", type=types.unique_bc_set_name)
@arg("-pvi", "--product-version-id",
     help="ID of the product version to associate this BuildConfigurationSet.",
     type=types.existing_product_version)
@arg("-bcs", "--build-configuration-ids", type=types.existing_bc_id, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
def create_build_configuration_set(**kwargs):
    """
    Create a new BuildConfigurationSet.
    """
    content = create_build_configuration_set_raw(**kwargs)
    if content:
        return utils.format_json(content)

def get_build_configuration_set_raw(id=None, name=None):
    """
    Get a specific BuildConfigurationSet by name or ID
    """
    found_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'get_specific', id=found_id)
    if response:
        return response.content

@arg("-id", "--id", help="ID of the BuildConfigurationSet to retrieve", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to retrieve", type=types.existing_bc_set_name)
def get_build_configuration_set(id=None, name=None):
    """
    Get a specific BuildConfigurationSet by name or ID
    """
    content = get_build_configuration_set(id, name)
    if content:
        return utils.format_json(content)


@arg("id", help="ID of the BuildConfigurationSet to update.", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Updated name for the BuildConfigurationSet.", type=types.unique_bc_set_name)
@arg("-pvi", "--product-version-id",
     help="Updated product version ID for the BuildConfigurationSet.", type=types.existing_product_version)
@arg("-bcs", "--build-configuration-ids", type=types.existing_bc_id, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
def update_build_configuration_set(id, **kwargs):
    """
    Update a BuildConfigurationSet
    """
    set_to_update = utils.checked_api_call(sets_api, 'get_specific', id=id).content

    for key, value in kwargs.items():
        if value is not None:
            setattr(set_to_update, key, value)

    response = utils.checked_api_call(sets_api, 'update', id=id, body=set_to_update)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfigurationSet to delete.", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to delete.", type=types.existing_bc_set_name)
# TODO: in order to delete a config set successfully, any buildconfigsetrecords must be deleted first
# TODO: it may be impossible / undesireable to remove
# buildconfigsetrecords. so perhaps just check and abort
def delete_build_configuration_set(id=None, name=None):
    set_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'delete_specific', id=set_id)
    if response:
        return utils.format_json(response.content)

def build_set_raw(id=None, name=None, force = False):
    """
    Start a build of the given BuildConfigurationSet
    """
    found_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'build', id=found_id, rebuild_all=force)
    if response:
        return response.content

@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.", type=types.existing_bc_set_name)
@arg("-f", "--force", help="Force rebuild of all configurations")
def build_set(id=None, name=None, force=False):
    """
    Start a build of the given BuildConfigurationSet
    """
    content = build_set_raw(id, name, force)
    if common:
        return utils.format_json_list(content)


@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.", type=types.existing_bc_set_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_set(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all build configurations in a given BuildConfigurationSet.
    """
    found_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'get_configurations', id=found_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-sid", "--set-id", help="ID of the BuildConfigurationSet to add to", type=types.existing_bc_set_id)
@arg("-sn", "--set-name", help="Name of the BuildConfigurationSet to add to", type=types.existing_bc_set_name)
@arg("-cid", "--config-id",
     help="ID of the build configuration to add to the given set", type=types.existing_bc_id)
@arg("-cn", "--config-name",
     help="Name of the build configuration to add to the given set", type=types.existing_bc_name)
def add_build_configuration_to_set(
        set_id=None, set_name=None, config_id=None, config_name=None):
    """
    Add a build configuration to an existing BuildConfigurationSet
    """
    config_set_id = common.set_id(sets_api, set_id, set_name)
    bc_id = common.set_id(configs_api, config_id, config_name)
    bc = common.get_entity(configs_api, bc_id)
    response = utils.checked_api_call(
        sets_api,
        'add_configuration',
        id=config_set_id,
        body=bc)
    if response:
        return utils.format_json(response.content)


@arg("-sid", "--set-id", help="ID of the BuildConfigurationSet to remove from", type=types.existing_bc_set_id)
@arg("-sn", "--set-name", help="Name of the BuildConfigurationSet to remove from", type=types.existing_bc_set_name)
@arg("-cid", "--config-id", help="ID of the BuildConfiguration to remove from the set",
     type=types.existing_bc_id)
@arg("-cn", "--config-name", help="Name of the BuildConfiguration to remove from the set",
     type=types.existing_bc_name)
def remove_build_configuration_from_set(set_id=None, set_name=None, config_id=None, config_name=None):
    config_set_id = common.set_id(sets_api, set_id, set_name)
    bc_id = common.set_id(configs_api, config_id, config_name)
    response = utils.checked_api_call(
        sets_api,
        'remove_configuration',
        id=config_set_id,
        config_id=bc_id)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the BuildConfigurationSet", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet", type=types.existing_bc_set_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records_for_set(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all build records for a BuildConfigurationSet
    """
    found_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'get_build_records', id=found_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfigurationSet", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet", type=types.existing_bc_set_name)
@arg("-p", "--page-size", help="Limit the amount of build records returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_set_records(id=None, name=None, page_size=200, page_index=0, sort="", q=""):
    """
    List all build set records for a BuildConfigurationSet
    """
    found_id = common.set_id(sets_api, id, name)
    response = utils.checked_api_call(sets_api, 'get_all_build_config_set_records', id=found_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return utils.format_json_list(response.content)


@arg("-i", "--id", help="ID of the BuildConfigurationSet", type=types.existing_bc_set_id)
@arg("-n", "--name", help="Name of the BuildConfigurationSet", type=types.existing_bc_set_name)
def latest_build_set_records_status(id=None, name=None):
    """
    List latest build set record status
    """
    data = list_build_set_records(id, name)
    data_json = json.loads(data)
    if len(data_json) > 0:
        data_json.sort(key=lambda obj: obj['id'], reverse=True)
        return "Build Config Set Record #" + str(data_json[0]['id']) + ": " + data_json[0]['status']
