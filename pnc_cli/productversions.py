from argh import arg
from six import iteritems

import logging
from pnc_cli import swagger_client
from pnc_cli.swagger_client.apis.productversions_api import ProductversionsApi
from pnc_cli.swagger_client.apis.products_api import ProductsApi
from pnc_cli import utils

versions_api = ProductversionsApi(utils.get_api_client())
products_api = ProductsApi(utils.get_api_client())

__author__ = 'thauser'


def create_product_version_object(**kwargs):
    created_version = swagger_client.ProductVersionRest()
    for key, value in iteritems(kwargs):
        setattr(created_version, key, value)
    return created_version


def version_exists(id):
    response = utils.checked_api_call(versions_api, 'get_all', q='id=='+str(id))
    if not response:
        return False
    return True


def version_exists_for_product(id, version):
    existing_products = products_api.get_product_versions(id=id).content
    if existing_products:
        return version in [x.version for x in existing_products]
    else:
        return False


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_versions(page_size=200, sort="", q=""):
    """
    List all ProductVersions
    """
    response = utils.checked_api_call(versions_api, 'get_all', page_size=page_size, sort=sort, q=q)
    if response:
        return response.content


# TODO: Version needs to be checked for validity.
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
        logging.error("Version {} already exists for product: {}".format(
            version, products_api.get_specific(id=product_id).content.name))
        return
    kwargs['product_id'] = product_id
    kwargs['version'] = version
    product_version = create_product_version_object(**kwargs)
    response = utils.checked_api_call(versions_api, 'create_new_product_version',
                                      body=product_version)
    if response: return response.content


@arg("id", help="ID of the ProductVersion to retrieve")
def get_product_version(id):
    """
    Get a specific ProductVersion by ID
    """
    if not version_exists(id):
        logging.error("No ProductVersion with ID {} exists.".format(id))
        return
    response = utils.checked_api_call(versions_api, 'get_specific', id=id)
    if response: return response.content


# TODO: how should constraints be defined? Can a new productId be specified?
# TODO: Version needs to be checked for validity.
@arg("id", help="ID of the ProductVersion to update.")
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
        logging.error("A ProductVersion with id {} doesn't exist.".format(id))
        return

    to_update = versions_api.get_specific(id=id).content
    for key, value in kwargs.items():
        if value is not None:
            setattr(to_update, key, value)
    response = utils.checked_api_call(versions_api, 'update',
                                      id=id,
                                      body=to_update)
    if response:
        return response.content
