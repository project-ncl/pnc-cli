from pprint import pprint
import sys

from argh import arg

import swagger_client
from swagger_client.apis.productversions_api import ProductversionsApi
from swagger_client.apis.products_api import ProductsApi
import utils

versions_api = ProductversionsApi(utils.get_api_client())
products_api = ProductsApi(utils.get_api_client())

__author__ = 'thauser'


def create_product_version_object(**kwargs):
    created_version = swagger_client.ProductVersionRest()
    for key, value in kwargs.iteritems():
        setattr(created_version, key, value)
    return created_version


def version_exists(id):
    version_ids = [str(x.id) for x in versions_api.get_all().content]
    return id in version_ids


def version_exists_for_product(id, version):
    return version in [x.version for x in [
        y for y in products_api.get_product_versions(id=id).content]]


def list_product_versions():
    """
    List all ProductVersions
    """
    response = utils.checked_api_call(versions_api, 'get_all')
    if response: return response.content


@arg("product_id", help="ID of product to add a version to")
@arg("version", help="Version to add")
@arg("-cm", "--current-product-milestone-id",
     help="ID of the milestone this version should be on")
@arg("-pr", "--product-releases", type=int, nargs="+",
     help="List of product release IDs for this Product version")
@arg("-pm", "--product-milestones", type=int, nargs="+",
     help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=int, nargs="+",
     help="List of build configuration set IDs to associate with the new version")
def create_product_version(product_id, version, **kwargs):
    """
    Create a new ProductVersion
    """
    if version_exists_for_product(product_id, version):
        print("Version {} already exists for product: {}").format(
            version, products_api.get_specific(id=product_id).content.name)
        return
    kwargs['product_id'] = product_id
    kwargs['version'] = version
    product_version = create_product_version_object(**kwargs)
    response = utils.checked_api_call(versions_api, 'create_new_product_version',
                                      body=product_version)
    if response: return response.content


@arg("id", help="ID of the product version to retrieve")
def get_product_version(id):
    """
    Get a specific ProductVersion by ID
    """
    response = utils.checked_api_call(versions_api, 'get_specific', id=id)
    if response: return response.content


# TODO: how should constraints be defined? Can a new productId be specified?
@arg("-pid", "--product-id", help="ID of product to add a version to")
@arg("-v", "--version", help="Version to add")
@arg("-cm", "--current-product-milestone-id", type=int,
     help="ID of the ProductMilestone this version should be on")
@arg("-pr", "--product-releases", type=int, nargs="+",
     help="List of ProductRelease IDs for this Product version")
@arg("-pm", "--product-milestones", type=int, nargs="+",
     help="List of ProductMilestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=int, nargs="+",
     help="List of BuildConfigurationSet IDs to associate with the new version")
def update_product_version(id, **kwargs):
    """
    Update the ProductVersion with the given ID with new values.
    """
    if not version_exists(id):
        print("A product version with id {} doesn't exist.".format(id))
        return

    to_update = versions_api.get_specific(id=id).content
    for key,value in kwargs.items():
        if value is not None:
            setattr(to_update, key, value)
    response = utils.checked_api_call(versions_api, 'update',
        id=id,
        body=to_update)
    if response:
        return response.content