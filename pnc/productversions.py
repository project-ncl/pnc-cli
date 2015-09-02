import sys

from argh import arg

import swagger_client
from swagger_client.apis.productversions_api import ProductversionsApi
import utils


__author__ = 'thauser'

def create_product_version_object(**kwargs):
    created_version = swagger_client.models.product_version.ProductVersion()
    for key, value in kwargs.iteritems():
        setattr(created_version, key, value)
    return created_version

def version_exists(version_id):
    return get_specific(version_id).ok

@arg("-a", "--attributes", help="Comma separated list of attributes to print for each product-version")
def list_product_versions(attributes=None):
    response = get_all()
    utils.print_json_result(sys._getframe().f_code.co_name,
                            response,
                            attributes,
                            swagger_client.models.product_version.ProductVersion().attribute_map)

@arg("product-id", help="ID of product to add a version to")
@arg("version", help="Version to add")
@arg("-cm", "--current-milestone", help="ID of the milestone this version should be on")
@arg("-pm", "--product-milestones", help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-sets", help="List of build configuration set IDs to associate with the new version")
@arg("-pr", "--product-releases", help="List of release IDs to associate with this version")
def create_product_version(product_id, version, current_milestone=None, product_milestones=None,
                           build_configuration_sets=None, product_releases=None):
    version = create_product_version_object(version, product_id, current_milestone, product_milestones,
                                            build_configuration_sets, product_releases)
    response = create(version)
    utils.print_json_result(sys._getframe().f_code.co_name,response)

# TODO: allow resolution / search by version
@arg("id", help="ID of the product version to retrieve")
@arg("-a", "--attributes", help="Comma separated list of attributes to print.")
def get_product_version(id, attributes=None):
    """
    List information about a specific product version
    :param id: the id of the product version
    :return:
    """
    if id:
        response = get_specific(id)
        utils.print_json_result(sys._getframe().f_code.co_name,
                                response,
                                attributes,
                                swagger_client.models.product_version.ProductVersion().attribute_map)
    else:
        print("A product version id is required")


# TODO: how should constraints be defined? Can a new productId be specified?
def update_product_version(id, version=None, current_product_milestone=None, product_milestones=None,
                           build_config_sets=None, product_releases=None):
    """
    Replace the product version with id with a new product version with provided values
    :param id: id of ProductVersion to replace
    :param version: new version
    :param product_id: new product to associate with
    :param current_product_milestone: new milestone
    :param product_milestones: list of product milestone ids
    :param build_config_sets: list of build configuration set ids
    :param product_releases: list of product release ids
    :return:
    """
    if not version_exists(id):
        print("A product version with id {0} doesn't exist.".format(id))
        return

    updated_version = create_product_version_object(version, current_product_milestone, product_milestones,
                                            build_config_sets, product_releases)
    response = update(id, updated_version)
    if not response.ok:
        utils.print_json_result(sys._getframe().f_code.co_name,response)
        return

    print("Update of version with id {0} successful.".format(id))

def get_all():
    return ProductversionsApi(utils.get_api_client()).getAll()

def get_specific(version_id):
    return ProductversionsApi(utils.get_api_client()).getSpecific(id=version_id)

def create(version):
    return ProductversionsApi(utils.get_api_client()).createNewProductVersion(body=version)

def update(version_id, version):
    return ProductversionsApi(utils.get_api_client()).update(id=version_id, body=version)

#not implemented in rest
def delete():
    pass

