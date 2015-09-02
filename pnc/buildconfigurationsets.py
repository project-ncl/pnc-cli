import sys

from argh import arg

import swagger_client
import utils
import buildconfigurations
import productversions
from swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi


def _create_build_config_set_object(**kwargs):
    created_build_config_set = swagger_client.models.build_configuration_set.BuildConfigurationSet()
    for key, value in kwargs.iteritems():
        setattr(created_build_config_set, key, value)
    return created_build_config_set

def get_build_config_set_id_by_name(search_name):
    response = get_all()
    for set in response.json():
        if set['name'] == search_name:
            return set['id']
    return None

def build_config_set_exists(search_id):
    return get_specific(search_id).ok

@arg("-a","--attributes", help="Comma separated list to specify attributes to print")
def list_build_configuration_sets(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_configuration_set.BuildConfigurationSet().attribute_map)

@arg("name", help="Name for the new build configuration set.")
@arg("-pvi", "--product-version-id", help="ID of the product version to associate this build configuration set.")
@arg("-bc", "--build-configurations", help="Comma separated list of build-configurations to include in the set.")
def create_build_config_set(name, product_version_id=None, build_configurations=None):
    build_configs = None

    if build_config_set_exists(get_build_config_set_id_by_name(name)):
        print("A build configuration set with name {0} already exists.").format(name)
        return

    if product_version_id and not productversions.version_exists(product_version_id):
        print("No product version with id {0} exists.".format(product_version_id))
        return

    if build_configurations:
        build_configs = build_configurations.split(',')
        failed = False
        for config in build_configs:
            if not buildconfigurations.build_configuration_exists(config):
                print("No build configuration with id {0} exists.".format(config))
                failed = True
        if failed:
            return

    config_set = _create_build_config_set_object(name, product_version_id, build_configs)

    response = create(config_set)
    utils.print_json_result(sys._getframe().f_code.co_name, response)

@arg("-id", "--id", help="ID of the build configuration set to retrieve")
@arg("-n", "--name", help="Name of the build configuration set to retrieve")
@arg("-a", "--attributes", help="Comma separated list of attributes to print")
def get_build_config_set(id=None, name=None, attributes=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    response = get_specific(set_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_configuration_set.BuildConfigurationSet().attribute_map)

@arg("-i", "--id", help="ID of the build configuration set to update.")
@arg("-n", "--name", help="Name for the build configuration set to update.")
@arg("-un", "--updated-name", help="Updated name for the build configuration set.")
@arg("-pvi", "--product-version-id", help="Updated product version ID for the build configuration set.")
@arg("-bc", "--build-configurations", help="Comma separated list of build configurations to include in the updated set.")
def update_build_config_set(id=None, name=None, updated_name=None, product_version_id=None, build_configurations=None):
    build_configs = None
    set_id = get_set_id(id,name)
    if not set_id:
        return

    if build_configurations:
        build_configs = build_configurations.split(',')

    updated_build_config_set = _create_build_config_set_object(name=updated_name, productVersionId=product_version_id, buildConfigurationIds=build_configs)
    response = update(set_id, updated_build_config_set)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return

    print("Update of build configuration set {0} successful").format(id)

@arg("-i", "--id", help="ID of the build configuration set to delete.")
@arg("-n", "--name", help="Name of the build configuration set to delete.")
#TODO: in order to delete a config set successfully, any buildconfigsetrecords must be deleted first
#TODO: it may be impossible / undesireable to remove buildconfigsetrecords. so perhaps just check and abort
def delete_build_config_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return

    response = delete_specific(set_id)

    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return

    print("Successfully deleted build configuration set with ID {0}.").format(set_id)

def get_set_id(id, name):
    if id:
        set_id = id
        if not build_config_set_exists(set_id):
            print("No build configuration set with ID {0} exists.").format(set_id)
            return
    elif name:
        set_id = get_build_config_set_id_by_name(name)
        if not build_config_set_exists(set_id):
            print("No build configuration set with name {0} exists.").format(name)
            return
    else:
        print("Either a build configuration set ID or name is required.")
        return
    return set_id

@arg("-i", "--id", help="ID of the build configuration set to build.")
@arg("-n", "--name", help="Name of the build configuration set to build.")
def build_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    #callbackUrl?
    response = trigger(set_id)
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name, response)
        return
    print("Successfully triggered build of build configuration set with ID {0}.").format(set_id)

@arg("-i", "--id", help="ID of the build configuration set to build.")
@arg("-n", "--name", help="Name of the build configuration set to build.")
@arg("-a", "--attributes", help="Comma separated list of attributes to print")
def list_build_configurations_for_set(id=None, name=None, attributes=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    response = get_configurations(set_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_configuration_set.BuildConfigurationSet().attribute_map)


@arg("-sid", "--set-id", help="ID of the build configuration set to add to")
@arg("-sn", "--set-name", help="Name of the build configuration set to add to")
@arg("-cid", "--config-id", help="ID of the build configuration to add to the given set")
@arg("-cn", "--config-name", help="Name of the build configuration to add to the given set")
def add_build_configuration_to_set(set_id=None, set_name=None, config_id=None, config_name=None):
    config_set_id = get_set_id(set_id,set_name)
    if not config_set_id:
        return

    build_config_id = buildconfigurations.get_config_id(config_id, config_name)
    if not build_config_id:
        return

    bc_response = buildconfigurations.get_specific(build_config_id)

    if not bc_response.ok:
        utils.print_error(sys._getframe().f_code.co_name,bc_response)
        return

    # todo: need to create a Configuration object here, not just pass json.
    bc = bc_response.json()

    response = add_configuration(config_set_id, bc)
    if not response.ok:
        utils.print_error(sys._getframe().f_code.co_name,response)
        return
    print("Build configuration successfully added to build configuration set.")

@arg("-i", "--id", help="ID of the build configuration set")
@arg("-n", "--name", help="name of the build configuration set")
@arg("-a", "--attributes", help="Comma separated list of attributes to print")
def list_build_records(id=None, name=None, attributes=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    response = get_build_records(set_id)
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.build_configuration_set.BuildConfigurationSet().attribute_map)
def get_all():
    return BuildconfigurationsetsApi(utils.get_api_client()).getAll()

def create(build_config_set):
    return BuildconfigurationsetsApi(utils.get_api_client()).createNew(body=build_config_set)

def get_specific(set_id):
    return BuildconfigurationsetsApi(utils.get_api_client()).getSpecific(id=set_id)

def update(set_id, updated_config_set):
    return BuildconfigurationsetsApi(utils.get_api_client()).update(id=set_id, body=updated_config_set)

def delete_specific(set_id):
    return BuildconfigurationsetsApi(utils.get_api_client()).deleteSpecific(id=set_id)

def trigger(set_id, callback_url=None):
    return BuildconfigurationsetsApi(utils.get_api_client()).build(id=set_id, callbackUrl=callback_url)

def get_configurations(set_id):
    return BuildconfigurationsetsApi(utils.get_api_client()).getConfigurations(id=set_id)

def add_configuration(set_id, build_configuration):
    return BuildconfigurationsetsApi(utils.get_api_client()).addConfiguration(id=set_id, body=build_configuration)

def get_build_records(set_id):
    return BuildconfigurationsetsApi(utils.get_api_client()).getBuildRecords(id=set_id)
