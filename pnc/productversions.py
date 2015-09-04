from pprint import pprint
import sys

from argh import arg

import swagger_client
from swagger_client.apis.productversions_api import ProductversionsApi
import utils


versions_api = ProductversionsApi(utils.get_api_client())

__author__ = 'thauser'

def create_product_version_object(**kwargs):
    created_version = swagger_client.models.product_version.ProductVersion()
    for key, value in kwargs.iteritems():
        setattr(created_version, key, value)
    return created_version

def version_exists(id):
    version_ids = [str(x.id) for x in versions_api.get_all().content]
    return id in version_ids

def list_product_versions():
    versions_api.get_all(callback=callback_function)

@arg("product_id", help="ID of product to add a version to")
@arg("version", help="Version to add")
@arg("-cm", "--current-product-milestone-id", help="ID of the milestone this version should be on")
@arg("-pr", "--product-releases", type=int, nargs="+", help="List of product release IDs for this Product version")
@arg("-pm", "--product-milestones", type=int, nargs="+", help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=int, nargs="+", help="List of build configuration set IDs to associate with the new version")
def create_product_version(**kwargs):
    version = create_product_version_object(**kwargs)
    versions_api.create_new_product_version(body=version, callback=callback_function)

@arg("id", help="ID of the product version to retrieve")
def get_product_version(id, attributes=None):
    """
    List information about a specific product version
    :param id: the id of the product version
    :return:
    """
    if id:
        versions_api.get_specific(id=id, callback=callback_function)
    else:
        print("A product version id is required")


# TODO: how should constraints be defined? Can a new productId be specified?
@arg("product-id", help="ID of product to add a version to")
@arg("-v", "--version", help="Version to add")
@arg("-cm", "--current-product-milestone-id", help="ID of the milestone this version should be on")
@arg("-pr", "--product-releases", type=int, nargs="+", help="List of product release IDs for this Product version")
@arg("-pm", "--product-milestones", type=int, nargs="+", help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=int, nargs="+", help="List of build configuration set IDs to associate with the new version")
def update_product_version(id, **kwargs):
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

    updated_version = create_product_version_object(**kwargs)
    versions_api.update(id=id, body=updated_version, callback=callback_function)

def callback_function(response):
    if response:
        pprint(response)
