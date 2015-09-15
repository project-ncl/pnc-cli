from pprint import pprint
import sys

from argh import arg

import swagger_client
import utils
import buildconfigurations
import productversions
from swagger_client.apis.buildconfigurationsets_api import BuildconfigurationsetsApi
from swagger_client.apis.buildconfigurations_api import BuildconfigurationsApi

sets_api = BuildconfigurationsetsApi(utils.get_api_client())
configs_api = BuildconfigurationsApi(utils.get_api_client())

def _create_build_config_set_object(**kwargs):
    created_build_config_set = swagger_client.models.build_configuration_set.BuildConfigurationSet()
    for key, value in kwargs.iteritems():
        setattr(created_build_config_set, key, value)
    return created_build_config_set

def get_build_config_set_id_by_name(search_name):
    response = sets_api.get_all()
    for set in response.json():
        if set.name == search_name:
            return set.id
    return None

@arg("-a","--attributes", help="Comma separated list to specify attributes to print")
def list_build_configuration_sets():
    sets_api.get_all(callback=callback_function)

@arg("name", help="Name for the new build configuration set.")
@arg("-pvi", "--product-version-id", help="ID of the product version to associate this build configuration set.")
@arg("-bcs", "--build-configurations", type=int, nargs='+', help="Space separated list of build-configurations to include in the set.")
def create_build_config_set(name, product_version_id=None, build_configurations=None):
    build_configs = None

    if get_build_config_set_id_by_name(name):
        print("A build configuration set with name {0} already exists.").format(name)
        return

    if product_version_id and not productversions.version_exists(product_version_id):
        print("No product version with id {0} exists.".format(product_version_id))
        return

    if build_configurations:
        failed = False
        for config in build_configs:
            if not buildconfigurations.config_id_exists(config):
                print("No build configuration with id {0} exists.".format(config))
                failed = True
        if failed:
            return

    config_set = _create_build_config_set_object(name, product_version_id, build_configs)
    sets_api.create(config_set, callback=callback_function)

@arg("-id", "--id", help="ID of the build configuration set to retrieve")
@arg("-n", "--name", help="Name of the build configuration set to retrieve")
def get_build_config_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    sets_api.get_specific(id=set_id, callback=callback_function)

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
    sets_api.update(id=set_id, body=updated_build_config_set, callback=callback_function)

@arg("-i", "--id", help="ID of the build configuration set to delete.")
@arg("-n", "--name", help="Name of the build configuration set to delete.")
#TODO: in order to delete a config set successfully, any buildconfigsetrecords must be deleted first
#TODO: it may be impossible / undesireable to remove buildconfigsetrecords. so perhaps just check and abort
def delete_build_config_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    sets_api.delete_specific(id=set_id, callback=callback_function)

def _set_exists(id):
    existing_ids = [str(x.id) for x in sets_api.get_all().content]
    return id in existing_ids

def get_set_id(set_id, name):
    if set_id:
       if not _set_exists(set_id):
           print("There is no build configuration set with ID {}.").format(set_id)
           return
    elif name:
        set_id = get_build_config_set_id_by_name(name)
        if not set_id:
            print("There is no build configuration set with name {}.").format(name)
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
    sets_api.build(id=set_id,callback=callback_function)

@arg("-i", "--id", help="ID of the build configuration set to build.")
@arg("-n", "--name", help="Name of the build configuration set to build.")
def list_build_configurations_for_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    sets_api.get_configurations(id=set_id, callback=callback_function)

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
    bc = configs_api.get_specific(build_config_id)
    sets_api.add_configuration(id=config_set_id, body=bc, callback=callback_function)

@arg("-i", "--id", help="ID of the build configuration set")
@arg("-n", "--name", help="name of the build configuration set")
def list_build_records_for_set(id=None, name=None):
    set_id = get_set_id(id,name)
    if not set_id:
        return
    sets_api.get_build_records(id=set_id,callback=callback_function)

def callback_function(response):
    if response:
        pprint(response.content)