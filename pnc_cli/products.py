from argh import arg
from six import iteritems

import pnc_cli.common as common
import pnc_cli.cli_types as types
import pnc_cli.utils as utils
from pnc_cli.swagger_client import ProductRest
from pnc_cli.swagger_client import ProductsApi
import pnc_cli.user_config as uc

products_api = ProductsApi(uc.user.get_api_client())

__author__ = 'thauser'


def create_product_object(**kwargs):
    created_product = ProductRest()
    for key, value in iteritems(kwargs):
        setattr(created_product, key, value)
    return created_product


@arg("name", help="Name for the Product", type=types.unique_product_name)
@arg("abbreviation", help="The abbreviation or \"short name\" of the new Product", type=types.unique_product_abbreviation)
@arg("-d", "--description", help="Detailed description of the new Product")
@arg("-p", "--product-code", help="The Product code for the new Product")
@arg("-sn", "--pgm-system-name", help="The system code for the new Product")
@arg("-pvids", "--product-version-ids", type=types.existing_product_version, nargs='+',
     help="Space separated list of associated ProductVersion ids.")
def create_product(name, abbreviation, **kwargs):
    """
    Create a new Product
    """
    product = create_product_object(name=name, abbreviation=abbreviation, **kwargs)
    response = utils.checked_api_call(products_api, 'create_new', body=product)
    if response:
        return utils.format_json(response.content)


@arg("product-id", help="ID of the Product to update", type=types.existing_product_id)
@arg("-n", "--name", help="New name for the Product", type=types.unique_product_name)
@arg("-d", "--description", help="New Product description")
@arg("-a", "--abbreviation", help="New abbreviation")
@arg("-p", "--product-code", help="New Product code")
@arg("-sn", "--pgm-system-name", help="New system name")
@arg("--product-version-ids", type=types.existing_product_version, nargs='+',
     help="Space separated list of associated ProductVersion ids.")
def update_product(product_id, **kwargs):
    """
    Update a Product with new information
    """
    to_update = products_api.get_specific(id=product_id).content

    for key, value in iteritems(kwargs):
        if value is not None:
            setattr(to_update, key, value)

    response = utils.checked_api_call(
        products_api, 'update', id=product_id, body=to_update)
    if response:
        return utils.format_json(response.content)


@arg("-i", "--id", help="ID of the Product to retrieve", type=types.existing_product_id)
@arg("-n", "--name", help="Name of the Product to retrieve", type=types.existing_product_name)
def get_product(id=None, name=None):
    """
    Get a specific Product by name or ID
    """
    prod_id = common.set_id(products_api, id, name)
    response = utils.checked_api_call(products_api, 'get_specific', id=prod_id)
    if response:
        return utils.format_json(response.content)


def list_versions_for_product_raw(id=None, name=None, page_size=200, page_index=0, sort='', q=''):
    """
    List all ProductVersions for a given Product
    """
    prod_id = common.set_id(products_api, id, name)
    response = utils.checked_api_call(
        products_api, 'get_product_versions', id=prod_id, page_size=page_size, page_index=page_index, sort=sort, q=q)
    if response:
        return response.content

@arg("-i", "--id", help="ID of the Product to retrieve versions from", type=types.existing_product_id)
@arg("-n", "--name", help="Name of the Product to retrieve versions from", type=types.existing_product_name)
@arg("-p", "--page-size", help="Limit the amount of Product Versions returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_versions_for_product(id=None, name=None, page_size=200, page_index=0, sort='', q=''):
    """
    List all ProductVersions for a given Product
    """
    content = list_versions_for_product_raw(id, name, page_size, page_index, sort, q)
    if content:
        return utils.format_json_list(content)


@arg("-p", "--page-size", help="Limit the amount of Products returned", type=int)
@arg("--page-index", help="Select the index of page", type=int)
@arg("-s", "--sort", help="Sorting RSQL")
@arg("-q", help="RSQL query")
def list_products(page_size=200, page_index=0, sort="", q=""):
    """
    List all Products
    """
    response = utils.checked_api_call(products_api, 'get_all', page_size=page_size, page_index=page_index, q=q, sort=sort)
    if response:
        return utils.format_json_list(response.content)
