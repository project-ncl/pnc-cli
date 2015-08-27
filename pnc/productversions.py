from argh import arg
import client
from client.ProductversionsApi import ProductversionsApi
import utils

__author__ = 'thauser'

def create_product_version_object(version, product_id, current_milestone_id, product_milestones, build_config_sets, product_releases):
    """
    Create an instance of the ProductVersion object
    :param version:
    :param product_id:
    :param current_milestone_id:
    :param product_milestones:
    :param build_config_sets:
    :param product_releases:
    :return:
    """
    created_version = client.models.ProductVersion.ProductVersion()
    created_version.version = version
    if product_id: created_version.productId = product_id
    if current_milestone_id: created_version.currentProductMilestoneId = current_milestone_id
    if product_milestones: created_version.productMilestones = product_milestones
    if build_config_sets: created_version.buildConfigurationSetIds = build_config_sets
    if product_releases: created_version.productReleases = product_releases
    return created_version

def _version_exists(version_id):
    return ProductversionsApi(utils.get_api_client()).getSpecific(id=version_id).ok

@arg("-a","--attributes", help="Comma separated list of attributes to print for each product-version")
def list_product_versions(attributes=None):
    product_versions = ProductversionsApi(utils.get_api_client()).getAll().json()
    if attributes is not None:
        utils.print_matching_attribute(product_versions, attributes, client.models.ProductVersion.ProductVersion().attributeMap)
    else:
        utils.print_by_key(product_versions)


@arg("product-id", help="ID of product to add a version to")
@arg("version", help="Version to add")
@arg("-cm", "--current-milestone", help="ID of the milestone this version should be on")
@arg("-pm", "--product-milestones", help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-sets", help="List of build configuration set IDs to associate with the new version")
@arg("-pr", "--product-releases", help="List of release IDs to associate with this version")

def create_product_version(product_id, version, current_milestone=None, product_milestones=None, build_configuration_sets=None, product_releases=None):
    version = create_product_version_object(version, product_id, current_milestone, product_milestones, build_configuration_sets, product_releases)
    response = ProductversionsApi(utils.get_api_client()).createNewProductVersion(body=version)
    if not response.ok:
        utils.print_error(__name__,response)
        return

    new_version = response.json()
    utils.print_by_key(new_version)
    return new_version

# TODO: allow resolution / search by version
@arg("id", help="ID of the product version to retrieve")
def get_product_version(id):
    """
    List information about a specific product version
    :param id: the id of the product version
    :return:
    """
    if id:
        response = ProductversionsApi(utils.get_api_client()).getSpecific(id=id)
        if response.ok:
            print(utils.pretty_format_response(response.json()))
        else:
            print("A product version with id {0} doesn't exist.".format(id))
    else:
        print("A product version id is required")

# TODO: how should constraints be defined? Can a new productId be specified?
def update_product_version(id, version=None, current_product_milestone=None, product_milestones=None, build_config_sets=None, product_releases=None):
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
    if not _version_exists(id):
        print("A product version with id {0} doesn't exist.".format(id))
    else:
        version = create_product_version_object(version, current_product_milestone, product_milestones, build_config_sets, product_releases)
        response = ProductversionsApi(utils.get_api_client()).update(id=id, body=version)
        if response.ok:
            print("Update of version with id {0} successful.".format(id))
            print(response)
        else:
            utils.print_error(__name__,response)
            print(response)