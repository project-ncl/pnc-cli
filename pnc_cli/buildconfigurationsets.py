from argh import arg
from six import iteritems

import logging
from pnc_cli import swagger_client
from pnc_cli import utils
from pnc_cli import buildconfigurations
from pnc_cli import productversions
from pnc_cli.swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from pnc_cli.swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi

sets_api = BuildconfigurationsetsApi(utils.get_api_client())
configs_api = BuildconfigurationsApi(utils.get_api_client())


def _create_build_config_set_object(**kwargs):
    created_build_config_set = swagger_client.BuildConfigurationSetRest()
    for key, value in iteritems(kwargs):
        setattr(created_build_config_set, key, value)
    return created_build_config_set


def get_build_config_set_id_by_name(search_name):
    sets = sets_api.get_all().content
    for set in sets:
        if set.name == search_name:
            return set.id
    return None


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configuration_sets(page_size=200, sort="", q=""):
    """
    List all build configurtion sets
    """
    response = utils.checked_api_call(sets_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("name", help="Name for the new BuildConfigurationSet.")
@arg("-pvi", "--product-version-id",
     help="ID of the product version to associate this BuildConfigurationSet.")
@arg("-bcs", "--build-configuration_ids", type=int, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
def create_build_configuration_set(**kwargs):
    """
    Create a new BuildConfigurationSet.
    """
    name = kwargs.get('name')
    if get_build_config_set_id_by_name(name):
        logging.error("A BuildConfigurationSet with name {0} already exists.".format(
            name))
        return

    version_id = kwargs.get('product_version_id')
    if version_id and not productversions.version_exists(version_id):
        logging.error("No ProductVersion with id {0} exists.".format(version_id))
        return

    build_configurations = kwargs.get('build_configuration_ids')
    failed = False
    if build_configurations:
        for config in build_configurations:
            if not buildconfigurations.config_id_exists(config):
                logging.error(
                    "No BuildConfiguration with id {0} exists.".format(config))
                failed = True
    if failed:
        return

    config_set = _create_build_config_set_object(**kwargs)
    response = utils.checked_api_call(sets_api, 'create_new', body=config_set)
    if response:
        return response.content


@arg("-id", "--id", help="ID of the BuildConfigurationSet to retrieve")
@arg("-n", "--name", help="Name of the BuildConfigurationSet to retrieve")
def get_build_configuration_set(id=None, name=None):
    """
    Get a specific BuildConfigurationSet by name or ID
    """
    found_id = get_set_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(sets_api, 'get_specific', id=found_id)
    if response:
        return response.content


@arg("id", help="ID of the BuildConfigurationSet to update.")
@arg("-n", "--name", help="Updated name for the BuildConfigurationSet.")
@arg("-pvi", "--product-version-id",
     help="Updated product version ID for the BuildConfigurationSet.")
@arg("-bcs", "--build-configuration_ids", type=int, nargs='+',
     help="Space separated list of build-configurations to include in the set.")
# TODO: seems like a bug in PNC prevents us from updating the buildconfigurationset
def update_build_configuration_set(id, **kwargs):
    """
    Update a BuildConfigurationSet
    """
    invalid_bcs = False
    if not get_set_id(id, None):
        return
    set_to_update = utils.checked_api_call(sets_api, 'get_specific', id=id).content

    pvi = kwargs.get('product_version_id')
    if pvi and not productversions.get_product_version(id=pvi):
        logging.error("There is no ProductVersion with ID {}".format(pvi))
        return

    bc_ids = kwargs.get('build_configuration_ids')

    if bc_ids:
        for id in bc_ids:
            if not buildconfigurations.get_build_configuration(id=id):
                logging.error("There is no BuildConfiguration with ID {}".format(id))
                invalid_bcs = True

    if invalid_bcs:
        logging.error("Attempted to add non-existing BuildConfigurations to BuildConfigurationSet.")
        return

    for key, value in kwargs.items():
        if value is not None:
            setattr(set_to_update, key, value)

    response = utils.checked_api_call(sets_api, 'update', id=id, body=set_to_update)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet to delete.")
@arg("-n", "--name", help="Name of the BuildConfigurationSet to delete.")
# TODO: in order to delete a config set successfully, any buildconfigsetrecords must be deleted first
# TODO: it may be impossible / undesireable to remove
# buildconfigsetrecords. so perhaps just check and abort
def delete_build_config_set(id=None, name=None):
    set_id = get_set_id(id, name)
    if not set_id:
        return
    response = utils.checked_api_call(sets_api, 'delete_specific', id=set_id)
    if response:
        return response.content


def _set_exists(id):
    existing_ids = [str(x.id) for x in sets_api.get_all().content]
    return str(id) in existing_ids


def get_set_id(set_id, name):
    if set_id:
        if not _set_exists(set_id):
            logging.error("There is no BuildConfigurationSet with ID {}.".format(set_id))
            return
    elif name:
        set_id = get_build_config_set_id_by_name(name)
        if not set_id:
            logging.error("There is no BuildConfigurationSet with name {}.".format(name))
            return
    else:
        logging.error("Either a BuildConfigurationSet ID or name is required.")
        return
    return set_id


@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.")
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.")
def build_set(id=None, name=None):
    """
    Start a build of the given BuildConfigurationSet
    """
    found_id = get_set_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(sets_api, 'build', id=found_id)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet to build.")
@arg("-n", "--name", help="Name of the BuildConfigurationSet to build.")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_configurations_for_set(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all build configurations in a given BuildConfigurationSet.
    """
    found_id = get_set_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(sets_api, 'get_configurations', id=id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


@arg("-sid", "--set-id", help="ID of the BuildConfigurationSet to add to")
@arg("-sn", "--set-name", help="Name of the BuildConfigurationSet to add to")
@arg("-cid", "--config-id",
     help="ID of the build configuration to add to the given set")
@arg("-cn", "--config-name",
     help="Name of the build configuration to add to the given set")
def add_build_configuration_to_set(
        set_id=None, set_name=None, config_id=None, config_name=None):
    """
    Add a build configuration to an existing BuildConfigurationSet
    """
    config_set_id = get_set_id(set_id, set_name)
    if not config_set_id:
        return
    bc_id = buildconfigurations.get_config_id(config_id, config_name)
    if not bc_id:
        return
    bc = configs_api.get_specific(id=bc_id).content
    response = utils.checked_api_call(
        sets_api,
        'add_configuration',
        id=config_set_id,
        body=bc)
    if response:
        return response.content


@arg("-i", "--id", help="ID of the BuildConfigurationSet")
@arg("-n", "--name", help="Name of the BuildConfigurationSet")
@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_build_records_for_set(id=None, name=None, page_size=200, sort="", q=""):
    """
    List all build records for a BuildConfigurationSet
    """
    found_id = get_set_id(id, name)
    if not found_id:
        return
    response = utils.checked_api_call(sets_api, 'get_build_records', id=found_id, page_size=page_size, sort=sort, q=q)
    if response:
        return response.content
