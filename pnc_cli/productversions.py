import argparse

from argh import arg
from six import iteritems

import pnc_cli.utils as utils
import pnc_cli.cli_types as types
from pnc_cli import swagger_client
from pnc_cli.pnc_api import pnc_api


__author__ = 'thauser'


def create_product_version_object(**kwargs):
    created_version = swagger_client.ProductVersionRest()
    for key, value in iteritems(kwargs):
        setattr(created_version, key, value)
    return created_version


def version_exists_for_product(id, version):
    existing_products = pnc_api.products.get_product_versions(id=id).content
    if existing_products:
        return version in [x.version for x in existing_products]
    else:
        return False


@arg("-p", "--page-size", help="Limit the amount of build records returned")
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_product_versions(page_size=200, page_index=0, sort="", q=""):
    """
    List all ProductVersions
    """
    content = list_product_versions_raw(page_size, page_index, sort, q)
    if content:
        return utils.format_json_list(content)


def list_product_versions_raw(page_size=200, page_index=0, sort="", q=""):
    response = utils.checked_api_call(pnc_api.product_versions, 'get_all', page_size=page_size, page_index=page_index, sort=sort,
                                      q=q)
    if response:
        return response.content


@arg("product_id", help="ID of product to add a version to", type=types.existing_product_id)
@arg("version", help="Version to add", type=types.valid_version_two_digits)
@arg("-cm", "--current-product-milestone-id",
     help="ID of the milestone this version should be on", type=types.existing_product_milestone)
@arg("-pr", "--product-releases", type=types.existing_product_release, nargs="+",
     help="List of product release IDs for this Product version")
@arg("-pm", "--product-milestones", type=types.existing_product_milestone, nargs="+",
     help="List of milestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=types.existing_bc_set_id, nargs="+",
     help="List of build configuration set IDs to associate with the new version")
def create_product_version(product_id, version, **kwargs):
    """
    Create a new ProductVersion.
    Each ProductVersion represents a supported product release stream, which includes milestones and releases typically associated with a single major.minor version of a Product.
    Follows the Red Hat product support cycle, and typically includes Alpha, Beta, GA, and CP releases with the same major.minor version.

    Example:
    ProductVersion 1.0 includes the following releases:
    1.0.Beta1, 1.0.GA, 1.0.1, etc.
    """
    data = create_product_version_raw(product_id, version, **kwargs)
    if data:
        return utils.format_json(data)


def create_product_version_raw(product_id, version, **kwargs):
    if version_exists_for_product(product_id, version):
        raise argparse.ArgumentTypeError("Version {} already exists for product: {}".format(
            version, pnc_api.products.get_specific(id=product_id).content.name))

    kwargs['product_id'] = product_id
    kwargs['version'] = version
    product_version = create_product_version_object(**kwargs)
    response = utils.checked_api_call(pnc_api.product_versions, 'create_new_product_version',
                                      body=product_version)
    if response:
        return response.content


@arg("id", help="ID of the ProductVersion to retrieve", type=types.existing_product_version)
def get_product_version(id):
    """
    Retrieve a specific ProductVersion by ProductVersion ID
    """
    content = get_product_version_raw(id)
    if content:
        return utils.format_json(content)


def get_product_version_raw(id):
    response = utils.checked_api_call(pnc_api.product_versions, 'get_specific', id=id)
    if response:
        return response.content


# TODO: how should constraints be defined? Can a new productId be specified?
@arg("id", help="ID of the ProductVersion to update.", type=types.existing_product_version)
@arg("-pid", "--product-id", help="ID of product to add a version to", type=types.existing_product_id)
@arg("-v", "--version", help="Version to add", type=types.valid_version_two_digits)
@arg("-cm", "--current-product-milestone-id", help="ID of the ProductMilestone this version should be on",
     type=types.existing_product_milestone)
@arg("-pr", "--product-releases", type=types.existing_product_release, nargs="+",
     help="List of ProductRelease IDs for this Product version")
@arg("-pm", "--product-milestones", type=types.existing_product_milestone, nargs="+",
     help="List of ProductMilestone IDs to associate with the new version")
@arg("-bc", "--build-configuration-set-ids", type=types.existing_bc_set_id, nargs="+",
     help="List of BuildConfigurationSet IDs to associate with the new version")
def update_product_version(id, **kwargs):
    """
    Update the ProductVersion with ID id with new values.
    """
    content = update_product_version_raw(id, **kwargs)
    if content:
        return utils.format_json(content)


def update_product_version_raw(id, **kwargs):
    product_id = kwargs.get('product_id')
    if product_id is None:
        product_id = get_product_version_raw(id).product_id

    version = kwargs.get('version')
    if version is not None:
        if version_exists_for_product(product_id, version):
            raise argparse.ArgumentTypeError("Version {} already exists for product: {}".format(
                version, pnc_api.products.get_specific(id=product_id).content.name))

    to_update = pnc_api.product_versions.get_specific(id=id).content
    for key, value in kwargs.items():
        if value is not None:
            setattr(to_update, key, value)
    response = utils.checked_api_call(pnc_api.product_versions, 'update',
                                      id=id,
                                      body=to_update)
    if response:
        return response.content
